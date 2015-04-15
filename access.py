import pymysql
from decimal import Decimal

host = "academic-mysql.cc.gatech.edu"
username = "cs4400_Group_33"
passwd = "3RMYn5Tp"

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

    def login(self, user, password):
        sql = 'SELECT * FROM User WHERE USERNAME = "%s" AND Password = "%s"'%(user,password)
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


    def search(self, ISBN = None, title = None, author = None,
            publisher = None, edition = None):
        #TODO: cut it down to ISBN author title
        # v this is really hackish, do not replicate
        terms = locals()
        terms.pop("self", None)
        # if author !None, then search the Author database only and return
        if author != None and ISBN != None:
            sql = 'SELECT * FROM Author '\
                'WHERE ISBN LIKE "%%%s%%" '\
                'AND author LIKE "%%%s%%"'%(ISBN, author)
            resp = self.query(sql, (ISBN, author))
            return resp
        # otherwise, construct the SQL statement
        first = True
        sql = "SELECT * FROM Book "
        for param in terms:
            if terms[param] is not None:
                print(param)
                print(terms[param])
                if first:
                    sql += 'WHERE %s LIKE "%%%s%%" '%(param, terms[param])
                    first = False
                else:
                    sql += 'AND %s LIKE "%%%s%%" '%(param, terms[param])
        # and execute
        resp = self.query(sql)
        return resp

    def selectBook(self, ISBN, copy = -1):
        #if copy = -1, then copy number doesn't matter
        sql = 'SELECT * FROM Book_Copy WHERE ISBN = "%s"'%ISBN
        if copy is not -1:
            sql += ' AND copy_num = "%s"'%copy
        return self.query(sql)

    def getCopies(self, ISBN):
        sql = 'SELECT count(*) FROM Book_Copy WHERE ISBN = "%(ISBN)s"'
        # return the only item in the query list and the SQL SELECT list
        return self.query(sql)[0][0]

    def submitRequest(self, ISBN):
        pass

    def locateBook(self, ISBN):
        sql = 'SELECT shelf, subject, '\
            '(SELECT aisle FROM Shelf s WHERE s.shelf=b.shelf),'\
            '(SELECT floor FROM Subject u WHERE u.name=b.subject) '\
            'FROM Book b WHERE ISBN = "%s"'%ISBN
        return self.query(sql)

    def checkoutBook(self, user, ISBN, copy):
        pass

    def returnBook(self, user, ISBN, copy = -1):
        # if copy = -1, then we have to find out what copy this
        # user checked out
        # check to see if current date is past return date,
        # then go get the fine
        pass

    # might want to consolidate damaged and lost
    def submitDamagedBook(self, user, ISBN, copy):
        self.brokenBook(user, ISBN, copy, True)
        return True

    def submitLostBook(self, user, ISBN, copy):
        self.brokenBook(user, ISBN, copy, False)
        return True

    def brokenBook(self, user, ISBN, copy, damaged):
        # get price of the book
        costSQL = 'SELECT cost FROM Book WHERE ISBN = "%s"'%ISBN
        cost = self.query(costSQL)[0][0]
        # get current penalty
        penaltySQL = 'SELECT penalty FROM Student_Faculty WHERE username = "%s"'%user
        penalty = self.query(penaltySQL)[0][0]
        # solve for new penalty, convert to string
        if damaged:
            newPen = str(float(penalty) + float(cost) * 0.5)
        else:
            newPen = str(float(penalty) + float(cost))
        penaltySQL = 'UPDATE Student_Faculty SET penalty = %s '\
            'WHERE username = "%s";'%(newPen, user)
        self.query(penaltySQL)
        # get specific copy of book and do shit to it
        sql = 'UPDATE Book_Copy SET damaged = 1 '\
            'WHERE ISBN = "%s" AND copy_num = "%s"'%(ISBN,copy)
        return self.query(sql)

############## REPORTS ###############

    def generateReport(self):
        # generic bundling of report information
        pass

    def damageReport(self):
        # get damaged books
        pass

    def popularBookReport(self, monthList = [1, 2, 3]):
        # get popular books
        # month list is a list of ints (months)
        # for month in monthList...
        # TODO: might need to change it to always do last three months
        pass

    def frequentReport(self):
        # frequent users
        pass

    def popularSubjectReport(self):
        # popular subject
        pass

######################## HELPER CODE ##########################

    def test(self, string):
        return string

    def alltabs(self, table):
        db = self.db.cursor()
        sql = 'SELECT * FROM %s' %table
        db.execute(sql)
        return db

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

    def availableBook(self, ISBN):
        sql = 'SELECT checked_out FROM Book_Copy WHERE ISBN = "%s"' %ISBN
        res = self.query(sql)
        if len(res) == 0:
            return False
        else:
            return res

    def query(self, sql):
        db = self.db.cursor()
        resp = []
        db.execute(sql)
        resp = self.clean(db.fetchall())
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

# success = dis.login("dip","hunter8") 
# print(success) # FALSE
# success = dis.createAccount("dip","hunter8")
# print(success) # TRUE
# success = dis.login("dip","hunter8")
# print(success) # TRUE

# ver = dis.verify("diplo")
# print(ver) # TRUE

# success = dis.createProfile("diplo", "nomen", "lomen", "12", False, 'F', "dip@di",
#     "122", False, 0, "music")
# print(success) # TRUE

# resp = dis.search(None,'abc')
# print(resp)

# resp = dis.selectBook('123456789012')
# print(resp) # returns copy tuples (only one in this case)

# resp = dis.locateBook(123456789012)
# print(resp) # returns floor, subject, aisle, shelf (or something)


# res = dis.submitDamagedBook("ewbrower","0-136-08620-9",1)
# print(res)

# res = dis.getCopies("0-136-08620-9")
# print(res)










## extra room