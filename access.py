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
            # need a lot more value verifying here !!!!!!
            db.execute(
                "INSERT INTO Student_Faculty VALUES "
                + "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (str(user), str(fname), str(lname), str(dob), str(debarred), str(gender), str(email), str(address),
                    str(faculty), str(penalty), str(dept)))
            return True
        return False


    def search(self, ISBN = None, publisher = None, title = None,
        edition = None, author = None):
        db = self.db.cursor()
        # if author !None, then search the Author database first
        if author != None and ISBN != None:
            sql = "SELECT * FROM Author WHERE ISBN = %s AND author = %s"
            db.execute(sql, (ISBN, author))
            return db
        else:
            return False

    def selectBook(self, ISBN, copy = -1):
        #if copy = -1, then copy number doesn't matter
        pass

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

# success = dis.createAccount("ewbrower","hunter8")
##
# success = dis.createProfile("ewbrower","Eric", "Brower", "19940702", False,
#     "M", "ewbrower@gatech.edu", "182", False, 0, None)
success = dis.search("100",None,None,None,"Bilbo")




print(success)







## extra room