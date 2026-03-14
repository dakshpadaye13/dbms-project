# ============================================================
# EduQuest - User Model (Adapted for dbmsminipppp)
# ============================================================
from utils.db_connection import execute_query

class User:
    """Provides methods for user (STUDENT) operations."""

    @staticmethod
    def get_student_by_id(student_id):
        return execute_query(
            "SELECT * FROM STUDENT WHERE student_id = %s", (student_id,), fetchone=True
        )

    @staticmethod
    def get_student_by_name(name):
        return execute_query(
            "SELECT * FROM STUDENT WHERE name = %s", (name,), fetchone=True
        )

    @staticmethod
    def get_all_students():
        return execute_query(
            "SELECT * FROM STUDENT ORDER BY points DESC", fetch=True
        )

    @staticmethod
    def get_all_teachers():
        return execute_query(
            "SELECT * FROM TEACHER", fetch=True
        )
