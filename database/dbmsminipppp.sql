DROP DATABASE IF EXISTS dbmsminipppp;
CREATE DATABASE dbmsminipppp;
USE dbmsminipppp;

CREATE TABLE STUDENT (
student_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100) NOT NULL,
school VARCHAR(120) NOT NULL,
village VARCHAR(120) NOT NULL,
level ENUM('Beginner','Intermediate','Advanced') DEFAULT 'Beginner',
points INT DEFAULT 0 CHECK(points >= 0)
);
CREATE TABLE TEACHER (
teacher_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100) NOT NULL,
specialization VARCHAR(100) NOT NULL
);
CREATE TABLE COURSE (
course_id INT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(120) NOT NULL,
subject VARCHAR(100) NOT NULL,
level VARCHAR(50) DEFAULT 'Level1',
teacher_id INT,
FOREIGN KEY (teacher_id) REFERENCES TEACHER(teacher_id)
);
CREATE TABLE ENROLL (
student_id INT,
course_id INT,
enroll_date DATE DEFAULT (CURRENT_DATE),
PRIMARY KEY(student_id,course_id),
FOREIGN KEY(student_id) REFERENCES STUDENT(student_id),
FOREIGN KEY(course_id) REFERENCES COURSE(course_id)
);
CREATE TABLE QUIZ (
quiz_id INT AUTO_INCREMENT PRIMARY KEY,
course_id INT,
marks INT CHECK(marks BETWEEN 0 AND 100),
FOREIGN KEY(course_id) REFERENCES COURSE(course_id)
);
CREATE TABLE PUZZLE (
puzzle_id INT AUTO_INCREMENT PRIMARY KEY,
difficulty ENUM('Easy','Medium','Hard')
);
CREATE TABLE SCRAMBLE (
scramble_id INT AUTO_INCREMENT PRIMARY KEY,
word_type VARCHAR(50),
correct_answer VARCHAR(100)
);
CREATE TABLE BADGE (
badge_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100) UNIQUE,
description VARCHAR(200)
);
CREATE TABLE LEADERBOARD (
rank_id INT AUTO_INCREMENT PRIMARY KEY,
student_id INT,
points INT,
FOREIGN KEY(student_id) REFERENCES STUDENT(student_id)
);
CREATE TABLE LOGIN (
login_id   VARCHAR(50)  NOT NULL PRIMARY KEY,
password   VARCHAR(100) NOT NULL,
role       ENUM('student','teacher') NOT NULL,
student_id INT DEFAULT NULL,
teacher_id INT DEFAULT NULL,
FOREIGN KEY(student_id) REFERENCES STUDENT(student_id),
FOREIGN KEY(teacher_id) REFERENCES TEACHER(teacher_id)
);
INSERT INTO TEACHER(name,specialization)
SELECT CONCAT('Teacher',n),
ELT(FLOOR(1+RAND()*3),'Math','Science','English')
FROM (
SELECT a.N + b.N*10 +1 n
FROM
(SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) a
CROSS JOIN
(SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) b
) numbers
WHERE n <= 25;
INSERT INTO STUDENT(name,school,village,level,points)
SELECT 
CONCAT('Student',n),
'Rural School',
ELT(FLOOR(1+RAND()*5),'Khed','Satara','Nashik','Pune','Ahmednagar'),
ELT(FLOOR(1+RAND()*3),'Beginner','Intermediate','Advanced'),
FLOOR(RAND()*100)
FROM (
SELECT a.N + b.N*10 + c.N*100 +1 n
FROM
(SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a
CROSS JOIN
(SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) b
CROSS JOIN
(SELECT 0 N UNION SELECT 1) c
) numbers
WHERE n <= 150;
INSERT INTO COURSE(title,subject,level,teacher_id)
VALUES
('Basic Math','Math','Level1',1),
('Algebra','Math','Level2',2),
('General Science','Science','Level1',3),
('Physics Basics','Science','Level2',4),
('English Grammar','English','Level1',5),
('Story Reading','English','Level1',6),
('Geometry','Math','Level2',7),
('Biology','Science','Level2',8),
('Essay Writing','English','Level2',9),
('Advanced Math','Math','Level3',10);
INSERT INTO ENROLL(student_id,course_id)
SELECT student_id, FLOOR(1+RAND()*10)
FROM STUDENT
LIMIT 150;

INSERT INTO QUIZ(course_id,marks)
VALUES
(1,100),(2,100),(3,100),(4,100),(5,100);

INSERT INTO PUZZLE(difficulty)
VALUES
('Easy'),('Medium'),('Hard'),('Easy'),('Medium');

INSERT INTO SCRAMBLE(word_type,correct_answer)
VALUES
('Animal','Tiger'),
('Fruit','Apple'),
('Country','India'),
('Bird','Peacock');
INSERT INTO BADGE(name,description)
VALUES
('Starter','Completed first lesson'),
('Quiz Master','Scored above 80 in quiz'),
('Puzzle Solver','Solved puzzles'),
('Top Performer','Top 10 leaderboard');

INSERT INTO LEADERBOARD(student_id,points)
SELECT student_id,points
FROM STUDENT
ORDER BY points DESC
LIMIT 20;

-- Seed LOGIN table for students (login_id = Student name, password = 'pass' + student_id)
INSERT INTO LOGIN (login_id, password, role, student_id)
SELECT name, CONCAT('pass', student_id), 'student', student_id
FROM STUDENT;

-- Seed LOGIN table for teachers (login_id = Teacher name, password = 'teach' + teacher_id)
INSERT INTO LOGIN (login_id, password, role, teacher_id)
SELECT name, CONCAT('teach', teacher_id), 'teacher', teacher_id
FROM TEACHER;
SELECT * FROM STUDENT LIMIT 50;
SELECT s.name,l.points
FROM LEADERBOARD l
JOIN STUDENT s ON s.student_id=l.student_id
ORDER BY points DESC;
SELECT c.title,t.name
FROM COURSE c
JOIN TEACHER t
ON c.teacher_id=t.teacher_id;
SELECT s.name,c.title
FROM STUDENT s
JOIN ENROLL e ON s.student_id=e.student_id
JOIN COURSE c ON c.course_id=e.course_id; 

