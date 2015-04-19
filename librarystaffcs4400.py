from tkinter import *
from tkinter import ttk
import pymysql
import urllib.request
from urllib import *
from access import Accessor

class LibraryStaff:

    def __init__(self,win):
        self.StaffPage(win)
        self.a=Accessor()

    def StaffPage(self,win):
        self.Page=win
        self.Page.title('Welcome to the Library')

        Button(self.Page,text='Checkout',command=self.checkoutPage).grid(row=1,column=1)
        Button(self.Page, text='Return',command=self.ReturnBook).grid(row=1,column=2)
        Button(self.Page,text='Lost/Damaged',command=self.LostDamagedPage).grid(row=2,column=1)
        Button(self.Page,text='Reports',command=self.ReportsPage).grid(row=2,column=2)

    def checkoutPage(self):
        self.Page.withdraw()
        self.CheckOut=Toplevel()
        self.CheckOut.title('Book Checkout')

        Label(self.CheckOut,text='Issue Id').grid(row=1,column=1)
        Label(self.CheckOut,text='ISBN').grid(row=2,column=1)
        Label(self.CheckOut, text='Check out Date').grid(row=3,column=1)
        Label(self.CheckOut,text='User Name').grid(row=1, column=3)
        Label(self.CheckOut, text='Copy#').grid(row=2,column=3)
        Label(self.CheckOut, text='Estimated Return Date').grid(row=3,column=3)

        issueID=StringVar()
        ISBN=StringVar()
        CheckOut=StringVar()
        UserName=StringVar()
        Copyno=IntVar()
        ReturnDate=StringVar()

        Entry(self.CheckOut,textvariable=issueID).grid(row=1,column=2, ipadx=30)
        Entry(self.CheckOut,textvariable=ISBN, state='readonly').grid(row=2,column=2, ipadx=30)
        Entry(self.CheckOut,textvariable=CheckOut,state='readonly').grid(row=3,column=2, ipadx=30)
        Entry(self.CheckOut,textvariable=UserName,state='readonly').grid(row=1,column=4, ipadx=30)
        Entry(self.CheckOut,textvariable=Copyno,state='readonly').grid(row=2,column=4, ipadx=30)
        Entry(self.CheckOut,textvariable=ReturnDate,state='readonly').grid(row=3,column=4, ipadx=30)

        Button(self.CheckOut,text='Confirm', command=self.checkout).grid(row=6, column=1, columnspan=4, sticky=E+W)
        Button(self.CheckOut, text='Cancel', command=self.backfromcheckout).grid(row=7,column=1,columnspan=4, sticky=E+W)

    def checkout(self):
        pass

    def backfromcheckout(self):
        self.CheckOut.withdraw()
        self.Page.deiconify()

    def LostDamagedPage(self):
        self.Page.withdraw()
        self.Lost=Toplevel()
        self.Lost.title('Lost/Damaged Book')

        Label(self.Lost, text='ISBN').grid(row=1,column=1,sticky=E)
        Label(self.Lost,text='Book Copy #').grid(row=1,column=3)
        Label(self.Lost,text='Current Time').grid(row=2,column=1)

        isbn=StringVar()
        copy=IntVar()
        time=StringVar()

        Entry(self.Lost,textvariable=isbn).grid(row=1,column=2,ipadx=30)
        OptionMenu(self.Lost,copy,'1','2','3','4','5','6','7','8','9','10').grid(row=1,column=4)
        Entry(self.Lost,textvariable=time,state='readonly').grid(row=2,column=2,ipadx=20)

        Button(self.Lost,text='Look for the last user', command=self.lastuser).grid(row=3,column=1,columnspan=4,sticky=E+W)

        ttk.Separator(self.Lost, orient=HORIZONTAL).grid(row=5,column=0,columnspan=6, sticky=E+W)

        Label(self.Lost,text='Last User of the Book').grid(row=7,column=1)
        Label(self.Lost,text='Amount to be charged').grid(row=8,column=1)

        lastuser=StringVar()
        amount=StringVar()
        
        Entry(self.Lost,textvariable=lastuser,state='readonly').grid(row=7,column=2)
        Entry(self.Lost,textvariable=amount).grid(row=8,column=2)

        Button(self.Lost,text='Submit',command=self.submitchange).grid(row=9,column=4)
        Button(self.Lost,text='Cancel', command=self.cancel).grid(row=9,column=5)

    def cancel(self):
        self.Lost.withdraw()
        self.Page.deiconify()

    def lastuser(self):
        pass

    def submitchange(self):
        pass
    
    def ReturnBook(self):
        self.Page.withdraw()
        self.ReturnBook=Toplevel()
        self.ReturnBook.title("Return Book")

        Label(self.ReturnBook,text="Issue ID").grid(row=2,column=0,sticky=E)
        self.issueID=StringVar()
        e1=Entry(self.ReturnBook,textvariable=self.issueID).grid(row=2,column=1,ipadx=30)

        Label(self.ReturnBook,text="ISBN").grid(row=3,column=0,sticky=E)
        self.ISBN=StringVar()
        e2=Entry(self.ReturnBook,textvariable=self.ISBN,state='readonly').grid(row=3,column=1,ipadx=30)

        Label(self.ReturnBook,text='Return in Damaged Condition').grid(row=4,column=0,sticky=E)
        self.YN = StringVar()
        w=OptionMenu(self.ReturnBook, self.YN, "Y","N").grid(row=4,column=1)

        Label(self.ReturnBook,text='Copy Number').grid(row=3,column=2,sticky=E)
        self.copyNum = StringVar()
        e3=Entry(self.ReturnBook,textvariable=self.copyNum,state="readonly").grid(row=3,column=3,ipadx=30)

        Label(self.ReturnBook,text="User Name").grid(row=4,column=2,sticky=E)
        self.userName = StringVar()
        e4=Entry(self.ReturnBook,textvariable=self.userName,state="readonly").grid(row=4,column=3,ipadx=30)

        b1=Button(self.ReturnBook,text="Return", command=self.returnb).grid(row=5,column=3)
        b2=Button(self.ReturnBook, text='Cancel', command=self.backfromreturn).grid(row=5, column=4)

    def backfromreturn(self):
        self.ReturnBook.withdraw()
        self.Page.deiconify()

    def returnb(self):
        pass
        
    def ReportsPage(self):
        self.Page.withdraw()
        self.Reports=Toplevel()
        self.Reports.title('Reports')

        Button(self.Reports, text='Damaged Books', command=self.damagedbooks).grid(row=1,column=1)
        Button(self.Reports,text='Popular Books',command=self.popularbooks).grid(row=1,column=2)
        Button(self.Reports,text='Frequent Users',command=self.frequentusers).grid(row=2,column=1)
        Button(self.Reports,text='Popular Subject',command=self.popularsubject).grid(row=2,column=2)

        Button(self.Reports,text='Back',command=self.backfromreports).grid(row=3,column=1,columnspan=2, sticky=E+W)

    def damagedbooks(self):
        self.Reports.withdraw()
        self.Damaged=Toplevel()
        self.Damaged.title('Damaged Books Report')

        f1=Frame(self.Damaged)
        f1.grid(row=1,column=1)
        self.month=StringVar()
        self.subj1=StringVar()
        self.subj2=StringVar()
        self.subj3=StringVar()
        
        Label(f1, text='Month').grid(row=1,column=1)
        OptionMenu(f1, self.month, 'January','February','March').grid(row=1,column=2)

        
        Label(f1, text='Subject').grid(row=1,column=3)
        Label(f1, text='Subject').grid(row=2,column=3)
        Label(f1, text='Subject').grid(row=3,column=3)
        OptionMenu(f1,self.subj1,'subjects').grid(row=1,column=4)
        OptionMenu(f1,self.subj2, 'subjects').grid(row=2,column=4)
        OptionMenu(f1,self.subj3, 'subjects').grid(row=3,column=4)

        Button(f1, text='Show Report', command=self.showreport).grid(row=4,column=1,columnspan=4,sticky=E+W)
        Button(f1, text='Back', command=self.damtoreports).grid(row=5,column=1,columnspan=4, sticky=E+W)

    def damtoreports(self):
        self.Damaged.withdraw()
        self.Reports.deiconify()
        
    def showreport(self):        
        f2=Frame(self.Damaged)
        f2.grid(row=2,column=1)
        
        Label(f2, text='Month').grid(row=1,column=1)
        Label(f2, text='Subject').grid(row=1,column=2)
        Label(f2,text='#damaged books').grid(row=1,column=3)

        month=self.month.get()
        subj1=self.subj1.get()
        subj2=self.subj2.get()
        subj3=self.subj3.get()
        
        Label(f2, text=month).grid(row=3,column=1)
        Label(f2, text=subj1).grid(row=2,column=2)
        Label(f2, text=subj2).grid(row=3,column=2)
        Label(f2, text=subj3).grid(row=4,column=2)

        dam1=StringVar()
        dam2=StringVar()
        dam3=StringVar()
        #retrieve damaged books
        
        Label(f2, text=dam1).grid(row=2,column=3)
        Label(f2, text=dam2).grid(row=3,column=3)
        Label(f2, text=dam3).grid(row=4,column=3)
        
    def popularbooks(self):
        self.Reports.withdraw()
        self.Popbooks=Toplevel()
        self.Popbooks.title('Popular Books Report')

        Label(self.Popbooks, text='Month').grid(row=1,column=1)
        Label(self.Popbooks, text='Title').grid(row=1,column=2)
        Label(self.Popbooks, text='#checkouts').grid(row=1,column=3)

        
        Label(self.Popbooks, text='January').grid(row=2,column=1)
        #retrieve popular books using access - store in list
        Janlist=[['a','1'],['b','2'],['c','3']]
        Feblist=[['a','1'],['b','2'],['c','3']]
        
        i=0
        while i<len(Janlist):
            Label(self.Popbooks, text=Janlist[i][0]).grid(row=i+2, column=2)
            Label(self.Popbooks, text=Janlist[i][1]).grid(row=i+2, column=3)
            i+=1
        Label(self.Popbooks, text='February').grid(row=5, column=1)
        
        i=0
        while i<len(Feblist):
            Label(self.Popbooks, text=Feblist[i][0]).grid(row=i+5, column=2)
            Label(self.Popbooks, text=Feblist[i][1]).grid(row=i+5, column=3)
            i+=1

        Button(self.Popbooks, text='Back', command=self.popbtoreports).grid(column=1, row=15, columnspan=3,sticky=E+W)

    def popbtoreports(self):
        self.Popbooks.withdraw()
        self.Reports.deiconify()
        
    def frequentusers(self):
        self.Reports.withdraw()
        self.Freq=Toplevel()
        self.Freq.title('Frequent Users Report')

        Label(self.Freq, text='Month').grid(row=1,column=1)
        Label(self.Freq, text='User Name').grid(row=1,column=2)
        Label(self.Freq, text='#checkouts').grid(row=1,column=3)

        
        Label(self.Freq, text='January').grid(row=2,column=1)
        #retrieve frequent users using access - store in list
        Janlist=[['a','1'],['b','2'],['c','3']]
        Feblist=[['a','1'],['b','2'],['c','3']]
        
        i=0
        while i<len(Janlist):
            Label(self.Freq, text=Janlist[i][0]).grid(row=i+2, column=2)
            Label(self.Freq, text=Janlist[i][1]).grid(row=i+2, column=3)
            i+=1
        Label(self.Freq, text='February').grid(row=len(Janlist)+2, column=1)
        
        i=0
        while i<len(Feblist):
            Label(self.Freq, text=Feblist[i][0]).grid(row=i+2+len(Janlist), column=2)
            Label(self.Freq, text=Feblist[i][1]).grid(row=i+2+len(Janlist), column=3)
            i+=1
        Button(self.Freq,text='Back', command=self.freqtoreports).grid(row=20, column=1, columnspan=3, sticky=E+W)

    def freqtoreports(self):
        self.Freq.withdraw()
        self.Reports.deiconify()
        
    def popularsubject(self):
        self.Reports.withdraw()
        self.Popsub=Toplevel()
        self.Popsub.title('Popular Subject Report')

        Label(self.Popsub, text='Month').grid(row=1,column=1)
        Label(self.Popsub, text='Top Subject').grid(row=1,column=2)
        Label(self.Popsub, text='#checkouts').grid(row=1,column=3)

        
        Label(self.Popsub, text='January').grid(row=2,column=1)
        #retrieve frequent users using access - store in list
        Janlist=[['a','1'],['b','2'],['c','3']]
        Feblist=[['a','1'],['b','2'],['c','3']]
        
        i=0
        while i<len(Janlist):
            Label(self.Popsub, text=Janlist[i][0]).grid(row=i+2, column=2)
            Label(self.Popsub, text=Janlist[i][1]).grid(row=i+2, column=3)
            i+=1
        Label(self.Popsub, text='February').grid(row=len(Janlist)+2, column=1)
        
        i=0
        while i<len(Feblist):
            Label(self.Popsub, text=Feblist[i][0]).grid(row=i+2+len(Janlist), column=2)
            Label(self.Popsub, text=Feblist[i][1]).grid(row=i+2+len(Janlist), column=3)
            i+=1
        Button(self.Popsub,text='Back', command=self.subjtoreports).grid(row=20, column=1, columnspan=3, sticky=E+W)

    def subjtoreports(self):
        self.Popsub.withdraw()
        self.Reports.deiconify()

    def backfromreports(self):
        self.Reports.withdraw()
        self.Page.deiconify()

#win=Tk()
#w=LibraryStaff(win)
#win.mainloop()

