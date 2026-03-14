# ============================================================
# EduQuest - Game Model
# (Delegates to quiz.py and gamification_engine.py)
# ============================================================
# This module provides a unified interface for game-related queries.

from models.quiz import Quiz, Puzzle, Subject
from models.progress import Progress
from utils.gamification_engine import get_leaderboard, get_user_rank


class Game:
    """Unified game interface for templates/routes."""

    @staticmethod
    def get_recent_players(limit=5):
        """Get recently active students."""
        from utils.db_connection import execute_query
        return execute_query(
            """SELECT u.username, u.current_level, u.total_points,
                      MAX(sp.completed_at) AS last_active
               FROM users u
               JOIN student_progress sp ON sp.user_id = u.id
               WHERE u.role = 'student'
               GROUP BY u.id
               ORDER BY last_active DESC
               LIMIT %s""",
            (limit,), fetch=True
        )

    @staticmethod
    def get_quiz_leaderboard(quiz_id, limit=10):
        """Top scorers for a specific quiz."""
        from utils.db_connection import execute_query
        return execute_query(
            """SELECT u.username, MAX(sp.score) AS best_score,
                      MIN(sp.time_taken) AS best_time
               FROM student_progress sp
               JOIN users u ON u.id = sp.user_id
               WHERE sp.activity_type = 'quiz' AND sp.activity_id = %s
                 AND sp.completed = 1
               GROUP BY u.id, u.username
               ORDER BY best_score DESC, best_time ASC
               LIMIT %s""",
            (quiz_id, limit), fetch=True
        )
