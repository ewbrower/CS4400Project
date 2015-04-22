import pymysql
from decimal import Decimal
import datetime

host = "academic-mysql.cc.gatech.edu"
username = "cs4400_Group_33"
passwd = "3RMYn5Tp"

# for Search - 2 separate methods:
# 1. for searching for available books and
# 2. for searching for reserved books
#implement reserve

class Accessor:
    """This class accesses the MySQL database"""
    def __init__(self):
        try:
            db = pymysql.connect(
                host = "academic-mysql.cc.gatech.edu",
                passwd = "3RMYn5Tp",
                user = "cs4400_Group_33",
                db = "cs4400_Group_33",
                charset = "utf8")
        except:
            messagebox.showwarning("Error","Unable to connect to database!")
            raise
        self.db = db

    # lastUser
    # returnBook
    # submitDamagedBook
    # checkoutBook
    # searchForCheckOut
    # updatePenalty
    # typeUser
    # login
    # createAccount
    # createProfile
    # search
    # getCopies
    # holdRequest
    # getIssueData
    # requestExtension
    # locateBook

########## USER / PROFILE MANAGEMENT ###########

    def login(self, user, password):
        sql = 'SELECT * FROM User WHERE USERNAME = "%s" AND '\
            'Password = "%s"'%(user,password)
        resp = self.query(sql)
        if len(resp) == 1:
            return True
        else:
            return False

    def createAccount(self, user, password):
        sql = 'INSERT INTO User VALUES ("%s", "%s")'%(user, password)
        #check if the account already exists exist
        userExist = self.verify(user, "User")
        if not userExist:
            resp = self.query(sql)
            return True
        return False
	
    def createProfile(self, user, fname, lname, dob, debarred, gender,
        email, address, faculty, penalty, dept):
        sql = 'INSERT INTO Student_Faculty VALUES("%s", "%s", "%s",'\
                '"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'\
                %(user, fname, lname, dob, debarred, gender, email, address,
                faculty, penalty, dept)
        # check if exists in User table
        userExist = self.verify(user, "User")
        profileExist = self.verify(user, "Student_Faculty")
        # so if there is a user, but no profile yet
        if (userExist and not profileExist):
            self.query(sql)
            return True
        return False

########################### SEARCH #####################

    def search(self, ISBN = None, title = None, author = None,
            publisher = None, edition = None):
        # THIS IS TERRIBLE
        terms = dict(locals())
        terms.pop("self", None)
        if terms["author"] != None:
            sql = self.searchAuthor(terms["author"])
        else:
            sql = self.searchBook(terms)
        # use the sql to get a list of ISBNs
        res = self.query(sql)
        totalList = []
        for item in res:
            if item[0] is not None:
                totalList.append(item[0])
        # select available and unheld books based on ISBN
        if totalList == []:
            return None
        # go through totalList and remove reserve books
        isbnList = []
        for isbn in totalList:
            sql = 'SELECT reserve FROM Book WHERE ISBN = "%s"'%isbn
            if self.query(sql)[0][0] == 0:
                isbnList.append(isbn)
        elif len(isbnList) >= 1:
            resList = []
            for ISBN in isbnList:
                print(self.selectBooks(ISBN))
                resList.append(self.selectBooks(ISBN))
            return resList

    def searchAuthor(self, terms):
        sql = 'SELECT ISBN FROM Author '\
            'WHERE author LIKE "%%%s%%" '%terms["author"]
        if terms["ISBN"] != None:
            sql += 'AND ISBN LIKE "%%%s%%" '%terms["ISBN"]
        return sql

    def searchBook(self, terms):
        first = True
        sql = 'SELECT ISBN FROM Book '
        for param in terms:
            if terms[param] is not None:
                if first:
                    sql += 'WHERE %s LIKE "%%%s%%" '%(param, terms[param])
                    first = False
                else:
                    sql += 'AND %s LIKE "%%%s%%" '%(param, terms[param])
        return sql

    def selectBooks(self, ISBN):
        heldSQL = 'SELECT b.ISBN, (SELECT count(*) FROM Book_Copy AS c '\
            'WHERE c.checked_out = 0 '\
            'AND c.hold = 1 '\
            'AND c.damaged = 0 '\
            'AND b.ISBN = c.ISBN) AS Count '\
            'FROM Book AS b WHERE ISBN = "%s";'%ISBN
        unheldSQL = 'SELECT b.ISBN, (SELECT count(*) FROM Book_Copy AS c '\
            'WHERE c.checked_out = 0 '\
            'AND c.hold = 0 '\
            'AND c.damaged = 0 '\
            'AND b.ISBN = c.ISBN) AS Count '\
            'FROM Book AS b WHERE ISBN = "%s";'%ISBN
        metaSQL = 'SELECT title, edition FROM Book WHERE ISBN = "%s"'%ISBN
        held = self.query(heldSQL)[0]
        unheld = self.query(unheldSQL)[0]
        title, edition = self.query(metaSQL)[0]
        res = {"ISBN" : ISBN, "held" : held[1], "unheld" : unheld[1],
                "title": title, "edition": edition}
        return res

