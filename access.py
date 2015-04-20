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
            sql = self.searchAuthor(terms)
        else:
            sql = self.searchBook(terms)
        # use the sql to get a list of ISBNs
        res = self.query(sql)
        isbnList = []
        for item in res:
            if item[0] is not None:
                isbnList.append(item[0])
        # select available and unheld books based on ISBN
        if isbnList == []:
            return None
        elif len(isbnList) >= 1:
            resList = []
            for ISBN in isbnList:
                print(self.selectBooks(ISBN))
                resList.append(self.selectBooks(ISBN))
            return resList

    def searchAuthor(self, terms):
        sql = 'SELECT ISBN FROM Author AS b '\
            'WHERE author LIKE "%%%s%%"'%(terms["author"])
        if terms["ISBN"] != None:
            sql += ' WHERE ISBN LIKE "%%%s%%" '%ISBN
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
        availSQL = 'SELECT b.ISBN, (SELECT count(*) FROM Book_Copy AS c '\
            'WHERE c.checked_out = 0 AND b.ISBN = c.ISBN) AS Count '\
            'FROM Book AS b WHERE ISBN = "%s";'%ISBN
        heldSQL = 'SELECT b.ISBN, (SELECT count(*) FROM Book_Copy AS c '\
            'WHERE c.future_requester IS NULL AND b.ISBN = c.ISBN) AS Count '\
            'FROM Book AS b WHERE ISBN = "%s";'%ISBN
        avail = self.query(availSQL)[0]
        unheld = self.query(heldSQL)[0]
        res = {"ISBN" : ISBN, "available" : avail[1], "unheld" : unheld[1]}
        return res

####################### REQUESTS

    def holdRequest(self, user, ISBN):
        # also really hackish
        if not self.availableBook(ISBN, 'r'):
            return False
        copy = self.getNextAvailable(ISBN)
        issueSQL = 'INSERT INTO Issues (username, issue_date, extension_date, '\
            'extension_count, copy_num, return_date, ISBN) VALUES '\
            '("%s", CURDATE(), DATE_ADD(CURDATE(), INTERVAL 7 DAY), 1, %s,'\
            ' DATE_ADD(CURDATE(), INTERVAL 10 DAY), "%s")'%(user, copy, ISBN)
        self.query(issueSQL)
        # now update that specific copy of the book
        reqSQL = 'UPDATE Book_Copy SET future_requester = "%s" '\
        'WHERE ISBN = "%s" AND copy_num = %s'%(user, ISBN, copy)
        self.query(reqSQL)
        return True

    def requestExtension(self, issue):
        checkSQL = 'SELECT username, extension_count, copy_num, return_date, ISBN '\
            'FROM Issues WHERE issue_id = %s'%issue
        ans = self.query(checkSQL)
        print(ans)
        user = ans[0][0]
        extCount = ans[0][1] + 1
        copy_num = ans[0][2]
        retDate = ans[0][3] + datetime.timedelta(7)
        ISBN = ans[0][4]
        # print(extCount)
        # print(copy_num)
        print(retDate)
        # print(ISBN)
        # make sure they aren't extending too many times
        if extCount == 3 and self.isFaculty(user) == False:
            print("extended three times already")
            return False
        elif extCount == 6:
            return False
        # make sure the book doesn't have a hold on it
        holdSQL = 'SELECT future_requester FROM Book_Copy WHERE ISBN = "%s" '\
            'AND copy_num = %s'%(ISBN, copy_num)
        future = self.query(holdSQL)
        print(future)
        if future != "NULL":
            print("this")
            return False
        extSQL = 'UPDATE Issues SET extension_count = %s, return_date = "%s" '\
            'WHERE issue_id = %s'%(extCount, retDate, issue)
        self.query(extSQL)
        return True

    def futureHoldRequest(self, user, ISBN):
        # get copy num sorted by available date
        sql = 'SELECT b.ISBN, (SELECT copy_num FROM Book_Copy AS c '\
            'WHERE c.checked_out = 0 AND b.ISBN = c.ISBN) AS Copy '\
            'FROM Book AS b WHERE ISBN = "%s" ORDER BY c.return_date'%ISBN
        print(self.query(sql))
        # take out books that already have a future hold request

    def locateBook(self, ISBN):
        sql = 'SELECT shelf, subject, '\
            '(SELECT aisle FROM Shelf s WHERE s.shelf=b.shelf),'\
            '(SELECT floor FROM Subject u WHERE u.name=b.subject) '\
            'FROM Book b WHERE ISBN = "%s"'%ISBN
        return self.query(sql)

    def checkoutBook(self, issue):
        # check if a book has been on hold for three days
        checkSQL = 'SELECT username, issue_date, copy_num, isbn FROM Issues '\
            'WHERE issue_id="%s"'%issue
        user, issueDate, copy_num, ISBN = self.query(checkSQL)[0]
        diff = datetime.date.today() - issueDate
        if diff.days > 3:
            return False
        # check if that copy is damaged
        damSQL = 'SELECT damaged FROM Book_Copy WHERE ISBN = "%s" '\
            "AND copy_num = %s"%(ISBN, copy_num)
        dam = self.query(damSQL)[0][0]
        if dam == 1:
            return False
        # then update Issues, add estimated return date +14
        issueSQL = 'UPDATE Issues SET return_date = DATE_ADD(return_date,'\
            'INTERVAL 14 DAY) WHERE issue_id = %s'%issue
        self.query(issueSQL)
        copySQL = 'UPDATE Book_Copy SET checked_out = 1 WHERE ISBN = "%s" '\
            'AND copy_num = %s'%(ISBN, copy_num)
        self.query(copySQL)
        return True

    def getIssueData(self, issue):
        sql = 'SELECT issue_date, extension_date, return_date FROM Issues '\
            'WHERE issue_id = %s'%issue
        print(sql)
        dateList = self.query(sql)
        print(dateList)
        return dateList
        
    def returnBook(self, issue):
        # check to see if current date is past return date,
        today = datetime.date.today()
        # print(today)
        issueSQL = 'SELECT username, copy_num, return_date, ISBN '\
            'FROM Issues WHERE issue_id = %s'%issue
        user, copy, retDate, ISBN = self.query(issueSQL)[0]
        if retDate < today:
            # this means they turned it in late
            diff = today - retDate
            amount = diff.days * 0.5
            self.addPenalty(user, amount)
        retSQL = 'UPDATE Book_Copy SET checked_out = 0 '\
            'WHERE ISBN = "%s" AND copy_num = %s'%(ISBN, copy)
        # add new return date in issues
        self.query(retSQL)
        return True

