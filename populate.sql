CREATE TABLE User(
  username varchar(50) NOT NULL,
  password varchar(50) NOT NULL,
  PRIMARY KEY(username));

CREATE TABLE Staff(
  username varchar(50) NOT NULL,
  PRIMARY KEY(username),
  FOREIGN KEY(username) REFERENCES User(username));

CREATE TABLE Student_Faculty(
  username varchar(50) NOT NULL,
  fname varchar(50) NOT NULL,
  lname varchar(50) NOT NULL,
  dob date NOT NULL,
  debarred tinyint(1) NOT NULL, 
  gender char(1) NOT NULL,
  email varchar(50) NOT NULL,
  address varchar(50) NOT NULL,
  faculty tinyint(1) NOT NULL,
  penalty decimal NOT NULL,
  dept varchar(50) NULL,
  PRIMARY KEY(username),
  FOREIGN KEY(username) REFERENCES User(username));

CREATE TABLE Book(
  ISBN varchar(13) NOT NULL,
  title varchar(50) NOT NULL,
  publisher varchar(50) NOT NULL,
  edition int NOT NULL, 
  publication_place varchar(50) NOT NULL,
  copyright int NOT NULL,
  shelf int NOT NULL,
  subject varchar(50) NOT NULL,
  cost decimal NOT NULL, 
  reserve tinyint(1) NOT NULL,
  PRIMARY KEY (ISBN),
  FOREIGN KEY (shelf) REFERENCES Shelf(shelf),
  FOREIGN KEY (subject) REFERENCES Subject(name));

CREATE TABLE Author(
  ISBN varchar(13) NOT NULL,
  author varchar(50) NOT NULL,
  PRIMARY KEY(ISBN, author),
  FOREIGN KEY(ISBN) REFERENCES Book(ISBN));

CREATE TABLE Issues(
  username varchar(50) NOT NULL,
  issue_id int NOT NULL AUTO_INCREMENT,
  issue_date date NOT NULL,
  extension_date date NULL,
  extension_count int NOT NULL,
  copy_num int NOT NULL,
  return_date date NOT NULL,
  ISBN varchar(13) NOT NULL,
  PRIMARY KEY(issue_id),
  FOREIGN KEY(username) REFERENCES Student_Faculty(username),
  FOREIGN KEY(ISBN, copy_num) REFERENCES Book_Copy(ISBN, copy_num),
  FOREIGN KEY(ISBN) REFERENCES Book_Copy(ISBN));
  
CREATE TABLE Book_Copy(
  ISBN char(13) NOT NULL,
  copy_num int NOT NULL,
  hold tinyint(1) NOT NULL,
  damaged tinyint(1) NOT NULL,
  checked_out tinyint(1) NOT NULL,
  future_requester varchar(50) NULL,
  PRIMARY KEY (ISBN, copy_num),
  FOREIGN KEY (ISBN) REFERENCES Book(ISBN));
  
CREATE TABLE Keyword(
  subject varchar(50) NOT NULL,
  keyword varchar(50) NOT NULL,
  PRIMARY KEY (subject, keyword),
  FOREIGN KEY (subject) REFERENCES Subject(name));
  
CREATE TABLE Subject(
  name varchar(50) NOT NULL,
  journals int NOT NULL,
  floor int NOT NULL,
  PRIMARY KEY (name),
  FOREIGN KEY (floor) REFERENCES Floor(floor));

CREATE TABLE Floor(
  floor int NOT NULL,
  student_assistants int NOT NULL,
  copiers int NOT NULL,
  PRIMARY KEY (floor));

CREATE TABLE Shelf(
  floor int NOT NULL,
  shelf int NOT NULL,
  aisle int NOT NULL,
  PRIMARY KEY (floor, shelf),
  FOREIGN KEY (floor) REFERENCES Floor(floor));

