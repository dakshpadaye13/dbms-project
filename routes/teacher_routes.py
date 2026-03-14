# ============================================================
# EduQuest - Teacher Routes
# ============================================================
from flask import Blueprint, render_template, redirect, url_for, session
from functools import wraps
from utils.db_connection import execute_query

teacher_bp = Blueprint('teacher', __name__)


def teacher_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        if session.get('role') not in ('teacher', 'admin'):
            return redirect(url_for('student.dashboard'))
        return f(*args, **kwargs)
    return decorated


# ── Teacher Dashboard ─────────────────────────────────────────
@teacher_bp.route('/teacher/dashboard')
@teacher_required
def dashboard():
    teacher_id = session['user_id']

    # Fetch teacher profile
    teacher = execute_query(
        "SELECT * FROM TEACHER WHERE teacher_id = %s", (teacher_id,), fetchone=True
    )
    if not teacher:
        session.clear()
        return redirect(url_for('auth.login'))

    # Courses this teacher teaches
    courses = execute_query(
        "SELECT * FROM COURSE WHERE teacher_id = %s", (teacher_id,), fetch=True
    )

    # Total enrolled students across all teacher's courses
    enrolled_count = execute_query("""
        SELECT COUNT(DISTINCT e.student_id) AS total
        FROM ENROLL e
        JOIN COURSE c ON e.course_id = c.course_id
        WHERE c.teacher_id = %s
    """, (teacher_id,), fetchone=True)

    # Students enrolled in teacher's courses
    students = execute_query("""
        SELECT DISTINCT s.student_id, s.name, s.school, s.village, s.level, s.points,
               c.title as course_title
        FROM STUDENT s
        JOIN ENROLL e ON s.student_id = e.student_id
        JOIN COURSE c ON e.course_id = c.course_id
        WHERE c.teacher_id = %s
        ORDER BY s.points DESC
    """, (teacher_id,), fetch=True)

    total_enrolled = enrolled_count['total'] if enrolled_count else 0

    return render_template('teacher_dashboard.html',
                           teacher=teacher,
                           courses=courses,
                           students=students,
                           total_enrolled=total_enrolled)
