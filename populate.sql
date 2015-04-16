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
  issue_id int NOT NULL,
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
        "London, England", 2000, 2, "Boring", 200.0, 0),
    ("1-285-19614-7", "Database Systems", "Penguin", 8, "Detroit",
        2011, 1, "Computer Science", 215.0, 1);

INSERT INTO User (username, password) VALUES
    ("ewbrower", "hunter2"),
    ("pearvarin", "aaa"),
    ("diplo", "hunter2"),
    ("demoGuy", "hunter2")
    ("bbaggins", "hunter2");

INSERT INTO Student_Faculty (username, fname, lname, dob, debarred, gender,
                                email, address, faculty, penalty) VALUES
    ("ewbrower", "Eric", "Brower", "19940702", 0, "M", "ewbrower@gmail.com",
        "182", 0, 0.0),
    ("pearvarin", "Varinthorn", "Banjurkajurka", "12000101", 0, "F",
        "pear@varin", "1122", 0, 20.0),
    ("bbaggins", "Bilbo", "Baggins", "10000412", 0, "M",
        "bilbo@underhill.net", "Bag End", 0, 0.0)

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
    ("0-123-81479-0", 8, 0, 0, 0),
    ("1-285-19614-7", 1, 0, 0, 0),
    ("1-285-19614-7", 2, 0, 0, 0),
    ("1-285-19614-7", 3, 0, 0, 0);




