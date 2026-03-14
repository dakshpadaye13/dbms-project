# ============================================================
# EduQuest - Gamification Engine
# Handles: points, levels, badges, streaks, leaderboard
# ============================================================
from utils.db_connection import execute_query
from config import config
from datetime import date, datetime
import logging

logger = logging.getLogger(__name__)

# ── Level Thresholds ──────────────────────────────────────────
LEVEL_THRESHOLDS = config.LEVEL_THRESHOLDS   # [0, 100, 250, ...]
LEVEL_NAMES = [
    "Beginner", "Explorer", "Learner", "Scholar",
    "Expert", "Master", "Champion", "Legend",
    "Grandmaster", "Quantum Mind"
]


def get_level_from_points(points: int) -> int:
    """Return 1-based level for the given points total."""
    for lvl, threshold in enumerate(reversed(LEVEL_THRESHOLDS), 1):
        if points >= threshold:
            return len(LEVEL_THRESHOLDS) - lvl + 1
    return 1


def get_level_name(level: int) -> str:
    idx = min(level - 1, len(LEVEL_NAMES) - 1)
    return LEVEL_NAMES[idx]


def get_next_level_points(points: int) -> dict:
    """Return progress info toward the next level."""
    current_level = get_level_from_points(points)
    if current_level >= len(LEVEL_THRESHOLDS):
        return {"current": points, "next": None, "percent": 100}
    current_threshold = LEVEL_THRESHOLDS[current_level - 1]
    next_threshold    = LEVEL_THRESHOLDS[current_level]
    percent = int(((points - current_threshold) / (next_threshold - current_threshold)) * 100)
    return {
        "current":   points,
        "next":      next_threshold,
        "percent":   min(percent, 100),
        "remaining": next_threshold - points
    }


# ── Points & Level Update ─────────────────────────────────────
def award_points(user_id: int, points: int, reason: str = "") -> dict:
    """
    Add points to a user's total. Recalculate level.
    Returns updated user stats.
    """
    execute_query(
        "UPDATE users SET total_points = total_points + %s WHERE id = %s",
        (points, user_id)
    )
    user = execute_query(
        "SELECT total_points FROM users WHERE id = %s", (user_id,), fetchone=True
    )
    new_total  = user['total_points']
    new_level  = get_level_from_points(new_total)
    execute_query(
        "UPDATE users SET current_level = %s WHERE id = %s",
        (new_level, user_id)
    )
    # Update leaderboard cache
    _update_leaderboard(user_id)
    # Check badge eligibility
    new_badges = check_and_award_badges(user_id)
    logger.info(f"User {user_id} awarded {points} pts ({reason}). Total: {new_total}, Level: {new_level}")
    return {
        "points_awarded": points,
        "total_points":   new_total,
        "level":          new_level,
        "level_name":     get_level_name(new_level),
        "new_badges":     new_badges
    }


# ── Streak Tracking ──────────────────────────────────────────
def update_streak(user_id: int):
    """Increment streak if user logged in today, reset if they missed a day."""
    user = execute_query(
        "SELECT last_login, streak_days FROM users WHERE id = %s", (user_id,), fetchone=True
    )
    if not user:
        return
    today = date.today()
    last  = user['last_login'].date() if user['last_login'] else None
    if last == today:
        return   # already updated today
    if last and (today - last).days == 1:
        new_streak = user['streak_days'] + 1
    else:
        new_streak = 1
    execute_query(
        "UPDATE users SET streak_days = %s, last_login = %s WHERE id = %s",
        (new_streak, datetime.now(), user_id)
    )
    # Streak badge check
    if new_streak >= 7:
        _grant_badge_by_name(user_id, "Streak Master")


