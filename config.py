# ============================================================
# EduQuest - Application Configuration
# ============================================================
import os


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'eduquest_super_secret_key_2024')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # SQLite Database Configuration
    DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'eduquest.db')

    # Gamification Settings
    POINTS_PER_CORRECT_ANSWER = 10
    POINTS_PER_PUZZLE         = 50
    STREAK_BONUS_MULTIPLIER   = 1.5
    LEVEL_THRESHOLDS = [0, 100, 250, 500, 1000, 2000, 3500, 5000, 7500, 10000]


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


# Active config
config = DevelopmentConfig()