INSERT INTO Book (ISBN, title, publisher, edition, publication_place, 
                    copyright, shelf, subject, cost, reserve) VALUES
    ("0-136-08620-9", "Fundamentals of Database Systems", "Penguin", 1,
        "New York", 2012, 1, "Boring", 230.0, 0),
    ("0-123-81479-0", "Database Mining: Concepts & Techniques", "Aardvark", 6,
        "London", 2000, 2, "Boring", 200.0, 0),
    ("0-132-56870-5", "Engineering Computation with MATLAB", "Prentice Hall", 3, 
        "Upper Saddle River", 2012, 1, "Computer Science", 120, 0),
    ("1-285-19614-7", "Database Systems", "Penguin", 8, "Detroit", 
        2011, 1, "Computer Science", 215.0, 1),
    ("1-435-13211-4", "The Count of Monte Cristo", "Barnes & Noble", 1, 
        "New York", 2011, 3, "Fiction", 25, 1),
    ("0-553-59354-4", "The Bourne Identity", "Penguin", 1, 
        "New York", 2010, 3, "Fiction", 20, 0),
    ("0-140-44430-0","Les Misérables", "Penguin", 1, 
        "New York", 1982, 3, "Fiction", 15, 0),
    ("0-131-67995-3", "Discrete Mathematics with Graph Theory", "Pearson", 3, 
        "New York", 2005, 4, "Mathematics", 145, 0),
    ("0-321-88407-8", "Thomas' Calculus: Early Transcendentals" "Pearson", 13, 
        "New York", 2013, 4, "Mathematics", 200, 0),
    ("0-321-38517-9", "Linear Algebra and Its Applications", "Pearson", 4, 
        "New York", 2011, 4, "Mathematics", 150, 0),

INSERT INTO Author (ISBN, author) VALUES
    ("0-136-08620-9", "Addison Wesley"),
    ("0-123-81479-0", "Jiawei Han"),
    ("0-123-81479-0", "Micheline Kamber"), #this is a double one
    ("0-132-56870-5", "David Smith"),
    ("1-285-19614-7", "Coronel"),
    ("1-285-19614-7", "Morris"), #the second multiple authors
    ("1-435-13211-4", "Alexander Dumas"),
    ("0-553-59354-4", "Robert Ludlum"),
    ("0-140-44430-0", "Victor Hugo"),
    ("0-131-67995-3", "Edgar Goodaire"),
    ("0-321-88407-8", "George Thomas"),
    ("0-321-38517-9", "David Lay");
    
INSERT INTO User (username, password) VALUES
    ("ewbrower", "a"),
    ("pearvarin", "b"),
    ("hasquith", "c"),
    ("bbaggins", "d"),
    ("fbaggins", "e"),
    ("sgamgee", "f"),
    ("ptook", "g"),
    ("aundomiel", "h"),
    ("swhite", "i"),
    ("gwhite", "j"),
    ("gsmeagol", "k"),
    ("lgreenleaf", "l"),
    ("astrider", "m"),
    ("gdwarf", "n"),
    ("dsauron", "o"),
    ("bmussolini", "p"),
    ("wchurchill", "q"),
    ("cdegaulle", "r"),
    ("froosevelt", "s"),
    ("tstauning", "t");

INSERT INTO Staff (username) VALUES
  ("hclinton"),
  ("jbush");

