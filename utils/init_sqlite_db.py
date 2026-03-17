
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

    # Seed Data (Dynamic Generation to match MySQL schema)
    print("Seeding Teachers...")
    specializations = ['Math', 'Science', 'English']
    teachers = []
    for i in range(1, 26):
        teachers.append((f"Teacher{i}", specializations[i % 3]))
    cursor.executemany("INSERT INTO TEACHER (name, specialization) VALUES (?, ?)", teachers)

    print("Seeding Students...")
    villages = ['Khed', 'Satara', 'Nashik', 'Pune', 'Ahmednagar']
    levels = ['Beginner', 'Intermediate', 'Advanced']
    students = []
    for i in range(1, 151):
        students.append((
            f"Student{i}", 
            "Rural School", 
            villages[i % 5], 
            levels[i % 3], 
            (i * 7) % 100
        ))
    cursor.executemany("INSERT INTO STUDENT (name, school, village, level, points) VALUES (?, ?, ?, ?, ?)", students)

    print("Seeding Courses...")
    courses = [
        ('Basic Math', 'Math', 'Level1', 1),
        ('Algebra', 'Math', 'Level2', 4),
        ('General Science', 'Science', 'Level1', 2),
        ('Physics Basics', 'Science', 'Level2', 5),
        ('English Grammar', 'English', 'Level1', 3),
        ('Story Reading', 'English', 'Level1', 6),
        ('Geometry', 'Math', 'Level2', 7),
        ('Biology', 'Science', 'Level2', 8),
        ('Essay Writing', 'English', 'Level2', 9),
        ('Advanced Math', 'Math', 'Level3', 10)
    ]
    cursor.executemany("INSERT INTO COURSE (title, subject, level, teacher_id) VALUES (?, ?, ?, ?)", courses)

    print("Seeding Enrollments...")
    enrollments = []
    for i in range(1, 151):
        enrollments.append((i, (i % 10) + 1))
    cursor.executemany("INSERT INTO ENROLL (student_id, course_id) VALUES (?, ?)", enrollments)

    print("Seeding Quiz, Puzzles, Scramble...")
    cursor.execute("INSERT INTO QUIZ (course_id, marks) VALUES (1, 100), (2, 100), (3, 100)")
    cursor.execute("INSERT INTO PUZZLE (difficulty) VALUES ('Easy'), ('Medium'), ('Hard')")
    cursor.execute("INSERT INTO SCRAMBLE (word_type, correct_answer) VALUES ('Animal', 'Tiger'), ('Fruit', 'Apple'), ('Country', 'India')")

    print("Seeding Badges...")
    cursor.execute("""
    INSERT INTO BADGE (name, description) VALUES
    ('Starter', 'Completed first lesson'),
    ('Quiz Master', 'Scored above 80 in quiz'),
    ('Puzzle Solver', 'Solved puzzles'),
    ('Top Performer', 'Top 10 leaderboard')
    """)

    print("Seeding Leaderboard...")
    cursor.execute("""
    INSERT INTO LEADERBOARD (student_id, points)
    SELECT student_id, points FROM STUDENT ORDER BY points DESC LIMIT 20
    """)

    print("Seeding Login accounts...")
    # Student logins
    student_logins = []
    for i in range(1, 151):
        student_logins.append((f"Student{i}", f"pass{i}", "student", i))
    cursor.executemany("INSERT INTO LOGIN (login_id, password, role, student_id) VALUES (?, ?, ?, ?)", student_logins)

    # Teacher logins
    teacher_logins = []
    for i in range(1, 26):
        teacher_logins.append((f"Teacher{i}", f"teach{i}", "teacher", i))
    cursor.executemany("INSERT INTO LOGIN (login_id, password, role, teacher_id) VALUES (?, ?, ?, ?)", teacher_logins)
    conn.commit()
    conn.close()
    print("Seed data inserted successfully.")

if __name__ == "__main__":
    init_db()