####################### REQUESTS #####################################

    def holdRequest(self, user, ISBN):
        # bookData["available"] = books that aren't checked out
        # bookData["unheld"] = books that are checked out but not on hold
        copy = self.getNextAvailable(ISBN)
        print(copy)
        if copy is None:
            print("no book copy available")
            return False
        # check to see if the user already future requested this book (not copy)
        if user in self.getFutureRequesters(ISBN):
            print("already a future requester for this book")
            return False
        # check to see if the user already checked out the book
        if not self.canCheckout(user, ISBN):
            print("cnanot check out another copy of this ISBN")
            return False
        if self.debarred(user):
            return "debarred"
        issueSQL = 'INSERT INTO Issues (username, issue_date, '\
                'extension_count, copy_num, return_date, ISBN) VALUES '\
                '("%s", CURDATE(), 0, %s, '\
                'DATE_ADD(CURDATE(), INTERVAL 17 DAY), "%s")'\
                %(user, copy, ISBN)
        self.query(issueSQL)
        # now update that specific copy of the book (NIX THIS)
        reqSQL = 'UPDATE Book_Copy SET hold = 1 WHERE ISBN = "%s" '\
            'AND copy_num = %s'%(ISBN, copy)
        self.query(reqSQL)
        issueid = self.query('SELECT last_insert_id()')[0][0]
        return issueid

    def requestExtension(self, issue):
        # get some data to munch on
        checkSQL = 'SELECT username, extension_count, copy_num, '\
            'return_date, ISBN FROM Issues WHERE issue_id = %s'%issue
        ans = self.query(checkSQL)
        user = ans[0][0]
        extCount = ans[0][1] + 1
        copy_num = ans[0][2]
        retDate = ans[0][3] + datetime.timedelta(7)
        ISBN = ans[0][4]
        # make sure they aren't extending too many times
        if extCount == 3 and self.isFaculty(user) == False:
            print("extending too many times")
            return False
        elif extCount == 6:
            print("extended too many times")
            return False
        # make sure the book doesn't have a hold on it from anyone
        holdSQL = 'SELECT future_requester FROM Book_Copy WHERE ISBN = "%s" '\
            'AND copy_num = %s'%(ISBN, copy_num)
        future = self.query(holdSQL)[0][0]
        if future != None:
            print("%s is already a future_requester"%future)
            return False
        # update the issue_id with the larger extension
        extSQL = 'UPDATE Issues SET extension_count = %s, return_date = "%s" '\
            'WHERE issue_id = %s'%(extCount, retDate, issue)
        self.query(extSQL)
        return True

    def futureHoldRequest(self, ISBN):
        # get copy num sorted by available date
        if self.futureRequestable(ISBN) == False:
            return False
        sql = 'SELECT c.copy_num, i.return_date '\
                'FROM Book_Copy AS c '\
                'INNER JOIN Issues AS i ON c.ISBN = i.ISBN '\
                'AND c.copy_num = i.copy_num '\
                'WHERE i.return_date > CURDATE() '\
                'AND c.ISBN = "%s" '\
                'ORDER BY i.return_date LIMIT 1;'%ISBN
        res = self.query(sql)
        print(res)
        return res[0]

    def addFutureRequest(self, user, ISBN, copy):
        sql = 'UPDATE Book_Copy SET future_requester = "%s" '\
                'WHERE ISBN = "%s" AND copy_num = %s'\
                %(user, ISBN, copy)
        self.query(sql)
        return True

    def checkReturn(self, issue):
        checkSQL = 'SELECT username, copy_num, ISBN FROM Issues '\
                    'WHERE issue_id = %s'%issue
        ans = self.query(checkSQL)
        return ans[0]


