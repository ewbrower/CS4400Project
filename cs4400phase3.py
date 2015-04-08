from tkinter import *
from tkinter import ttk
import pymysql
import urllib.request
from urllib import *

class Library:

    def __init__(self,win):
        self.LoginPage(win)

    def LoginPage(self,win): #LoginPage(1)
        self.Login=win
        self.Login.title('Login')
        f1=Frame(self.Login)
        f1.pack(expand=True)
        f2=Frame(self.Login)
        f2.pack(expand=True)


        Label(f2, text='Username').grid(row=0, column=0, sticky=E)
        Label(f2, text='Password').grid(row=1, column=0, sticky=E)

        self.sv=StringVar()
        self.sv1=StringVar()

        e1=Entry(f2, textvariable=self.sv)
        e1.grid(row=0,column=1,columnspan=3,ipadx=30)
        e2=Entry(f2, textvariable=self.sv1)
        e2.grid(row=1,column=1,columnspan=3,ipadx=30)

        b1=Button(f2, text='Create Account', command=self.Register)
        b1.grid(row=2,column=4, sticky=EW)
        b2=Button(f2,text='Login', command=self.LoginCheck)
        b2.grid(row=2,column=2, sticky=EW)

    def Register(self): #NewRegistration(2)
        self.Login.withdraw()
        self.Register=Toplevel()
        self.Register.title('New User Registration')

        Label(self.Register, text='UserName').grid(row=2,column=0,sticky=W)
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


    def Connect(self):
        try:
            db = pymysql.connect(db='cs2316db', user='varinthorn3',passwd='jdTG1bLO',host='academic-mysql.cc.gatech.edu')
            return(db)
        except:
            messagebox.showerror('Error','Check internet connection!')

            
    def LoginCheck(self): #checking if information matches with database after hitting login(1)
        db =self.Connect()
        u=self.sv.get()
        p=self.sv1.get()
        sql='SELECT * FROM ReservationUser WHERE Username=%s AND Password = %s'
        c=db.cursor()
        name = c.execute(sql,(u,p))
        if name == 0:
            messagebox.showerror('Error','You have entered an unrecognizable username/password combination.')
        else:
            messagebox.showinfo('Success','You have logged in successfully.')
            self.SearchBooks()

    def RegisterNew(self): #checking if information matches with database after hitting submit(2)
        usern=self.U.get()
        usern=str(usern)
        psw1=self.P.get()
        psw2=self.CP.get()
        lastname=self.LN.get()
        l=0
        u=0
        a=0
        while a==0:
            if psw1!=psw2:
                messagebox.showerror('Error','Passwords does not match.')
                a+=1
            elif usern=='':
                messagebox.showerror('Error','Please enter username.')
                a+=1
            elif psw1 == '':
                messagebox.showerror('Error','Please enter password.')
                a+=1
            elif psw2=='':
                messagebox.showerror('Error','Please confirm password.')
                a+=1
            else:
                for i in psw1:
                    import string
                    if i in string.ascii_uppercase:
                        l+=1
                    if i in ['0','1','2','3','4','5','6','7','8','9']:
                        u+=1
                if l==0 or u==0:
                    messagebox.showerror('Error','Please enter password with at least one number and one uppercase letter.')
                    a+=1
            a+=2
        db=self.Connect()
        sql='SELECT * FROM ReservationUser WHERE Username=%s'
        c=db.cursor()
        name = c.execute(sql,usern)
        if a==2:
            if name != 0:
                    messagebox.showerror('Error', 'Username already exists, please do not use it.')
            else:
                sql='INSERT INTO ReservationUser (Username,Password,LastName) VALUE(%s,%s,%s)'
                c.execute(sql, (usern,psw1,lastname))
                db.commit()
                self.MakeProfile()
                messagebox.showinfo('Success','You are now registered.')
                
    def MakeProfile(self): #making new profile (3)
        self.Login.withdraw()
        self.makeProfile=TopLevel()
        self.makeProfile.title('Create Profile')

        self.FN=StringVar()
        self.DOB=StringVar()
        self.EMAIL=StringVar()
        self.ADDRESS=StringVar()
        self.LN=StringVar()
        self.GENDER=StringVar() #drop down?
        self.FACULTY=IntVar() #radiobutton
        self.DEPARTMENT=StringVar()

        Label(self.makeProfile, text ='First Name').grid(row=2, column = 1, sticky=E)
        Label(self.makeProfile, text ='D.O.B').grid(row=4, column = 1, sticky=E)
        Label(self.makeProfile, text ='Email').grid(row=6, column = 1, sticky=E)
        Label(self.makeProfile, text ='Address').grid(row=8, column = 1, sticky=E)
        Label(self.makeProfile, text ='Last Name').grid(row=2, column = 4, sticky=E)
        Label(self.makeProfile, text = 'Gender').grid(row=4, column = 4, sticky=E)
        Label(self.makeProfile, text ='Are you a faculty member?').grid(row=6, column = 4, sticky=E)

        e1=Entry(self.makeProfile, textvariable=self.FN)
        e1.grid(row=2,column=2, ipadx=30)
        e2=Entry(self.makeProfile, textvariable=self.DOB)
        e2.grid(row=4,column=2, ipadx=30)
        e3=Entry(self.makeProfile, textvariable=self.EMAIL)
        e3.grid(row=6,column=2, ipadx=30)
        e4=Entry(self.makeProfile, textvariable=self.ADDRESS)
        e4.grid(row=8,column=2, ipadx=30)

        e5=Entry(self.makeProfile, textvariable=self.LN)
        e5.grid(row=2,column=5, ipadx=30)
        w=OptionMenu(self.makeProfile, self.GENDER, 'male','female')
        w.grid(row=4,column=5)
        r=Radiobutton(self.makeProfile, text='Yes',variable=self.FACULTY,command=self.department)
        r.grid(row=6,column=5, ipadx=30)
        
        b2=Button(self.makeProfile, text='Submit')
        b2.grid(row=10,column=5)

    def department(self):
        Label(self.makeProfile, text ='Associated Department').grid(row=8, column = 4, sticky=E)### rendered invisible
        dep=OptionMenu(self.makeProfile,self.DEPARTMENT, 'Chemistry','Math')
        dep.grid(row=8,column=5)

    def RegisterNew(self):
        pass
        #submit SQL into database

    def SearchBooks(self):
        self.Login.withdraw()
        self.Search=Toplevel()
        self.Search.title=('Search Books')

        self.ISBN=StringVar()
        self.Title=StringVar()
        self.Author=StringVar()

        Label(self.Search, text='ISBN').grid(row=2, column =2, sticky=E)
        Label(self.Search, text='Title').grid(row=4, column =2, sticky=E)
        Label(self.Search, text='Author').grid(row=6, column =2, sticky=E)

        e1=Entry(self.Search, textvariable=self.ISBN)
        e1.grid(row=2, column = 3, ipadx=30)
        e2=Entry(self.Search, textvariable=self.Title)
        e2.grid(row=4, column = 3, ipadx=30)
        e3=Entry(self.Search, textvariable=self.Author)
        e3.grid(row=6, column = 3, ipadx=30)

        b1=Button(self.Search, text='Back')#command = go back
        b1.grid(row=8, column=2)
        b1=Button(self.Search, text='Search')#command = search SQL
        b1.grid(row=8, column=4)
        b1=Button(self.Search, text='Close')#command = close
        b1.grid(row=8, column=6)


    def RequestHold(self): #####################FIX THE BORDERS
        self.Search.withdraw()
        self.holdRequest=TopLevel()
        self.holdRequest.title=('Hold Request for a Book')

        Label(self.holdRequest, text='Books Available Summary').grid(row=1, column=1, sticky=W)
        frame=Frame(borderwidth=2, relief=RIDGE)
        frame.grid(row=2,column=1, columnspan=6)
        Label(frame, text='Select',bd=1, relief=RIDGE).grid(row=1,column=1,sticky=E+W)
        Label(frame, text='ISBN',bd=1, relief=RIDGE).grid(row=1,column=2,sticky=E+W)
        Label(frame, text='Title of the Book',bd=1, relief=RIDGE).grid(row=1,column=3,sticky=E+W)
        Label(frame, text='Edition',bd=1, relief=RIDGE).grid(row=1,column=4,sticky=E+W)
        Label(frame, text='# copies available',bd=1, relief=RIDGE).grid(row=1,column=5,sticky=E+W)

        self.BooksFound=[['isbn','title','edition','copies'],['','','','']]
        self.selected=[]
        self.var=StringVar()
        i=0
        while i<len(self.BooksFound):
            self.r=Radiobutton(frame, variable=self.var, value=self.BooksFound[i])
            self.r.deselect()
            self.r.grid(row=i+2,column=1)
            
            Label(frame,text=self.BooksFound[i][0],bd=1, relief=RIDGE).grid(row=i+2,column=2)
            Label(frame,text=self.BooksFound[i][1],bd=1, relief=RIDGE).grid(row=i+2,column=3)
            Label(frame,text=self.BooksFound[i][2],bd=1, relief=RIDGE).grid(row=i+2,column=4)
            Label(frame,text=self.BooksFound[i][3],bd=1, relief=RIDGE).grid(row=i+2,column=5)
            i+=1
        frame2=Frame()
        frame2.grid(row=3,column=1,columnspan=6)
        Label(frame2,text='Hold Request Date').pack(side=LEFT)
        holddate=StringVar()
        e1=Entry(frame2,textvariable=holddate,state='readonly')
        e1.pack(side=LEFT)
        returndate=StringVar()
        e1=Entry(frame2,textvariable=returndate,state='readonly')
        e1.pack(side=RIGHT)
        Label(frame2,text='Estimated Return Date').pack(side=RIGHT)

        Button(self.holdRequest,text='Back').grid(row=4,column=3)
        Button(self.holdRequest,text='Submit').grid(row=4,column=4)
        Button(self.holdRequest,text='Close').grid(row=4,column=5)

        ttk.Separator(self.holdRequest, orient=HORIZONTAL).grid(row=5,column=0,columnspan=6, sticky=E+W)

        Label(self.holdRequest,text='Books on Reserve').grid(row=6,column=1,sticky=W)
        self.BooksReserved=self.BooksFound
        a=0
        frame3=Frame(borderwidth=2, relief=RIDGE,bg='grey')
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

    def RequestExtension(self): 
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
        self.locate=TopLevel()
        self.locate.title=('Track Book Location')

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

