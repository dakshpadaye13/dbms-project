# ============================================================
# LearnQuest AI - Student Routes (Adapted for dbmsminipppp)
# ============================================================
from flask import (Blueprint, render_template, redirect, url_for, session, jsonify)
from functools import wraps
from utils.db_connection import execute_query

student_bp = Blueprint('student', __name__)

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
    
    # Fetch Student
    user = execute_query("SELECT * FROM STUDENT WHERE student_id = %s", (user_id,), fetchone=True)
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))

    # Fetch Enrolled Courses
    courses = execute_query("""
        SELECT c.course_id, c.title, c.subject, c.level, t.name as teacher_name
        FROM COURSE c
        JOIN ENROLL e ON c.course_id = e.course_id
        JOIN TEACHER t ON c.teacher_id = t.teacher_id
        WHERE e.student_id = %s
    """, (user_id,), fetch=True)

    # Calculate rank based on LEADERBOARD or points
    rank_data = execute_query("""
        SELECT COUNT(*) + 1 as rank 
        FROM STUDENT WHERE points > %s
    """, (user.get('points', 0),), fetchone=True)
    rank = rank_data['rank'] if rank_data else '--'

    return render_template('dashboard.html', user=user, courses=courses, rank=rank)


# ── Leaderboard ───────────────────────────────────────────────
@student_bp.route('/leaderboard')
@login_required
def leaderboard():
    user_id = session['user_id']
    # Use the LEADERBOARD table joined with STUDENT
    board = execute_query("""
        SELECT s.name as username, l.points, 
               (@row_number:=@row_number + 1) AS rank
        FROM LEADERBOARD l
        JOIN STUDENT s ON s.student_id = l.student_id
        JOIN (SELECT @row_number:=0) r
        ORDER BY l.points DESC
    """, fetch=True)

    # Simplified user rank logic
    user_rank = '--'
    for b in board:
        if b['username'] == session.get('username'):
            user_rank = b['rank']
            break

    user = {'username': session.get('username'), 'total_points': session.get('points', 0)}
    return render_template('leaderboard.html', board=board, user_rank=user_rank, current_user=user)


# ── Games / Courses List ──────────────────────────────────────
@student_bp.route('/games')
@login_required
def games():
    courses = execute_query("SELECT * FROM COURSE", fetch=True)
    puzzles = execute_query("SELECT * FROM PUZZLE", fetch=True)
    return render_template('games.html', courses=courses, puzzles=puzzles)


# ── Profile ───────────────────────────────────────────────────
@student_bp.route('/profile')
@login_required
def profile():
    user_id = session['user_id']
    user = execute_query("SELECT * FROM STUDENT WHERE student_id = %s", (user_id,), fetchone=True)
    
    # User's quiz marks
    history = execute_query("""
        SELECT c.title, q.marks
        FROM QUIZ q
        JOIN COURSE c ON q.course_id = c.course_id
        JOIN ENROLL e ON c.course_id = e.course_id
        WHERE e.student_id = %s
    """, (user_id,), fetch=True)

    return render_template('profile.html', user=user, history=history, rank='--')


@student_bp.route('/api/my-stats')
@login_required
def my_stats():
    # Simplistic API just for UI functionality
    return jsonify({
        'points': session.get('points', 0),
        'level': session.get('level', 1),
        'level_name': 'Student Level',
        'streak': 0,
        'total_games': 0
    })
