# ============================================================
# LearnQuest AI - Admin Routes
# ============================================================
from flask import (Blueprint, render_template, request,
                   session, redirect, url_for, jsonify, flash)
from functools import wraps
from models.user import User
from models.quiz import Quiz, Puzzle, Subject
from models.progress import Progress
from utils.db_connection import execute_query
from utils.gamification_engine import get_leaderboard
import json

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# ── Admin Panel (main) ────────────────────────────────────────
@admin_bp.route('/admin')
@admin_required
def panel():
    students = User.get_all_students()
    quizzes  = Quiz.get_all()
    puzzles  = Puzzle.get_all()
    subjects = Subject.get_all()

    # Analytics summary
    total_attempts = execute_query(
        "SELECT COUNT(*) AS cnt FROM student_progress WHERE completed=1", fetchone=True
    )
    total_points_given = execute_query(
        "SELECT COALESCE(SUM(total_points),0) AS total FROM users WHERE role='student'",
        fetchone=True
    )

    return render_template('admin_panel.html',
                           students=students,
                           quizzes=quizzes,
                           puzzles=puzzles,
                           subjects=subjects,
                           total_attempts=total_attempts['cnt'] if total_attempts else 0,
                           total_points_given=total_points_given['total'] if total_points_given else 0)


# ── Add Quiz ──────────────────────────────────────────────────
@admin_bp.route('/admin/quiz/add', methods=['POST'])
@admin_required
def add_quiz():
    data = request.get_json() or request.form
    quiz_id = Quiz.create(
        subject_id=int(data.get('subject_id')),
        title=data.get('title'),
        description=data.get('description', ''),
        difficulty=data.get('difficulty', 'medium'),
        time_limit=int(data.get('time_limit', 300)),
        points_per_question=int(data.get('points_per_question', 10)),
        created_by=session['user_id']
    )
    return jsonify({'success': True, 'quiz_id': quiz_id})


# ── Add Quiz Question ─────────────────────────────────────────
@admin_bp.route('/admin/quiz/question/add', methods=['POST'])
@admin_required
def add_question():
    data = request.get_json() or request.form
    qid  = Quiz.add_question(
        quiz_id=int(data.get('quiz_id')),
        question=data.get('question'),
        opt_a=data.get('option_a'),
        opt_b=data.get('option_b'),
        opt_c=data.get('option_c'),
        opt_d=data.get('option_d'),
        correct=data.get('correct_answer', 'A').upper(),
        explanation=data.get('explanation', ''),
        difficulty=data.get('difficulty', 'medium')
    )
    return jsonify({'success': True, 'question_id': qid})


# ── Delete Quiz ───────────────────────────────────────────────
@admin_bp.route('/admin/quiz/<int:quiz_id>/delete', methods=['POST'])
@admin_required
def delete_quiz(quiz_id):
    Quiz.delete(quiz_id)
    return jsonify({'success': True})


# ── Add Puzzle ────────────────────────────────────────────────
@admin_bp.route('/admin/puzzle/add', methods=['POST'])
@admin_required
def add_puzzle():
    data = request.get_json()
    pid  = Puzzle.create(
        subject_id=int(data.get('subject_id')),
        title=data.get('title'),
        description=data.get('description', ''),
        puzzle_type=data.get('puzzle_type', 'concept_match'),
        difficulty=data.get('difficulty', 'medium'),
        puzzle_data=data.get('puzzle_data', {}),
        points=int(data.get('points', 50)),
        created_by=session['user_id']
    )
    return jsonify({'success': True, 'puzzle_id': pid})


# ── Manage Students ───────────────────────────────────────────
@admin_bp.route('/admin/student/<int:student_id>/deactivate', methods=['POST'])
@admin_required
def deactivate_student(student_id):
    User.deactivate(student_id)
    return jsonify({'success': True})


# ── Analytics API ─────────────────────────────────────────────
@admin_bp.route('/admin/api/analytics')
@admin_required
def analytics():
    # Most played quizzes
    top_quizzes = execute_query("""
        SELECT q.title, COUNT(sp.id) AS plays
        FROM quizzes q
        LEFT JOIN student_progress sp ON sp.activity_type='quiz' AND sp.activity_id=q.id
        GROUP BY q.id, q.title
        ORDER BY plays DESC
        LIMIT 5
    """, fetch=True)

    # Daily registrations (last 7 days)
    daily_reg = execute_query("""
        SELECT DATE(created_at) AS day, COUNT(*) AS count
        FROM users WHERE role='student'
          AND created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY DATE(created_at)
        ORDER BY day
    """, fetch=True)

    return jsonify({
        'top_quizzes': top_quizzes,
        'daily_registrations': [
            {'day': str(r['day']), 'count': r['count']} for r in daily_reg
        ]
    })


# ── Add Subject ───────────────────────────────────────────────
@admin_bp.route('/admin/subject/add', methods=['POST'])
@admin_required
def add_subject():
    data = request.get_json() or request.form
    execute_query(
        "INSERT INTO subjects (name, description, icon, color) VALUES (%s,%s,%s,%s)",
        (data.get('name'), data.get('description', ''),
         data.get('icon', '📚'), data.get('color', '#7c3aed'))
    )
    return jsonify({'success': True})
