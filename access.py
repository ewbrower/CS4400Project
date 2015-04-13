import pymysql
from tkinter import messagebox

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
                db="cs4400_Group_33")
        except:
            messagebox.showwarning("Error","Unable to connect to database!")
            raise
        self.db = db

    def login(self, user, password):
        db = self.db.cursor()
        db.execute(
            "SELECT * FROM User WHERE USERNAME = %s AND Password = %s",
            (username,password))
        # now check if the username and password are correct
        if db.rowcount == 1:
            return True
        else:
            return False

    def createAccount(self, user, password):
        db = self.db.cursor()
        # does this user already exist? if not, then create an account
        # doesnt actually look yet
        userExist = self.verify(user, "User")
        if (not userExist):
            db.execute(
                "INSERT INTO User VALUES (%s, %s)",
                (user, password))
            return True
        #returns false if failed
        else:
            return False

    def createProfile(self, user, fname, lname, dob, debarred, gender,
        email, address, faculty, penalty, dept):
        db = self.db.cursor()
        # check if exists in User table
        userExist = self.verify(user, "User")
        profileExist = self.verify(user, "Student_Faculty")
        # so if there is a user, but no profile yet
        if (userExist and not profileExist):
            #TODO: need a lot more value verifying here !!!!!!
            sql = 'INSERT INTO Student_Faculty VALUES("%s", "%s", "%s",'\
                '"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'\
                %(user, fname, lname, dob, debarred, gender, email, address,
                faculty, penalty, dept)
            # execute
            db.execute(sql)
            return True
        return False


    def search(self, ISBN = None, title = None, publisher = None,
        edition = None, author = None):
        # v this is really hackish, do not replicate
        terms = locals()
        terms.pop("self", None)
        # grab yo database
        db = self.db.cursor()
        # if author !None, then search the Author database only and return
        if author != None and ISBN != None:
            sql = 'SELECT * FROM Author WHERE ISBN = %s AND author = %s'
            db.execute(sql, (ISBN, author))
            return db
        # otherwise, construct the SQL statement
        first = True
        sql = "SELECT * FROM Book WHERE "
        for param in terms:
            if terms[param] is not None:
                if first:
                    sql += '%s = "%s" '%(param, terms[param])
                    first = False
                else:
                    sql += 'AND %s = "%s" '%(param, terms[param])
        print(sql)
        # and execute
        db.execute(sql)
        return db

    def selectBook(self, ISBN, copy = -1):
        #if copy = -1, then copy number doesn't matter
        db = self.db.cursor()
        sql = 'SELECT * FROM Book_Copy WHERE ISBN = "%s"'%ISBN
        if copy is not -1:
            sql += ' AND copy_num = "%s"'%copy
        db.execute(sql)

    def submitRequest(self):
        pass

    def getBookDetails(self, ISBN):
        pass

    def locateBook(self, ISBN):
        pass

    def checkoutBook(self, ISBN, copy):
        pass

    def returnBook(self, user, ISBN, copy = -1):
        # if copy = -1, then we have to find out what copy this
        # user checked out
        # check to see if current date is past return date,
        # then go get the fine
        pass

    def submitDamagedBook(self, ISBN, copy):
        # fine here?
        pass

    def submitLostBook(self, ISBN, copy):
        # delete from database?
        pass

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
        # populat subject
        pass

######################## HELPER CODE ##########################

    def test(self, string):
        return string

    def alltabs(self, table):
        db = self.db.cursor()
        sql = "SELECT * FROM %s" %table
        db.execute(sql)
        return db

    def verify(self, user, table = "User"):
        db = self.db.cursor()
        # you have to insert tables first
        sql = "SELECT * FROM %s WHERE USERNAME = %%s" %table
        # MySQL evaluates backwards, so let pymysql figure out the
        # other variables how it wants to
        db.execute(sql, (user))
        # if there is one result, the user already exists in the table
        if db.rowcount == 1:
            return True
        else:
            return False


dis = Accessor()
# print(dis.alltabs("User"))
# res = dis.alltabs("User")
# for item in res:
#     print(item)

# success = dis.createAccount("demo2","hunter8")
# ##
# success = dis.createProfile("demo2","Derrick", "Brower", "19940702", False,
#     "M", "ewbrower@gatech.edu", "182", False, 0, None)
# print(success)
# success = dis.search(123456789012,"abc",None,None,None)

success = dis.selectBook(123456789012)

print(success)







## extra room