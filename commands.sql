-- CREATE Statements --
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

-- Login Form --
-- check username

SELECT *
FROM USER
WHERE username = $username;

-- New User Registration --
-- check existing usernames

SELECT *
FROM USER
WHERE username = $username;

-- add user

INSERT INTO USER
VALUES ($username,
        $password);

-- Make Profile --

INSERT INTO Student_Faculty
VALUES ($fname,
        $lname,
        $dob,
        $debarred,
        $gender,
        $email,
        $address,
        $faculty_bool,
        $penalty,
        $dept);

-- Search Books --

SELECT *
FROM Book
WHERE ISBN = $ISBN 
AND publisher = $publisher 
AND title = $title 
AND edition = $edition 
AND author = $author;

-- search for books by author

SELECT *
FROM Author
WHERE ISBN = $ISBN
AND author = $author;

-- Request Hold --
UPDATE Book_Copy
SET hold= 1
WHERE ISBN = "0-136-08620-9" AND hold = 0 AND damaged = 0 AND checked_out = 0
LIMIT 1;


INSERT INTO Issues
VALUES(
	$issue_id, 
	$username,
	$issue_date, 
	$extension_date,
	0,
	$copy_num,
	return_date,
	$ISBN);
	
	
-- Future Hold Request --

SELECT copy_num
FROM Book_Copy
WHERE ISBN = $ISBN AND checked_out = FALSE AND damaged = FALSE;

-- since the above set is null (because we are looking for available books),
-- then select closest return date

SELECT copy_num, return_date,
  (SELECT c.copy_num
    FROM Book_Copy c
    WHERE future_requester=null) as free_copy
  FROM Issues i
  WHERE i.copy_num = c.copy_num AND ISBN = $ISBN
  ORDER BY return_date;

 -- then create new hold request on the most recent

UPDATE Book_Copy
SET future_requester=$username
WHERE copy_num = $copy_num;

-- Track Location --

SELECT shelf,
       subject,
       (SELECT aisle
        FROM Shelf s
        WHERE s.shelf=b.shelf),
       (SELECT floor
        FROM Subject u
        WHERE u.name=b.subject)
FROM Book b
WHERE ISBN = $ISBN;

-- Checkout --

SELECT *
FROM Book_Copy
WHERE ISBN = $ISBN
  AND copy_num = $copy_num
  AND damaged = FALSE;

SELECT *
FROM USER
WHERE username = $username;

UPDATE Book_Copy
SET checked_out = TRUE
	AND hold = FALSE
WHERE ISBN = $ISBN
  AND copy_num = $copy_num;

  
UPDATE Issues
SET return_date = $return_date WHERE issue_id = $issue_id;

INSERT INTO Issues
VALUES(
  $issue_id,
  $username,
  $issue_date,
  $extension_date,
  $extension_count,
  $copy_num,
  $return_date,
  $ISBN);

-- Return Book --

UPDATE Book_Copy
SET checked_out = FALSE 
	AND damaged=  FALSE
WHERE ISBN = $ISBN
  AND copy_num = $copy_num;

SELECT cost
FROM Book
WHERE ISBN = $data;

-- Damaged --

UPDATE Book_Copy
SET damaged = TRUE
WHERE ISBN = $data
  AND copy_num = $data;

UPDATE Student_Faculty
SET penalty = penalty + $cost
WHERE username = $username;

-- Lost --

DELETE
FROM Book_Copy
WHERE ISBN = $data
  AND copy_num = $data;

-- Damaged Report --

-- SELECT count(*),
--   c.return_date,
--   (SELECT subject
--     FROM Book b
--     WHERE b.ISBN = c.ISBN)
-- FROM Book_Copy c
-- WHERE damaged = TRUE;

SELECT count(*) FROM Book_Copy WHERE damaged = TRUE
JOIN (ISBN)
SELECT subject FROM Book
JOIN (ISBN)
SELECT return_date FROM Issues;

SELECT DISTINCT count(*), b.subject, MONTH(i.return_date) as month
FROM Book_Copy AS c
JOIN Book AS b ON c.ISBN = b.ISBN
JOIN Issues AS i ON c.ISBN = i.ISBN
WHERE c.damaged = 1
GROUP BY month;

SELECT subject, (SELECT count(*) FROM Book_Copy WHERE damaged = 1 AND ISBN = b.ISBN)
FROM Book AS b
GROUP BY b.subject;

SELECT subject, (select * from Book_Copy WHERE ISBN = b.ISBN)
FROM Book AS b;

SELECT b.subject, c.ISBN, c.copy_num, c.damaged FROM Book AS b
INNER JOIN Book_Copy AS c ON c.ISBN = b.ISBN
INNER JOIN Issues AS i ON c.ISBN = i.ISBN
WHERE c.damaged = 1;

SELECT c.copy_num, (
    SELECT ISBN, (
      SELECT MAX(return_date) FROM Issues WHERE ISBN = b.ISBN
      )
    FROM Book AS b
    WHERE ISBN = c.ISBN
  )
FROM Book_Copy AS c
WHERE c.damaged = 1;

SELECT i.return_date, c.ISBN, c.copy_num
FROM Book_Copy AS c
INNER JOIN Issues AS i ON i.copy_num = c.copy_num AND i.ISBN = c.ISBN
WHERE c.damaged = 1;

SELECT i.return_date, c.ISBN, c.copy_num
FROM Issues AS i
INNER JOIN Book_Copy AS c ON i.copy_num = c.copy_num AND i.ISBN = c.ISBN
WHERE c.damaged = 1;


SELECT c.ISBN, b.subject (
  SELECT MAX(return_date) FROM Issues AS i
  WHERE i.ISBN = c.ISBN AND i.copy_num = c.copy_num
) AS LastDate
FROM Book_Copy AS c
INNER JOIN Book AS b ON b.ISBN = c.ISBN
WHERE c.damaged = 1;

-- V this one actually works
SELECT c.ISBN, b.subject, (
  SELECT MAX(return_date) FROM Issues AS i
  WHERE i.ISBN = c.ISBN AND i.copy_num = c.copy_num
) AS LastDate
FROM Book_Copy AS c
INNER JOIN Book AS b ON b.ISBN = c.ISBN
WHERE c.damaged = 1;

-- INNER JOIN Book_Copy AS c ON b.ISBN = c.ISBN

-- Popular Report --

SELECT name,
       b.copy_num,
  (SELECT count(*)
   FROM Issues i
   WHERE i.copy_num = b.copy_num
    AND MONTH(i.issue_date) = $month) AS copies 
FROM Book b
ORDER BY copies DESC LIMIT 10;

-- Frequent Users Report --

SELECT lname,
       fname,
  (SELECT count(*)
   FROM Issues i
   WHERE i.username = u.username
    AND MONTH(i.issue_date) = $month) AS users
FROM USER
ORDER BY users DESC LIMIT 5;

-- Popular Subjects Report --

SELECT s.name,
  (SELECT
     (SELECT count(*)
      FROM Issues i
      WHERE i.copy_num = b.copy_num
        AND MONTH(i.issue_date) = $month) AS copies
   FROM Book b
   WHERE s.subject = b.subject)
FROM Subject s
ORDER BY copies DESC LIMIT 10;