##################### LOCATE CHECKOUT #################################

    def locateBook(self, ISBN):
        sql = 'SELECT shelf, subject, '\
            '(SELECT aisle FROM Shelf s WHERE s.shelf=b.shelf),'\
            '(SELECT floor FROM Subject u WHERE u.name=b.subject) '\
            'FROM Book b WHERE ISBN = "%s"'%ISBN
        return self.query(sql)

    def checkData(self, issue):
        checkSQL = 'SELECT username, issue_date, copy_num, isbn FROM Issues '\
            'WHERE issue_id="%s"'%issue
        user, issueDate, copy_num, ISBN = self.query(checkSQL)[0]
        return user, issueDate, copy_num, ISBN

    def checkoutBook(self, issue):
        # check if a book has been on hold for three days
        user, issueDate, copy_num, ISBN = self.checkData(issue)
        diff = datetime.date.today() - issueDate
        if diff.days > 3:
            return False
        # then update Issues, add estimated return date +14
        issueSQL = 'UPDATE Issues SET return_date = DATE_ADD(return_date,'\
            'INTERVAL 14 DAY) WHERE issue_id = %s'%issue
        self.query(issueSQL)
        copySQL = 'UPDATE Book_Copy SET checked_out = 1, hold = 0 '\
            'WHERE ISBN = "%s" AND copy_num = %s'%(ISBN, copy_num)
        self.query(copySQL)
        return True

    def getIssueData(self, issue):
        sql = 'SELECT issue_date, extension_date, return_date FROM Issues '\
            'WHERE issue_id = %s'%issue
        print(sql)
        dateList = self.query(sql)
        print(dateList)
        return dateList

    def getIssue(self, issue):
        sql = 'SELECT * FROM Issues WHERE issue_id = %s'%issue
        issueList = self.query(sql)
        print(issueList)
        return issueList
        
    def returnBook(self, issue):
        # check to see if current date is past return date
        today = datetime.date.today()
        issueSQL = 'SELECT username, copy_num, return_date, ISBN '\
            'FROM Issues WHERE issue_id = %s'%issue
        user, copy, retDate, ISBN = self.query(issueSQL)[0]
        if retDate < today:
            # this means they turned it in late
            diff = today - retDate
            amount = diff.days * 0.5
            self.addPenalty(user, amount)
        # update copy of the book
        retSQL = 'UPDATE Book_Copy SET checked_out = 0 '\
            'WHERE ISBN = "%s" AND copy_num = %s'%(ISBN, copy)
        # add new return date in issues
        self.query(retSQL)
        # update the issue to make it accurate
        issueSQL = 'UPDATE Issues SET return_date = "%s" '\
                    'WHERE issue_id = %s'%(today, issue)
        self.query(issueSQL)
        return True

############### DAMAGED LOST BOOKS ###############
    def brokenBookOLD(self, user, ISBN, copy, damaged):
        # get price of the book
        costSQL = 'SELECT cost FROM Book WHERE ISBN = "%s"'%ISBN
        cost = self.query(costSQL)[0][0]
        # get current penalty
        if damaged:
            amount = float(cost) * 0.5
        else:
            amount = float(cost)
        self.addPenalty(user, amount)
        # get specific copy of book and do shit to it
        sql = 'UPDATE Book_Copy SET damaged = 1 WHERE ISBN = "%s" '\
            'AND copy_num = "%s"'%(ISBN,copy)
        return self.query(sql)

    def brokenBook(self, user, ISBN, copy, damaged):
        # get specific copy of book and do shit to it
        sql = 'UPDATE Book_Copy SET damaged = 1 WHERE ISBN = "%s" '\
            'AND copy_num = "%s"'%(ISBN,copy)
        return self.query(sql)

    def lastUser(self, ISBN, copy):
        sql = 'SELECT username FROM Issues WHERE ISBN = "%s" AND copy_num=%s '\
            'ORDER BY issue_date DESC LIMIT 1'%(ISBN,copy)
        lastuser = self.query(sql)
        return lastuser

    def getName(self, user):
        sql = 'SELECT fname, lname FROM Student_Faculty '\
                'WHERE username = "%s"'%user
        return self.query(sql)[0]

    def submitDamagedBook(self, user, ISBN, copy):
        self.brokenBook(user, ISBN, copy, True)
        return True

    def submitLostBook(self, user, ISBN, copy):
        self.brokenBook(user, ISBN, copy, False)
        return True

    def updatePenalty(self, amount, user):
        sql = 'UPDATE Student_Faculty SET penalty = %s '\
            'WHERE username = "%s"'%(amount, user)
        self.query(sql)
        return True

