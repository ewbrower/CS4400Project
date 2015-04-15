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
    ("demoGuy", "hunter2");

INSERT INTO Student_Faculty (username, fname, lname, dob, debarred, gender,
                                email, address, faculty, penalty) VALUES
    ("ewbrower", "Eric", "Brower", "19940702", 0, "M", "ewbrower@gmail.com",
        "182", 0, 0.0),
    ("pearvarin", "Varinthorn", "Banjurkajurka", "12000101", 0, "F",
        "pear@varin", "1122", 0, 20.0);

INSERT INTO Book_Copy (ISBN, copy_num, hold, damaged, checked_out) VALUES
    ("0-136-08620-9", 1, 0, 0, 0),
    ("0-123-81479-0", 1, 0, 0, 0),
    ("0-123-81479-0", 2, 0, 0, 0),
    ("0-123-81479-0", 3, 0, 0, 0),
    ("0-123-81479-0", 4, 0, 0, 0),
    ("1-285-19614-7", 1, 0, 0, 0),
    ("1-285-19614-7", 2, 0, 0, 0),
    ("1-285-19614-7", 3, 0, 0, 0);