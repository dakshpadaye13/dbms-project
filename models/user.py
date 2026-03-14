# ============================================================
# LearnQuest AI - User Model
# ============================================================
from utils.db_connection import execute_query
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """Provides static methods for user CRUD operations."""

    # ── Create ────────────────────────────────────────────────
    @staticmethod
    def create(username, email, password, full_name="", role="student"):
        hashed = generate_password_hash(password)
        user_id = execute_query(
            """INSERT INTO users (username, email, password_hash, full_name, role)
               VALUES (%s, %s, %s, %s, %s)""",
            (username, email, hashed, full_name, role),
            lastrowid=True
        )
        # Initialise leaderboard entry
        execute_query(
            "INSERT IGNORE INTO leaderboard (user_id) VALUES (%s)", (user_id,)
        )
        return user_id

    # ── Read ──────────────────────────────────────────────────
    @staticmethod
    def get_by_id(user_id):
        return execute_query(
            "SELECT * FROM users WHERE id = %s AND is_active = 1", (user_id,), fetchone=True
        )

    @staticmethod
    def get_by_email(email):
        return execute_query(
            "SELECT * FROM users WHERE email = %s AND is_active = 1", (email,), fetchone=True
        )

    @staticmethod
    def get_by_username(username):
        return execute_query(
            "SELECT * FROM users WHERE username = %s AND is_active = 1", (username,), fetchone=True
        )

    @staticmethod
    def get_all_students():
        return execute_query(
            "SELECT id, username, email, full_name, total_points, current_level, streak_days, created_at "
            "FROM users WHERE role='student' AND is_active=1 ORDER BY total_points DESC",
            fetch=True
        )

    # ── Verify password ───────────────────────────────────────
    @staticmethod
    def verify_password(user, password):
        if not user:
            return False
        return check_password_hash(user['password_hash'], password)

    # ── Update ────────────────────────────────────────────────
    @staticmethod
    def update_last_login(user_id):
        execute_query(
            "UPDATE users SET last_login = NOW() WHERE id = %s", (user_id,)
        )

    @staticmethod
    def update_profile(user_id, full_name, avatar_url=None):
        if avatar_url:
            execute_query(
                "UPDATE users SET full_name=%s, avatar_url=%s WHERE id=%s",
                (full_name, avatar_url, user_id)
            )
        else:
            execute_query(
                "UPDATE users SET full_name=%s WHERE id=%s", (full_name, user_id)
            )

    # ── Badges ────────────────────────────────────────────────
    @staticmethod
    def get_badges(user_id):
        return execute_query(
            """SELECT b.*, ub.earned_at
               FROM badges b
               JOIN user_badges ub ON ub.badge_id = b.id
               WHERE ub.user_id = %s
               ORDER BY ub.earned_at DESC""",
            (user_id,), fetch=True
        )

    # ── Delete (soft) ─────────────────────────────────────────
    @staticmethod
    def deactivate(user_id):
        execute_query(
            "UPDATE users SET is_active = 0 WHERE id = %s", (user_id,)
        )