############## REPORTS ###############

    def damageReport(self):
        sql = 'SELECT count(c.ISBN), b.subject, ( '\
        'SELECT MONTH(MAX(return_date)) FROM Issues AS i '\
        'WHERE i.ISBN = c.ISBN AND i.copy_num = c.copy_num) AS LastDate '\
        'FROM Book_Copy AS c '\
        'INNER JOIN Book AS b ON b.ISBN = c.ISBN '\
        'WHERE c.damaged = 1 '\
        'GROUP BY LastDate, b.subject'
        return self.query(sql)

    def popularBookReport(self, month):
        sql ='SELECT b.title, COUNT(i.issue_id) '\
            'FROM Issues AS i '\
            'INNER JOIN Book AS b ON i.ISBN=b.ISBN '\
            'WHERE MONTH(i.issue_date)=%s '\
            'GROUP BY MONTH(i.issue_date), b.title '\
            'ORDER BY COUNT(i.issue_id) DESC LIMIT 3'%month
        return self.query(sql)

    def frequentReport(self, month):
        sql = 'SELECT s.fname, s.lname, COUNT( i.issue_id ) '\
              'FROM Issues AS i '\
              'INNER JOIN Student_Faculty AS s ON s.username = i.username '\
              'WHERE MONTH(i.issue_date)=%s '\
              'GROUP BY MONTH( i.issue_date ) , s.username '\
              'HAVING COUNT(i.issue_id)>10 '\
              'ORDER BY COUNT( i.issue_id ) DESC '\
              'LIMIT 5'%month
        return self.query(sql)

    def popularSubjectReport(self, month):
        sql = 'SELECT b.subject, COUNT(i.issue_id) '\
              'FROM Issues AS i '\
              'INNER JOIN Book AS b ON i.ISBN=b.ISBN '\
              'WHERE MONTH(i.issue_date)=%s '\
              'GROUP BY MONTH(i.issue_date), b.subject '\
              'ORDER BY COUNT(i.issue_id) DESC LIMIT 3'%month
        return self.query(sql)

