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
SELECT count(c.ISBN), b.subject, (
  SELECT MONTH(MAX(return_date)) FROM Issues AS i
  WHERE i.ISBN = c.ISBN AND i.copy_num = c.copy_num
) AS LastDate
FROM Book_Copy AS c
INNER JOIN Book AS b ON b.ISBN = c.ISBN
WHERE c.damaged = 1
GROUP BY LastDate, b.subject;

-- Popular Report --
SELECT MONTH(i.issue_date), b.title, COUNT(i.issue_id)
FROM Issues AS i
INNER JOIN Book AS b ON i.ISBN=b.ISBN
WHERE MONTH(i.issue_date)=$month
GROUP BY MONTH(i.issue_date), b.title
<<<<<<< HEAD
ORDER BY COUNT(i.issue_id) DESC LIMIT 3
=======
ORDER BY COUNT(i.issue_id) DESC LIMIT 3;
-- how to do limit 3 per group?
>>>>>>> c6c21a7554097543fdc9b78d257f02c3aa7c0670

-- Amol

-- Frequent Users Report --
SELECT MONTH( i.issue_date ) , s.fname, s.lname, COUNT( i.issue_id ) 
FROM Issues AS i
INNER JOIN Student_Faculty AS s ON s.username = i.username
WHERE MONTH(i.issue_date)=$month
GROUP BY MONTH( i.issue_date ) , s.username
HAVING COUNT(i.issue_id)>10
ORDER BY COUNT( i.issue_id ) DESC 
LIMIT 5

-- Popular Subjects Report --
SELECT MONTH(i.issue_date), b.subject, COUNT(i.issue_id)
FROM Issues AS i
INNER JOIN Book AS b ON i.ISBN=b.ISBN
WHERE MONTH(i.issue_date)=$month
GROUP BY MONTH(i.issue_date), b.subject
ORDER BY COUNT(i.issue_id) DESC LIMIT 3





-- more shit

SELECT b.ISBN, (
  SELECT count(*)
  FROM Book_Copy AS c
  WHERE c.checked_out = 0 AND b.ISBN = c.ISBN) AS Count
FROM Book AS b;

SELECT b.ISBN, (
  SELECT count(*)
  FROM Book_Copy AS c
  WHERE c.future_requester IS NOT NULL AND b.ISBN = c.ISBN) AS Count
FROM Book AS b;

SELECT b.title, i.issue_id, b.ISBN, c.copy_num, i.return_date
FROM Book AS b
INNER JOIN Book_Copy AS c ON b.ISBN = c.ISBN
INNER JOIN Issues AS i ON i.ISBN = b.ISBN AND c.copy_num = i.copy_num
ORDER BY i.issue_id;

SELECT b.title, b.ISBN
FROM Book AS b
INNER JOIN Book_Copy AS c
WHERE b.ISBN = c.ISBN AND c.checked_out = 1;

-- SELECT c.copy_num, i.return_date 
-- FROM Book_Copy AS c, Issues AS i
-- WHERE c.checked_out = 0
-- AND i.return_date > CURDATE()
-- AND c.ISBN = "0-553-59354-4" 
-- ORDER BY i.return_date LIMIT 1;

SELECT c.copy_num, i.return_date
FROM Book_Copy AS c
INNER JOIN Issues AS i ON c.ISBN = i.ISBN AND c.copy_num = i.copy_num
WHERE i.return_date > CURDATE()
AND c.ISBN = "1-285-19614-7"
ORDER BY i.return_date LIMIT 1;











