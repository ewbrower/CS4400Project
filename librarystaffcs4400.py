from tkinter import *
from tkinter import ttk
import pymysql
import urllib.request
from urllib import *

class Library:

    def __init__(self,win):
        self.StaffPage(win)

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

        Button(self.CheckOut,text='Confirm').grid(row=6, column=1, columnspan=4, sticky=E+W)

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

        Button(self.Lost,text='Look for the last user').grid(row=3,column=1,columnspan=4,sticky=E+W)

        ttk.Separator(self.Lost, orient=HORIZONTAL).grid(row=5,column=0,columnspan=6, sticky=E+W)

        Label(self.Lost,text='Last User of the Book').grid(row=7,column=1)
        Label(self.Lost,text='Amount to be charged').grid(row=8,column=1)

        lastuser=StringVar()
        amount=StringVar()
        
        Entry(self.Lost,textvariable=lastuser,state='readonly').grid(row=7,column=2)
        Entry(self.Lost,textvariable=amount).grid(row=8,column=2)

        Button(self.Lost,text='Submit').grid(row=9,column=4)
        Button(self.Lost,text='Cancel').grid(row=9,column=5)

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

        b1=Button(self.ReturnBook,text="Return").grid(row=5,column=3)
        
    def ReportsPage(self):
        pass

win=Tk()
w=Library(win)
win.mainloop()