# ── Badge Engine ─────────────────────────────────────────────
def check_and_award_badges(user_id: int) -> list:
    """Check all badge conditions and grant any newly earned badges."""
    new_badges = []
    user = execute_query(
        "SELECT total_points, streak_days FROM users WHERE id = %s", (user_id,), fetchone=True
    )
    if not user:
        return new_badges

    # Points-based badges
    badges = execute_query("SELECT * FROM badges WHERE points_required > 0", fetch=True)
    for badge in badges:
        if user['total_points'] >= badge['points_required']:
            if _grant_badge_by_id(user_id, badge['id']):
                new_badges.append(badge['name'])

    # Activity-based badges
    completed_quizzes = execute_query(
        "SELECT COUNT(*) as cnt FROM student_progress WHERE user_id=%s AND activity_type='quiz' AND completed=1",
        (user_id,), fetchone=True
    )
    if completed_quizzes and completed_quizzes['cnt'] >= 1:
        if _grant_badge_by_name(user_id, "First Steps"):
            new_badges.append("First Steps")

    completed_puzzles = execute_query(
        "SELECT COUNT(*) as cnt FROM student_progress WHERE user_id=%s AND activity_type='puzzle' AND completed=1",
        (user_id,), fetchone=True
    )
    if completed_puzzles and completed_puzzles['cnt'] >= 5:
        if _grant_badge_by_name(user_id, "Puzzle Pro"):
            new_badges.append("Puzzle Pro")

    return new_badges


def award_perfect_score_badge(user_id: int) -> bool:
    return _grant_badge_by_name(user_id, "Quick Learner")


def award_speed_badge(user_id: int) -> bool:
    return _grant_badge_by_name(user_id, "Speed Demon")


def _grant_badge_by_id(user_id: int, badge_id: int) -> bool:
    try:
        execute_query(
            "INSERT IGNORE INTO user_badges (user_id, badge_id) VALUES (%s, %s)",
            (user_id, badge_id)
        )
        return True
    except Exception:
        return False


def _grant_badge_by_name(user_id: int, badge_name: str) -> bool:
    badge = execute_query(
        "SELECT id FROM badges WHERE name = %s", (badge_name,), fetchone=True
    )
    if badge:
        return _grant_badge_by_id(user_id, badge['id'])
    return False


# ── Leaderboard ───────────────────────────────────────────────
def _update_leaderboard(user_id: int):
    """Refresh leaderboard cache for a single user."""
    stats = execute_query("""
        SELECT
            COUNT(*) as total_games,
            COALESCE(SUM(CASE WHEN score >= max_score * 0.7 THEN 1 ELSE 0 END) / NULLIF(COUNT(*),0) * 100, 0) as win_rate
        FROM student_progress
        WHERE user_id = %s AND completed = 1
    """, (user_id,), fetchone=True)

    user = execute_query(
        "SELECT total_points FROM users WHERE id = %s", (user_id,), fetchone=True
    )
    execute_query("""
        INSERT INTO leaderboard (user_id, total_points, total_games, win_rate)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            total_points = %s,
            total_games  = %s,
            win_rate     = %s
    """, (
        user_id, user['total_points'], stats['total_games'], stats['win_rate'],
        user['total_points'], stats['total_games'], stats['win_rate']
    ))


def get_leaderboard(limit: int = 10) -> list:
    """Fetch top N leaderboard entries with rank."""
    return execute_query("""
        SELECT
            u.id, u.username, u.full_name, u.avatar_url,
            u.total_points, u.current_level,
            l.total_games, l.win_rate,
            RANK() OVER (ORDER BY u.total_points DESC) as `rank`
        FROM users u
        LEFT JOIN leaderboard l ON l.user_id = u.id
        WHERE u.role = 'student' AND u.is_active = 1
        ORDER BY u.total_points DESC
        LIMIT %s
    """, (limit,), fetch=True)


def get_user_rank(user_id: int) -> int:
    """Return the rank position of a given user."""
    result = execute_query("""
        SELECT COUNT(*) + 1 as `rank`
        FROM users
        WHERE role = 'student' AND is_active = 1
          AND total_points > (SELECT total_points FROM users WHERE id = %s)
    """, (user_id,), fetchone=True)
    return result['rank'] if result else 0


# ── Score Calculation ─────────────────────────────────────────
def calculate_quiz_score(correct: int, total: int, time_taken: int, time_limit: int) -> int:
    """
    Score = base_points + time_bonus
    Time bonus: proportional to how quickly the quiz was finished.
    """
    if total == 0:
        return 0
    base  = correct * config.POINTS_PER_CORRECT_ANSWER
    ratio = max(0, (time_limit - time_taken) / time_limit)
    bonus = int(base * 0.5 * ratio)
    return base + bonus