INSERT INTO Student_Faculty (username, fname, lname, dob, debarred, gender,
                                email, address, faculty, penalty) VALUES
    ("ewbrower", "Eric", "Brower", "19940702", 0, "M", "ewbrower@gmail.com",
        "182", 0, 0.0),
    ("pearvarin", "Varinthorn", "Banjurkajurka", "12000101", 0, "F",
        "pear@varin", "1122", 0, 20.0),
    ("hasquith", "Hayden", "Asquith", "19910827", 0, "M", 
        "hasquith@gmail.com", "436", 0, 0.0),
    ("bbaggins", "Bilbo", "Baggins", "10000412", 0, "M",
        "bilbo@underhill.net", "Bag End", 0, 0.0),
    ("fbaggins", "Frodo", "Baggins", "19870923", 0, "M", 
        "fbaggins@gmail.com", "Shire 1", 0, 0.0),
    ("sgamgee", "Samwise", "Gamgee", "19870815", 0, "M", 
        "sgamgee@gmail.com", "Shire 2", 0, 0.0),
    ("ptook", "Pippin", "Took", "19911104", 0, "M", 
        "ptook@gmail.com", "Shire 3", 0, 0.0),
    ("aundomiel", "Arwen", "Undómiel", "19410924", 0, "F", 
        "aundomiel@gmail.com", "Rivendell", 0, 0.0),
    ("swhite", "Saruman", "White", "19600401", 0, "M", 
        "swhite@gmail.com", "Mordor", 0, 0.0),
    ("gwhite", "Gandalf", "White", "19600402", 0, "M", 
        "gwhite@gmail.com", "Valinor", 0, 0.0),
    ("gsmeagol", "Gollum", "Smeagol", "19701225", 1, "M", 
        "gsmeagol@gmailcom", "Riddle River", 0, 150.0),
    ("lgreenleaf", "Legolas", "Greenleaf","19001122", 0, "M",
        "lgreenleaf@gmail.com", "Mirkwood", 0, 0.0)
    ("astrider", "Aragorn", "Strider", "19910826", 0, "M",
        "astrider@gmail.com", "Rivendell 2", 0, 0.0)
    ("gdwarf", "Gimli", "Dwarf", "19280718", 0, "M",
        "gdwarf@gmail.com", "Moria", 0, 0.0),
    ("dsauron", "Dark", "Sauron", "18870127", 1, "M",
        "dsauron@gmail.com", "Mordor", 0, 120.0)
    ("bmussolini", "Benito", "Mussolini", "18830729", 0, "M", 
        "bmussolini@gmail.com", "6", 1, 0.0),
    ("wchurchill", "Winston", "Churchill", "18741130", 0, "M", 
        "wchurchill@gmail.com", "7", 1, 0.0),
    ("cdegaulle", "Charles", "de Gaulle", "18901122", 0, "M", 
        "cdegaulle@gmail.com", "77", 1, 0.0),
    ("froosevelt", "Franklin", "Roosevelt", "18820130", 0, "M", 
        "froosevelt@gmail.com", "777", 1, 0.0),
    ("tstauning", "Thorvald", "Stauning", "18731026", 0, "M", 
        "tstauning@gmail.com", "7777", 1, 0.0);
  
INSERT INTO Book_Copy (ISBN, copy_num, hold, damaged, checked_out) VALUES
    ("0-136-08620-9", 1, 0, 0, 0),
    ("0-136-08620-9", 2, 0, 0, 0),
    ("0-136-08620-9", 3, 0, 0, 0),
    ("0-123-81479-0", 1, 0, 0, 0),
    ("0-123-81479-0", 2, 0, 0, 0),
    ("0-123-81479-0", 3, 0, 0, 0),
    ("0-123-81479-0", 4, 0, 0, 0),
    ("0-123-81479-0", 5, 0, 0, 0),
    ("0-123-81479-0", 6, 0, 0, 0),
    ("0-123-81479-0", 7, 0, 0, 0),
    ("0-132-56870-5", 1, 0, 0, 0),
    ("0-132-56870-5", 2, 0, 0, 0),
    ("0-132-56870-5", 3, 0, 0, 0),
    ("1-285-19614-7", 1, 0, 0, 0),
    ("1-285-19614-7", 2, 0, 0, 0),
    ("1-285-19614-7", 3, 0, 0, 0),
    ("1-435-13211-4", 1, 0, 0, 0),
    ("1-435-13211-4", 2, 0, 0, 0),
    ("1-435-13211-4", 3, 0, 0, 0),
    ("1-435-13211-4", 4, 0, 0, 0),
    ("1-435-13211-4", 5, 0, 0, 0),
    ("1-435-13211-4", 6, 0, 0, 0),
    ("1-435-13211-4", 7, 0, 0, 0),
    ("0-553-59354-4", 1, 0, 0, 0),
    ("0-553-59354-4", 2, 0, 0, 0),
    ("0-553-59354-4", 3, 0, 0, 0),
    ("0-553-59354-4", 4, 0, 0, 0),
    ("0-553-59354-4", 5, 0, 0, 0),
    ("0-553-59354-4", 6, 0, 0, 0),
    ("0-553-59354-4", 7, 0, 0, 0),
    ("0-140-44430-0", 1, 0, 0, 0),
    ("0-140-44430-0", 2, 0, 0, 0),
    ("0-131-67995-3", 1, 0, 0, 0),
    ("0-131-67995-3", 2, 0, 0, 0),
    ("0-321-88407-8", 1, 0, 0, 0),
    ("0-321-38517-9", 1, 0, 0, 0),
    ("0-321-38517-9", 2, 0, 0, 0),
    ("0-321-38517-9", 3, 0, 0, 0),
    ("0-321-38517-9", 4, 0, 0, 0);
