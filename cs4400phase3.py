from tkinter import *
from tkinter import ttk
import pymysql
import urllib.request
from urllib import *
from access import Accessor
import datetime

class Library:

    def __init__(self,win):
        self.LoginPage(win)
        self.a=Accessor()

    def LoginPage(self,win): #LoginPage(1)
        self.Login=win
        self.Login.wm_title('Login')
        f1=Frame(self.Login)
        f1.grid(column=1, row=1)
        f2=Frame(self.Login)
        f2.grid(column=1, row=2)

        Label(f2, text='Username').grid(row=0, column=0, sticky=E)
        Label(f2, text='Password').grid(row=1, column=0, sticky=E)

        self.Username=StringVar()
        self.Psw=StringVar()

        e1=Entry(f2, textvariable=self.Username)
        e1.grid(row=0,column=1,columnspan=3,ipadx=30)
        e2=Entry(f2, textvariable=self.Psw)
        e2.grid(row=1,column=1,columnspan=3,ipadx=30)

        b1=Button(f2, text='Create Account', command=self.Register)
        b1.grid(row=2,column=4, sticky=EW)
        b2=Button(f2,text='Login', command=self.LoginCheck)
        b2.grid(row=2,column=2, sticky=EW)

    def LoginCheck(self): #checking if information matches with database after hitting login(1)
        User=self.Username.get()
        Psw=self.Psw.get()
        if self.a.login(User,Psw)==True:
            messagebox.showinfo('Success','You have logged in successfully.')
            self.SearchBooks()
        else:
            messagebox.showerror('Error','You have entered an unrecognizable username/password combination.')
          
    def Register(self): #NewRegistration(2)
        self.Login.withdraw()
        self.Register=Toplevel()
        self.Register.wm_title('New User Registration')

        Label(self.Register, text='Username').grid(row=2,column=0,sticky=W)
        Label(self.Register, text='Password').grid(row=3,column=0,sticky=W)
        Label(self.Register, text='Confirm Password').grid(row=4,column=0,sticky=W)

        self.U=StringVar()
        self.P=StringVar()
        self.CP=StringVar()

        e2=Entry(self.Register, textvariable=self.U)
        e2.grid(row=2,column=1, ipadx=30)
        e3=Entry(self.Register, textvariable=self.P)
        e3.grid(row=3,column=1, ipadx=30)
        e4=Entry(self.Register, textvariable=self.CP)
        e4.grid(row=4,column=1, ipadx=30)

        b2=Button(self.Register, text='Register', command=self.RegisterNew)
        b2.grid(row=6,column=2)

    def RegisterNew(self):
        U=self.U.get()
        P=self.P.get()
        CP=self.CP.get()
        if P!=CP:
            messagebox.showerror('Error','Passwords does not match')
        elif P =='' or CP =='' or U=='':
            messagebox.showerror('Error','Please enter all information')
        else:
            if self.a.createAccount(U,P)==True:
                messagebox.showinfo('Success','You have registered successfully')
                self.MakeProfile()
            else:
                messagebox.showerror('Error','Username already exists')
      
                
    def MakeProfile(self): #making new profile (3)
        self.Register.withdraw()
        self.makeProfile=Toplevel()
        self.makeProfile.wm_title('Create Profile')

        f1=Frame(self.makeProfile)
        f1.grid(row=4,column=1, columnspan=3)
        self.FN=StringVar()
        self.month=StringVar()
        self.year=StringVar()
        self.day=StringVar()
        self.EMAIL=StringVar()
        self.ADDRESS=StringVar()
        self.LN=StringVar()
        self.GENDER=StringVar() 
        self.FACULTY=IntVar() 
        self.DEPARTMENT=StringVar()

        Label(self.makeProfile, text ='First Name').grid(row=2, column = 1, sticky=E)
        Label(f1, text ='D.O.B').grid(row=1, column = 1, sticky=E)
        Label(f1, text = '-').grid(row=1,column=3)
        Label(f1, text = '-').grid(row=1,column=5)
        Label(self.makeProfile, text ='Email').grid(row=6, column = 1, sticky=E)
        Label(self.makeProfile, text ='Address').grid(row=8, column = 1, sticky=E)
        Label(self.makeProfile, text ='Last Name').grid(row=2, column = 4, sticky=E)
        Label(self.makeProfile, text = 'Gender').grid(row=4, column = 4, sticky=E)
        Label(self.makeProfile, text ='Are you a faculty member?').grid(row=6, column = 4, sticky=E)
        
        e1=Entry(self.makeProfile, textvariable=self.FN)
        e1.grid(row=2,column=2, ipadx=30)
        mon=Entry(f1, textvariable=self.month)
        mon.grid(row=1,column=2,ipadx=5)###something is still wrong here
        day=Entry(f1, textvariable=self.day)
        day.grid(row=1,column=4, ipadx=5)
        year=Entry(f1, textvariable=self.year)
        year.grid(row=1,column=6, ipadx=12)
        e3=Entry(self.makeProfile, textvariable=self.EMAIL)
        e3.grid(row=6,column=2, ipadx=30)
        e4=Entry(self.makeProfile, textvariable=self.ADDRESS)
        e4.grid(row=8,column=2, ipadx=30)

        e5=Entry(self.makeProfile, textvariable=self.LN)
        e5.grid(row=2,column=5, ipadx=30)
        w=OptionMenu(self.makeProfile, self.GENDER, 'M','F')
        w.grid(row=4,column=5)
        r=Radiobutton(self.makeProfile, text='Yes',variable=self.FACULTY,command=self.department)
        r.grid(row=6,column=5, ipadx=30)
        
        b2=Button(self.makeProfile, text='Submit', command=self.Create)
        b2.grid(row=10,column=5)

    def department(self):
        Label(self.makeProfile, text ='Associated Department').grid(row=8, column = 4, sticky=E)### rendered invisible
        dep=OptionMenu(self.makeProfile,self.DEPARTMENT, 'Chemistry','Math','Physics', 'Biology','Architecture','Engineering','Admissions')
        dep.grid(row=8,column=5)

    def Create(self):
        U=self.U.get()
        P=self.P.get()
        FN=self.FN.get()
        month=self.month.get()
        day=self.day.get()
        year=self.year.get()
        EMAIL=self.EMAIL.get()
        ADDRESS=self.ADDRESS.get()
        LN=self.LN.get()
        GENDER=self.GENDER.get()
        FACULTY=self.FACULTY.get()
        DEPARTMENT=self.DEPARTMENT.get()
        
        if FACULTY != 'Yes':
            DEPARTMENT='NULL'
        if self.a.createProfile(U,FN,LN,str(month+'-'+day+'-'+year),'No',GENDER,EMAIL,ADDRESS,FACULTY, '0.00',DEPARTMENT)==True:
            messagebox.showinfo('Success','Profile created')
            self.BackToLogin()
        else:
            messagebox.showerror('Error','Please fill in profile again')
            
    def BackToLogin(self):
        self.makeProfile.withdraw()
        self.Login.deiconify()
        
    def SearchBooks(self):
        self.Login.withdraw()
        self.Search=Toplevel()
        self.Search.wm_title('Search Books')

        self.ISBN=StringVar()
        self.Title=StringVar()
        self.Author=StringVar()
        self.Publisher=StringVar()
        self.Edition=StringVar()

        f1=Frame(self.Search)
        f1.grid(row=1,column=1)
        f2=Frame(self.Search)
        f2.grid(row=2,column=1)
        Label(f1, text='ISBN').grid(row=2, column =2, sticky=E)
        Label(f1, text='Title').grid(row=4, column =2, sticky=E)
        Label(f1, text='Author').grid(row=6, column =2, sticky=E)
        Label(f1, text='Publisher').grid(row=2, column = 4, sticky=E)
        Label(f1, text='Edition').grid(row=4,column=4, sticky=E)

        e1=Entry(f1, textvariable=self.ISBN)
        e1.grid(row=2, column = 3, ipadx=30)
        e2=Entry(f1, textvariable=self.Title)
        e2.grid(row=4, column = 3, ipadx=30)
        e3=Entry(f1, textvariable=self.Author)
        e3.grid(row=6, column = 3, ipadx=30)
        e4=Entry(f1, textvariable=self.Publisher)
        e4.grid(row=2, column=5, ipadx=30)
        e5=Entry(f1,textvariable=self.Edition)
        e5.grid(row=4, column=5, ipadx=30)

        b1=Button(f2, text='Back',command = self.goBacktoLogin)
        b1.grid(row=1, column=1)
        b1=Button(f2, text='Menu', command=self.gotoMenu)
        b1.grid(row=1, column=2)
        b1=Button(f2, text='Search',command = self.search)
        b1.grid(row=1, column=3)
        b1=Button(f2, text='Close',command = self.close)
        b1.grid(row=1, column=4)
        
    def gotoMenu(self):
        self.Search.withdraw()
        self.Menu=Toplevel()
        self.Menu.title('Menu')

        b1=Button(self.Menu, text='Search Books', command=self.menutosearch)
        b1.grid(row=1,column=1)
        b2= Button(self.Menu, text='Request Extension', command=self.RequestExtension)
        b2.grid(row=1,column=2)
        b3=Button(self.Menu, text='Future Hold Request', command=self.FutureHoldRequest)
        b3.grid(row=2, column=1)
        b4=Button(self.Menu, text='Track Location', command=self.TrackLocation)
        b4.grid(row=2,column=2)
        b5=Button(self.Menu, text='Back', command=self.menutologin)
        b5.grid(row=3,column=1)
        b6=Button(self.Menu, text='Close', command=self.close)
        b6.grid(row=3,column=2)

    def menutosearch(self):
        self.Menu.withdraw()
        self.Login.deiconify()
        self.SearchBooks()

    def menutologin(self):
        self.Menu.withdraw()
        self.Login.deiconify()
        
    def goBacktoLogin(self):
        self.Search.withdraw()
        self.Login.deiconify()

    def close(self):
        self.Login.destroy()

    def search(self):
        ISBN=self.ISBN.get()
        TITLE=self.Title.get()
        AUTHOR=self.Author.get()
        PUBLISHER=self.Publisher.get()
        EDITION=self.Edition.get()
        if ISBN =='':
            ISBN=None
        if TITLE=='':
            TITLE=None
        if AUTHOR=='':
            AUTHOR=None
        if PUBLISHER=='':
            PUBLISHER=None
        if EDITION=='':
            EDITION=None

        data=self.a.search(ISBN, TITLE, AUTHOR, PUBLISHER, EDITION)
        newlist=[]
        
        for i in data:
            copies=self.a.getCopies(i[0])
            newlist.append([i[0],i[1],i[3],copies[0]])
        self.RequestHold(newlist)
        
    def RequestHold(self, data): #####################FIX GUI
        self.Search.withdraw()
        self.holdRequest=Toplevel()
        self.holdRequest.wm_title('Hold Request for a Book')

        Label(self.holdRequest, text='Books Available Summary').grid(row=1, column=1, sticky=W)
        frame=Frame(self.holdRequest,borderwidth=2, background='black')
        frame.grid(row=2,column=1, columnspan=6)
        Label(frame, text='Select',width=5).grid(row=1,column=1,sticky=E+W,ipadx=1)
        Label(frame, text='ISBN',width=10).grid(row=1,column=2,sticky=E+W, ipadx=1)
        Label(frame, text='Title of the Book',width=40).grid(row=1,column=3,sticky=E+W,ipadx=1)
        Label(frame, text='Edition',width=5).grid(row=1,column=4,sticky=E+W,ipadx=1)
        Label(frame, text='# copies available',width=10).grid(row=1,column=5,sticky=E+W, ipadx=1)

        self.BooksFound=data
        print(data)
        self.selected=[]
        self.var=StringVar()
        i=0
        while i<len(self.BooksFound):
            self.r=Radiobutton(frame, variable=self.var, value=self.BooksFound[i])
            self.r.deselect()
            self.r.grid(row=i+2,column=1)
            Label(frame,text=self.BooksFound[i][0],width=10).grid(row=i+2,column=2, ipadx=1)
            Label(frame,text=self.BooksFound[i][1],width=40).grid(row=i+2,column=3, ipadx=1)
            Label(frame,text=self.BooksFound[i][2],width=5).grid(row=i+2,column=4, ipadx=1)
            Label(frame,text=self.BooksFound[i][3],width=5).grid(row=i+2,column=5, ipadx=1)
            i+=1
        frame2=Frame(self.holdRequest)
        frame2.grid(row=3,column=1,columnspan=6)
        Label(frame2,text='Hold Request Date').pack(side=LEFT)
        holddate=StringVar()
        date=datetime.datetime.now().strftime('%m')+'/'+datetime.datetime.now().strftime('%d')+'/'+datetime.datetime.now().strftime('%Y')
        holddate.set(date)
        e1=Entry(frame2,textvariable=holddate,state='readonly')
        e1.pack(side=LEFT)
        returndate=StringVar()
        e1=Entry(frame2,textvariable=returndate,state='readonly')
        e1.pack(side=RIGHT)
        Label(frame2,text='Estimated Return Date').pack(side=RIGHT)

        Button(self.holdRequest,text='Back', command=self.returntoSearch).grid(row=4,column=3)
        Button(self.holdRequest,text='Submit', command=self.holdrequest).grid(row=4,column=4)
        Button(self.holdRequest,text='Close', command=self.close).grid(row=4,column=5)

        ttk.Separator(self.holdRequest, orient=HORIZONTAL).grid(row=5,column=0,columnspan=6, sticky=E+W)

        Label(self.holdRequest,text='Books on Reserve').grid(row=6,column=1,sticky=W)
        self.BooksReserved=self.BooksFound
        a=0
        frame3=Frame(self.holdRequest,borderwidth=2, relief=RIDGE,bg='grey')
        frame3.grid(row=7,column=1, columnspan=6)
        Label(frame3, text='ISBN',bd=1, relief=RIDGE,bg='grey').grid(row=1,column=1,sticky=E+W)
        Label(frame3, text='Title of the Book',bd=1, relief=RIDGE,bg='grey').grid(row=1,column=2,sticky=E+W)
        Label(frame3, text='Edition',bd=1, relief=RIDGE,bg='grey').grid(row=1,column=3,sticky=E+W)
        Label(frame3, text='# copies available',bd=1, relief=RIDGE,bg='grey').grid(row=1,column=4,sticky=E+W)

        while a<len(self.BooksReserved):
            Label(frame3,text=self.BooksReserved[a][0],bd=1, relief=RIDGE,bg='grey').grid(row=a+2,column=1)
            Label(frame3,text=self.BooksReserved[a][1],bd=1, relief=RIDGE,bg='grey').grid(row=a+2,column=2)
            Label(frame3,text=self.BooksReserved[a][2],bd=1, relief=RIDGE,bg='grey').grid(row=a+2,column=3)
            Label(frame3,text=self.BooksReserved[a][3],bd=1, relief=RIDGE,bg='grey').grid(row=a+2,column=4)
            a+=1

    def returntoSearch(self):
        self.holdRequest.withdraw()
        self.Search.deiconify()


    def holdrequest(self):
        booktohold=self.var

    def RequestExtension(self):
        self.Menu.withdraw()
        self.RequestExtension=Toplevel()
        self.RequestExtension.title('Request extension on a book')

        #need to add in the logic to check the issue ID and then unlock the text entries

        Label(self.RequestExtension, text='Enter your issue_id').grid(row=2, column=0, sticky=E)
        self.issueID = StringVar()
        e1=Entry(self.RequestExtension, textvariable=self.issueID).grid(row=2,column=1,ipadx=30)        
        b1=Button(self.RequestExtension, text='Submit').grid(row=2,column=4)
        ttk.Separator(self.RequestExtension,orient=HORIZONTAL).grid(row=3,column=0,columnspan=6,sticky="EW")

        Label(self.RequestExtension, text='Original Checkout Date').grid(row=4,column=0,sticky=E)
        self.checkoutDate = StringVar()
        e2=Entry(self.RequestExtension, textvariable=self.checkoutDate,state="readonly")
        e2.grid(row=4,column=1,ipadx=30)
        
        Label(self.RequestExtension, text='Current Extension Date').grid(row=5,column=0,sticky=E)
        self.currentExtension = StringVar()
        e3=Entry(self.RequestExtension, textvariable=self.currentExtension,state='readonly')
        e3.grid(row=5,column=1,ipadx=30)
        
        Label(self.RequestExtension, text='New Extension Date').grid(row=6,column=0,sticky=E)
        self.newExtension = StringVar()
        e4=Entry(self.RequestExtension,textvariable=self.newExtension,state='readonly')
        e4.grid(row=6,column=1,ipadx=30)

        Label(self.RequestExtension, text='Current Return Date').grid(row=5,column=4,sticky=E)
        self.returnDate=StringVar()
        e5=Entry(self.RequestExtension,textvariable=self.returnDate,state='readonly')
        e5.grid(row=5,column=5,ipadx=30)

        Label(self.RequestExtension, text='New Estimated Return Date').grid(row=6,column=4,sticky=E)
        self.newReturnDate = StringVar()
        e6=Entry(self.RequestExtension,textvariable=self.newReturnDate,state='readonly')
        e6.grid(row=6,column=5,ipadx=30)

        b2=Button(self.RequestExtension,text='Submit').grid(row=7,column=5)

    def FutureHoldRequest(self):
        self.Menu.withdraw()
        self.FutureHoldRequest=Toplevel()
        self.FutureHoldRequest.title("Future Hold Request for a Book")

        Label(self.FutureHoldRequest,text="ISBN").grid(row=2,column=0,sticky=E)
        self.ISBN = StringVar()
        e1=Entry(self.FutureHoldRequest,textvariable=self.ISBN).grid(row=2,column=1,ipadx=30)
        b1=Button(self.FutureHoldRequest,text='Request').grid(row=2,column=3)
        ttk.Separator(self.FutureHoldRequest,orient=HORIZONTAL).grid(row=3,column=0,columnspan=4,sticky="EW")

        Label(self.FutureHoldRequest,text='Copy Number').grid(row=4,column=0,sticky=E)
        self.copyNum = StringVar()
        e2=Entry(self.FutureHoldRequest,textvariable=self.copyNum,state="readonly").grid(row=4,column=1,ipadx=30)

        Label(self.FutureHoldRequest,text="Expected Available Date").grid(row=5,column=0,sticky=E)
        self.expectedAvailable = StringVar()
        e3=Entry(self.FutureHoldRequest,textvariable=self.expectedAvailable,state="readonly").grid(row=5,column=1,ipadx=30)

        b2=Button(self.FutureHoldRequest,text="OK").grid(row=6,column=1,sticky=E)



    def TrackLocation(self):
        self.Menu.withdraw()
        self.locate=TopLevel()
        self.locate.title('Track Book Location')

        Label(self.locate,text='ISBN').grid(row=1,column=1)
        isbn=StringVar()
        Entry(self.locate,textvariable=isbn).grid(row=1,column=2,ipadx=30)
        Button(self.locate,text='Locate').grid(row=1,column=3)

        ttk.Separator(self.locate, orient=HORIZONTAL).grid(row=3,column=0,columnspan=6, sticky=E+W)

        Label(self.locate,text='Floor Number').grid(row=5, column=1)
        Label(self.locate,text='Aisle Number').grid(row=6,column=1)
        Label(self.locate,text='Shelf Number').grid(row=5,column=3)
        Label(self.locate,text='Subject').grid(row=6,column=3)

        floorno=IntVar()
        aisleno=IntVar()
        shelfno=IntVar()
        subj=StringVar()

        Entry(self.locate,textvariable=floorno, state='readonly').grid(row=5,column=2, ipadx=20)
        Entry(self.locate,textvariable=aisleno,state='readonly').grid(row=6,column=2, ipadx=20)
        Entry(self.locate,textvariable=shelfno,state='readonly').grid(row=5,column=4, ipadx=20)
        Entry(self.locate,textvariable=subj,state='readonly').grid(row=6,column=4, ipadx=20)
        
        

win=Tk()
w=Library(win)
win.mainloop()
