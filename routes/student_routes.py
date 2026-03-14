# ============================================================
# LearnQuest AI - Student Routes (Dashboard, Progress, etc.)
# ============================================================
from flask import (Blueprint, render_template, request,
                   redirect, url_for, session, jsonify)
from functools import wraps
import utils.dummy_data as dummy

student_bp = Blueprint('student', __name__)

# ── Helpers ───────────────────────────────────────────────────
def _db_ok():
    try:
        from utils.db_connection import test_connection
        return test_connection()
    except Exception:
        return False

LEVEL_THRESHOLDS = [0, 100, 250, 500, 1000, 2000, 3500, 5000, 7500, 10000]
LEVEL_NAMES      = ['Novice','Apprentice','Learner','Scholar','Expert',
                    'Master','Grandmaster','Legend','Elite','Champion']

def _level_info(points):
    level = 1
    for i, t in enumerate(LEVEL_THRESHOLDS):
        if points >= t:
            level = i + 1
    next_t = LEVEL_THRESHOLDS[min(level, len(LEVEL_THRESHOLDS)-1)]
    prev_t = LEVEL_THRESHOLDS[level - 1]
    pct    = int((points - prev_t) / max(next_t - prev_t, 1) * 100) if next_t > prev_t else 100
    return {'current_level': level, 'next_threshold': next_t,
            'current_threshold': prev_t, 'percentage': pct}

def _level_name(level):
    return LEVEL_NAMES[min(level - 1, len(LEVEL_NAMES)-1)]

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# ── Dashboard ─────────────────────────────────────────────────
@student_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']

    if not _db_ok():
        user          = dummy.get_user_by_id(user_id) or dummy.DUMMY_USERS[0]
        badges        = dummy.DUMMY_BADGES
        history       = dummy.DUMMY_HISTORY[:5]
        stats         = dummy.DUMMY_STATS
        subject_stats = dummy.DUMMY_SUBJECT_STATS
        level_info    = _level_info(user['total_points'])
        rank          = next((e['rank'] for e in dummy.DUMMY_LEADERBOARD
                              if e['username'] == user['username']), 99)
        level_name    = _level_name(user['current_level'])
        quizzes       = dummy.DUMMY_QUIZZES[:6]
    else:
        try:
            from models.user import User
            from models.quiz import Quiz
            from models.progress import Progress
            from utils.gamification_engine import (
                get_next_level_points, get_level_name, get_user_rank)
            user          = User.get_by_id(user_id)
            badges        = User.get_badges(user_id)
            history       = Progress.get_user_history(user_id, limit=5)
            stats         = Progress.get_stats(user_id)
            subject_stats = Progress.get_subject_stats(user_id)
            level_info    = get_next_level_points(user['total_points'])
            rank          = get_user_rank(user_id)
            level_name    = get_level_name(user['current_level'])
            quizzes       = Quiz.get_all()[:6]
        except Exception:
            user          = dummy.get_user_by_id(user_id) or dummy.DUMMY_USERS[0]
            badges        = dummy.DUMMY_BADGES
            history       = dummy.DUMMY_HISTORY[:5]
            stats         = dummy.DUMMY_STATS
            subject_stats = dummy.DUMMY_SUBJECT_STATS
            level_info    = _level_info(user['total_points'])
            rank          = 3
            level_name    = _level_name(user['current_level'])
            quizzes       = dummy.DUMMY_QUIZZES[:6]

    return render_template('dashboard.html',
                           user=user, badges=badges, history=history,
                           stats=stats, subject_stats=subject_stats,
                           level_info=level_info, rank=rank,
                           level_name=level_name, quizzes=quizzes)


# ── Leaderboard ───────────────────────────────────────────────
@student_bp.route('/leaderboard')
@login_required
def leaderboard():
    user_id = session['user_id']

    if not _db_ok():
        board        = dummy.DUMMY_LEADERBOARD
        current_user = dummy.get_user_by_id(user_id) or dummy.DUMMY_USERS[0]
        user_rank    = next((e['rank'] for e in board
                             if e['username'] == current_user['username']), 99)
    else:
        try:
            from models.user import User
            from utils.gamification_engine import get_leaderboard, get_user_rank
            board        = get_leaderboard(limit=50)
            user_rank    = get_user_rank(user_id)
            current_user = User.get_by_id(user_id)
        except Exception:
            board        = dummy.DUMMY_LEADERBOARD
            current_user = dummy.get_user_by_id(user_id) or dummy.DUMMY_USERS[0]
            user_rank    = 3

    return render_template('leaderboard.html',
                           board=board, user_rank=user_rank,
                           current_user=current_user)


# ── Games List ────────────────────────────────────────────────
@student_bp.route('/games')
@login_required
def games():
    if not _db_ok():
        subjects = dummy.DUMMY_SUBJECTS
        quizzes  = dummy.DUMMY_QUIZZES
        puzzles  = dummy.DUMMY_PUZZLES
    else:
        try:
            from models.quiz import Quiz, Puzzle, Subject
            subjects = Subject.get_all()
            quizzes  = Quiz.get_all()
            puzzles  = Puzzle.get_all()
        except Exception:
            subjects = dummy.DUMMY_SUBJECTS
            quizzes  = dummy.DUMMY_QUIZZES
            puzzles  = dummy.DUMMY_PUZZLES

    return render_template('games.html',
                           subjects=subjects, quizzes=quizzes, puzzles=puzzles)


# ── Profile ───────────────────────────────────────────────────
@student_bp.route('/profile')
@login_required
def profile():
    user_id = session['user_id']

    if not _db_ok():
        user    = dummy.get_user_by_id(user_id) or dummy.DUMMY_USERS[0]
        badges  = dummy.DUMMY_BADGES
        stats   = dummy.DUMMY_STATS
        history = dummy.DUMMY_HISTORY
        rank    = 3
    else:
        try:
            from models.user import User
            from models.progress import Progress
            from utils.gamification_engine import get_user_rank
            user    = User.get_by_id(user_id)
            badges  = User.get_badges(user_id)
            stats   = Progress.get_stats(user_id)
            history = Progress.get_user_history(user_id, limit=10)
            rank    = get_user_rank(user_id)
        except Exception:
            user    = dummy.get_user_by_id(user_id) or dummy.DUMMY_USERS[0]
            badges  = dummy.DUMMY_BADGES
            stats   = dummy.DUMMY_STATS
            history = dummy.DUMMY_HISTORY
            rank    = 3

    return render_template('profile.html',
                           user=user, badges=badges, stats=stats,
                           rank=rank, history=history)


# ── API: User stats JSON ───────────────────────────────────────
@student_bp.route('/api/my-stats')
@login_required
def my_stats():
    user_id = session['user_id']
    if not _db_ok():
        user  = dummy.get_user_by_id(user_id) or dummy.DUMMY_USERS[0]
        stats = dummy.DUMMY_STATS
    else:
        try:
            from models.user import User
            from models.progress import Progress
            from utils.gamification_engine import get_level_name
            user  = User.get_by_id(user_id)
            stats = Progress.get_stats(user_id)
        except Exception:
            user  = dummy.get_user_by_id(user_id) or dummy.DUMMY_USERS[0]
            stats = dummy.DUMMY_STATS

    return jsonify({
        'points':      user['total_points'],
        'level':       user['current_level'],
        'level_name':  _level_name(user['current_level']),
        'streak':      user['streak_days'],
        'total_games': stats.get('total_activities', 0),
    })