##### DAMAGED LOST BOOKS ###############
    def brokenBook(self, user, ISBN, copy, damaged):
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

    def lastUser(self, ISBN, copy):
        sql = 'SELECT username FROM Issues WHERE ISBN = %s AND copy_num=%s'\
            'ORDER BY issue_date DESC LIMIT 1'%(ISBN,copy)
        lastuser = self.query(sql)
        return lastuser

    def submitDamagedBook(self, user, ISBN, copy):
        self.brokenBook(user, ISBN, copy, True)
        return True

    def submitLostBook(self, user, ISBN, copy):
        self.brokenBook(user, ISBN, copy, False)
        return True

    def updatePenalty(self, user):
        sql = 'UPDATE Student_Faculty SET penalty = %s '\
            'WHERE username = "%s"'%user
        self.query(sql)
        return True

############## REPORTS ###############

    def generateReport(self):
        # generic bundling of report information
        pass

    def damageReport(self):
        # get damaged books
        pass

    def frequentReport(self):
        # frequent users
        pass

    def popularBookReport(self, monthList = [1, 2, 3]):
        # get popular books
        # month list is a list of ints (months)
        # for month in monthList...
        # TODO: might need to change it to always do last three months
        pass

    def popularSubjectReport(self):
        # popular subject
        pass

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

    def availableBook(self, ISBN, flag = 'c'):
        """returns a boolean if there is an available book"""
        sql = 'SELECT count(*) FROM Book_Copy WHERE ISBN = "%s" '%ISBN
        if flag == 'r':
            sql += 'AND future_requester IS NULL'
        elif flag == 'c':
            sql += 'AND checked_out = 0'
        res = self.query(sql)[0][0]
        if res == 0:
            return False
        else:
            return True

    def getNextAvailable(self, ISBN):
        # TODO FIX THIS!
        sql = 'SELECT * FROM Book_Copy WHERE ISBN = "%s"'%ISBN
        res = self.query(sql)
        for copy in res:
            #if copy[]
            #print(item)
            pass
        return 1

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

    def addPenalty(self, user, amount):
        penaltySQL = 'SELECT penalty FROM Student_Faculty WHERE '\
            'username = "%s"'%user
        penalty = self.query(penaltySQL)[0][0]
        # solve for new penalty, convert to string
        newPen = str(float(penalty) + amount)
        penaltySQL = 'UPDATE Student_Faculty SET penalty = %s '\
            'WHERE username = "%s";'%(newPen, user)
        self.query(penaltySQL)

    def query(self, sql):
        # turn this on to print all SQL queries
        if True:
            print(sql)
        db = self.db.cursor()
        resp = []
        db.execute(sql)
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


















## extra room