######################## HELPER CODE ##########################

    def verify(self, user, table = "User"):
        # you have to insert tables first
        sql = 'SELECT * FROM %s WHERE USERNAME = "%s"' %(table, user)
        # MySQL evaluates backwards, so let pymysql figure out the
        # other variables how it wants to
        res = self.query(sql)
        # if there is one result, the user already exists in the table
        if len(res) == 1:
            return True
        else:
            return False

    def getAvailableCopies(self, ISBN):
        # return books not checkoed out and not held
        sql = 'SELECT b.ISBN, (SELECT count(*) FROM Book_Copy AS c '\
            'WHERE c.checked_out = 0 '\
            'AND c.hold = 0 '\
            'AND b.ISBN = c.ISBN) AS Count '\
            'FROM Book AS b WHERE ISBN = "%s";'%ISBN
        return self.query(sql)[0]

    def getReservedCopies(self, ISBN):
        # return books not checked out but on hold
        # just need a number
        sql = 'SELECT b.ISBN, (SELECT count(*) FROM Book_Copy AS c '\
            'WHERE c.checked_out = 0 '\
            'AND c.hold = 1 '\
            'AND b.ISBN = c.ISBN) AS Count '\
            'FROM Book AS b WHERE ISBN = "%s";'%ISBN
        return self.query(sql)[0]

    def getCopyMeta(self, ISBN, checked_out = None, hold = None,
            future_requester = "NULL", damaged = 0):
        terms = dict(locals())
        terms.pop("self", None)
        terms.pop("ISBN")
        sql = 'SELECT (SELECT count(*) FROM Book_Copy AS c '
        first = True
        for param in terms:
            if terms[param] is not None:
                if first:
                    sql += 'WHERE '
                    first = False
                else:
                    sql += 'AND '
                if terms[param] == "NULL":
                    sql += 'c.%s IS NULL '%(param)
                else:
                    sql += 'c.%s = %s '%(param, terms[param])
        sql += 'AND b.ISBN = c.ISBN) AS Count '\
            'FROM Book AS b WHERE ISBN = "%s";'%ISBN
        return self.query(sql)[0][0]

    def futureRequestable(self, ISBN):
        if self.getCopyMeta(ISBN, 0, 0) > 0:
            return False
        if self.getCopyMeta(ISBN, 0, 1) > 0 or self.getCopyMeta(ISBN, 1,0) > 0:
            return True
        return False

    def getNextAvailable(self, ISBN):
        bookData = self.selectBooks(ISBN)
        sql = 'SELECT copy_num FROM Book_Copy WHERE ISBN = "%s" '\
            'AND damaged = 0 AND checked_out = 0 '\
            'AND hold = 0 '%ISBN
        # bookData["unheld"] = books that are checked out but not on hold
        if bookData["held"] <= 0 and bookData["unheld"] <= 0:
            return None
        sql += 'ORDER BY copy_num'
        copy = self.query(sql)[0][0]
        return copy

    def getFutureRequesters(self, ISBN):
        sql = 'SELECT future_requester FROM Book_Copy WHERE ISBN = "%s"'%ISBN
        futureList = []
        for tinyList in self.query(sql):
            futureList.append(tinyList[0])
        return futureList

    def canCheckout(self, user, ISBN):
        sql = 'SELECT count(1) FROM Issues WHERE username = "%s" '\
            'AND ISBN = "%s" AND return_date > CURDATE()'%(user, ISBN)
        res = self.query(sql)
        if res[0][0] >= 1:
            return False
        else:
            return True

    def isFaculty(self, user):
        # return True if staff, False otherwise
        sql = 'SELECT count(1) FROM Student_Faculty WHERE username = "%s" '\
        'AND faculty = 1'%user
        res = self.query(sql)
        if res[0][0] == 1:
            return True
        else:
            return False

    def typeUser(self, user):
        sql= 'SELECT count(1) FROM Staff WHERE username ="%s"'%user
        res = self.query(sql)
        if res[0][0]==1:
            return True
        else:
            return False

    def debarred(self, user):
        sql = 'SELECT debarred FROM Student_Faculty WHERE username '\
                '= "%s"'%user
        res = self.query(sql)[0][0]
        if res == 1:
            return True
        else:
            return False

    def validateIssue(self, user, issueid):
        sql = 'SELECT username FROM Issues WHERE issue_id = %s'%issueid
        dataName = self.query(sql)[0][0]
        if user == dataName:
            return True
        else:
            return False

    def addPenalty(self, user, amount):
        penaltySQL = 'SELECT penalty FROM Student_Faculty WHERE '\
            'username = "%s"'%user
        penalty = self.query(penaltySQL)[0][0]
        # solve for new penalty, convert to string
        newPen = str(float(penalty) + amount)
        penaltySQL = 'UPDATE Student_Faculty SET penalty = %s '\
            'WHERE username = "%s";'%(newPen, user)
        self.query(penaltySQL)

############## CRITICAL ################

    def query(self, sql):
        # turn this on to print all SQL queries
        if True:
            print("---\n" + sql + "\n---")
        db = self.db.cursor()
        resp = []
        # try:
        db.execute(sql)
        # except ProgrammingError as p:
        #     print(p)
        # except DataError as d:
        #     print(d)
        # except IntegrityError as i:
        #     print(i)
        # except OperationalError as o:
        #     print(o)
        # except NotSupportedError as n:
        #     print(n)
        # except:
        #     print("Unknown error")
        resp = self.clean(db.fetchall())
        if resp == []:
            return [[None]]
        return resp

    def clean(self, mess):
        resp = []
        if isinstance(mess, tuple):
            for item in mess:
                resp.append(self.clean(item))
        else:
            # this is incredibly hackish!!!
            # and not extensible either
            if type(mess) is bytes:
                if mess.decode() == '\x00':
                    return False
                else:
                    return True
            elif type(mess) is Decimal:
                return float(mess)
            return mess
        return resp



dis = Accessor()


# print(dis.futureRequestable("0-123-81479-0"))
# print(dis.getCopyMeta("0-123-81479-0",0,1))
# print(dis.getCopyMeta("0-123-81479-0",1,0))

# print(dis.futureHoldRequest("0-136-08620-9"))


# sql = dis.searchAuthor({"author":"Addison", "ISBN":"0-136-08620-9"})
# print(dis.query(sql))
# sql = dis.searchAuthor({"author":"S", "ISBN":None})
# print(dis.query(sql))




















## extra room
