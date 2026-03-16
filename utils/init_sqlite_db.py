
import sqlite3
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import config

def init_db():
    db_path = config.DB_PATH
    db_dir = os.path.dirname(db_path)
    
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"Created directory: {db_dir}")

    print(f"Initializing database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Schema converted for SQLite
    schema = """
    DROP TABLE IF EXISTS LOGIN;
    DROP TABLE IF EXISTS LEADERBOARD;
    DROP TABLE IF EXISTS BADGE;
    DROP TABLE IF EXISTS SCRAMBLE;
    DROP TABLE IF EXISTS PUZZLE;
    DROP TABLE IF EXISTS QUIZ;
    DROP TABLE IF EXISTS ENROLL;
    DROP TABLE IF EXISTS COURSE;
    DROP TABLE IF EXISTS TEACHER;
    DROP TABLE IF EXISTS STUDENT;

    CREATE TABLE STUDENT (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        school VARCHAR(120) NOT NULL,
        village VARCHAR(120) NOT NULL,
        level TEXT DEFAULT 'Beginner',
        points INTEGER DEFAULT 0 CHECK(points >= 0)
    );

    CREATE TABLE TEACHER (
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        specialization VARCHAR(100) NOT NULL
    );

    CREATE TABLE COURSE (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(120) NOT NULL,
        subject VARCHAR(100) NOT NULL,
        level VARCHAR(50) DEFAULT 'Level1',
        teacher_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES TEACHER(teacher_id)
    );

    CREATE TABLE ENROLL (
        student_id INTEGER,
        course_id INTEGER,
        enroll_date DATE DEFAULT (CURRENT_DATE),
        PRIMARY KEY(student_id, course_id),
        FOREIGN KEY(student_id) REFERENCES STUDENT(student_id),
        FOREIGN KEY(course_id) REFERENCES COURSE(course_id)
    );

    CREATE TABLE QUIZ (
        quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER,
        marks INTEGER CHECK(marks BETWEEN 0 AND 100),
        FOREIGN KEY(course_id) REFERENCES COURSE(course_id)
    );

    CREATE TABLE PUZZLE (
        puzzle_id INTEGER PRIMARY KEY AUTOINCREMENT,
        difficulty TEXT -- Easy, Medium, Hard
    );

    CREATE TABLE SCRAMBLE (
        scramble_id INTEGER PRIMARY KEY AUTOINCREMENT,
        word_type VARCHAR(50),
        correct_answer VARCHAR(100)
    );

    CREATE TABLE BADGE (
        badge_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) UNIQUE,
        description VARCHAR(200)
    );

    CREATE TABLE LEADERBOARD (
        rank_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        points INTEGER,
        FOREIGN KEY(student_id) REFERENCES STUDENT(student_id)
    );

    CREATE TABLE LOGIN (
        login_id VARCHAR(50) NOT NULL PRIMARY KEY,
        password VARCHAR(100) NOT NULL,
        role TEXT NOT NULL, -- student, teacher
        student_id INTEGER DEFAULT NULL,
        teacher_id INTEGER DEFAULT NULL,
        FOREIGN KEY(student_id) REFERENCES STUDENT(student_id),
        FOREIGN KEY(teacher_id) REFERENCES TEACHER(teacher_id)
    );
    """

    cursor.executescript(schema)
    print("Schema created successfully.")

    # Seed Data
    seed_sql = """
    INSERT INTO TEACHER (name, specialization) VALUES 
    ('Teacher1', 'Math'), ('Teacher2', 'Science'), ('Teacher3', 'English'), ('Teacher4', 'Math'), ('Teacher5', 'Science');

    INSERT INTO STUDENT (name, school, village, level, points) VALUES 
    ('Student1', 'Rural School', 'Khed', 'Beginner', 45),
    ('Student2', 'Rural School', 'Satara', 'Intermediate', 75),
    ('Student3', 'Rural School', 'Nashik', 'Advanced', 90),
    ('Student4', 'Rural School', 'Pune', 'Beginner', 20),
    ('Student5', 'Rural School', 'Ahmednagar', 'Intermediate', 60);

    INSERT INTO COURSE (title, subject, level, teacher_id) VALUES
    ('Basic Math', 'Math', 'Level1', 1),
    ('Algebra', 'Math', 'Level2', 4),
    ('General Science', 'Science', 'Level1', 2),
    ('Physics Basics', 'Science', 'Level2', 5),
    ('English Grammar', 'English', 'Level1', 3);

    INSERT INTO ENROLL (student_id, course_id) VALUES
    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5);

    INSERT INTO QUIZ (course_id, marks) VALUES
    (1, 100), (2, 100), (3, 100);

    INSERT INTO PUZZLE (difficulty) VALUES
    ('Easy'), ('Medium'), ('Hard');

    INSERT INTO SCRAMBLE (word_type, correct_answer) VALUES
    ('Animal', 'Tiger'), ('Fruit', 'Apple'), ('Country', 'India');

    INSERT INTO BADGE (name, description) VALUES
    ('Starter', 'Completed first lesson'),
    ('Quiz Master', 'Scored above 80 in quiz'),
    ('Puzzle Solver', 'Solved puzzles'),
    ('Top Performer', 'Top 10 leaderboard');

    INSERT INTO LEADERBOARD (student_id, points) VALUES
    (3, 90), (2, 75), (5, 60), (1, 45);

    INSERT INTO LOGIN (login_id, password, role, student_id) VALUES
    ('Student1', 'pass1', 'student', 1),
    ('Student2', 'pass2', 'student', 2),
    ('Student3', 'pass3', 'student', 3),
    ('Student4', 'pass4', 'student', 4),
    ('Student5', 'pass5', 'student', 5);

    INSERT INTO LOGIN (login_id, password, role, teacher_id) VALUES
    ('Teacher1', 'teach1', 'teacher', 1),
    ('Teacher2', 'teach2', 'teacher', 2),
    ('Teacher3', 'teach3', 'teacher', 3),
    ('Teacher4', 'teach4', 'teacher', 4),
    ('Teacher5', 'teach5', 'teacher', 5);
    """

    cursor.executescript(seed_sql)
    conn.commit()
    conn.close()
    print("Seed data inserted successfully.")

if __name__ == "__main__":
    init_db()
