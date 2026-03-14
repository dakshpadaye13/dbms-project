# ============================================================
# LearnQuest AI - Progress Model
# ============================================================
from utils.db_connection import execute_query


class Progress:
    @staticmethod
    def record(user_id, activity_type, activity_id, score,
               max_score, time_taken, completed=True):
        """Save a completed activity attempt."""
        attempt = execute_query(
            """SELECT COALESCE(MAX(attempt_number), 0) + 1 AS next_attempt
               FROM student_progress
               WHERE user_id=%s AND activity_type=%s AND activity_id=%s""",
            (user_id, activity_type, activity_id), fetchone=True
        )
        next_attempt = attempt['next_attempt'] if attempt else 1
        return execute_query(
            """INSERT INTO student_progress
               (user_id, activity_type, activity_id, score, max_score,
                time_taken, completed, attempt_number)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (user_id, activity_type, activity_id, score, max_score,
             time_taken, completed, next_attempt),
            lastrowid=True
        )

    @staticmethod
    def record_answer(user_id, quiz_id, question_id, selected, is_correct, time_taken):
        execute_query(
            """INSERT INTO scores (user_id, quiz_id, question_id,
               selected_answer, is_correct, time_taken)
               VALUES (%s,%s,%s,%s,%s,%s)""",
            (user_id, quiz_id, question_id, selected, is_correct, time_taken)
        )

    @staticmethod
    def get_user_history(user_id, limit=20):
        return execute_query(
            """SELECT sp.*, 
                CASE sp.activity_type
                    WHEN 'quiz'   THEN (SELECT title FROM quizzes  WHERE id = sp.activity_id)
                    WHEN 'puzzle' THEN (SELECT title FROM puzzles   WHERE id = sp.activity_id)
                    ELSE 'Unknown'
                END AS activity_title
               FROM student_progress sp
               WHERE sp.user_id = %s
               ORDER BY sp.completed_at DESC
               LIMIT %s""",
            (user_id, limit), fetch=True
        )

    @staticmethod
    def get_stats(user_id):
        return execute_query(
            """SELECT
                COUNT(*) AS total_activities,
                SUM(completed) AS completed,
                COALESCE(SUM(score), 0) AS total_score,
                COALESCE(AVG(score/NULLIF(max_score,0)*100), 0) AS avg_accuracy,
                COALESCE(MAX(score), 0) AS best_score
               FROM student_progress
               WHERE user_id = %s""",
            (user_id,), fetchone=True
        )

    @staticmethod
    def get_subject_stats(user_id):
        """Points earned per subject."""
        return execute_query(
            """SELECT s.name, s.icon, s.color,
                      COUNT(sp.id) AS attempts,
                      COALESCE(SUM(sp.score), 0) AS points_earned
               FROM subjects s
               LEFT JOIN quizzes q ON q.subject_id = s.id
               LEFT JOIN student_progress sp
                   ON sp.activity_type = 'quiz' AND sp.activity_id = q.id
                   AND sp.user_id = %s
               GROUP BY s.id, s.name, s.icon, s.color
               ORDER BY points_earned DESC""",
            (user_id,), fetch=True
        )

    @staticmethod
    def get_best_score(user_id, activity_type, activity_id):
        return execute_query(
            """SELECT MAX(score) AS best FROM student_progress
               WHERE user_id=%s AND activity_type=%s AND activity_id=%s""",
            (user_id, activity_type, activity_id), fetchone=True
        )
