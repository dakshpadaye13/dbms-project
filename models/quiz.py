# ============================================================
# EduQuest - Quiz Model
# ============================================================
from utils.db_connection import execute_query


class Quiz:
    @staticmethod
    def get_all(subject_id=None, difficulty=None):
        base = """
            SELECT q.*, s.name AS subject_name, s.icon AS subject_icon,
                   COUNT(qq.id) AS question_count
            FROM quizzes q
            JOIN subjects s ON s.id = q.subject_id
            LEFT JOIN quiz_questions qq ON qq.quiz_id = q.id
            WHERE q.is_active = 1
        """
        filters, params = [], []
        if subject_id:
            filters.append("q.subject_id = %s"); params.append(subject_id)
        if difficulty:
            filters.append("q.difficulty = %s"); params.append(difficulty)
        if filters:
            base += " AND " + " AND ".join(filters)
        base += " GROUP BY q.id ORDER BY q.created_at DESC"
        return execute_query(base, tuple(params), fetch=True)

    @staticmethod
    def get_by_id(quiz_id):
        return execute_query(
            """SELECT q.*, s.name AS subject_name, s.icon AS subject_icon
               FROM quizzes q JOIN subjects s ON s.id = q.subject_id
               WHERE q.id = %s AND q.is_active = 1""",
            (quiz_id,), fetchone=True
        )

    @staticmethod
    def get_questions(quiz_id):
        return execute_query(
            "SELECT * FROM quiz_questions WHERE quiz_id = %s ORDER BY id",
            (quiz_id,), fetch=True
        )

    @staticmethod
    def add_question(quiz_id, question, opt_a, opt_b, opt_c, opt_d,
                     correct, explanation="", difficulty="medium"):
        return execute_query(
            """INSERT INTO quiz_questions
               (quiz_id, question, option_a, option_b, option_c, option_d,
                correct_answer, explanation, difficulty)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (quiz_id, question, opt_a, opt_b, opt_c, opt_d,
             correct, explanation, difficulty),
            lastrowid=True
        )

    @staticmethod
    def create(subject_id, title, description, difficulty, time_limit,
               points_per_question, created_by):
        return execute_query(
            """INSERT INTO quizzes (subject_id, title, description, difficulty,
               time_limit, points_per_question, created_by)
               VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (subject_id, title, description, difficulty,
             time_limit, points_per_question, created_by),
            lastrowid=True
        )

    @staticmethod
    def delete(quiz_id):
        execute_query("UPDATE quizzes SET is_active=0 WHERE id=%s", (quiz_id,))


class Puzzle:
    @staticmethod
    def get_all(subject_id=None, puzzle_type=None):
        base = """
            SELECT p.*, s.name AS subject_name, s.icon AS subject_icon
            FROM puzzles p JOIN subjects s ON s.id = p.subject_id
            WHERE p.is_active = 1
        """
        filters, params = [], []
        if subject_id:
            filters.append("p.subject_id = %s"); params.append(subject_id)
        if puzzle_type:
            filters.append("p.puzzle_type = %s"); params.append(puzzle_type)
        if filters:
            base += " AND " + " AND ".join(filters)
        base += " ORDER BY p.created_at DESC"
        return execute_query(base, tuple(params), fetch=True)

    @staticmethod
    def get_by_id(puzzle_id):
        return execute_query(
            """SELECT p.*, s.name AS subject_name FROM puzzles p
               JOIN subjects s ON s.id = p.subject_id
               WHERE p.id = %s AND p.is_active = 1""",
            (puzzle_id,), fetchone=True
        )

    @staticmethod
    def create(subject_id, title, description, puzzle_type, difficulty,
               puzzle_data, points, created_by):
        import json
        return execute_query(
            """INSERT INTO puzzles (subject_id, title, description, puzzle_type,
               difficulty, puzzle_data, points, created_by)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (subject_id, title, description, puzzle_type, difficulty,
             json.dumps(puzzle_data), points, created_by),
            lastrowid=True
        )


class Subject:
    @staticmethod
    def get_all():
        return execute_query(
            "SELECT * FROM subjects WHERE is_active=1 ORDER BY name", fetch=True
        )

    @staticmethod
    def get_by_id(subject_id):
        return execute_query(
            "SELECT * FROM subjects WHERE id=%s", (subject_id,), fetchone=True
        )
