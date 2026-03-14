# ============================================================
# EduQuest - Auth Routes (Login / Signup / Logout)
# Adapted for dbmsminipppp schema
# ============================================================
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, jsonify)

auth_bp = Blueprint('auth', __name__)


def _db_ok():
    """Quick DB reachability probe."""
    try:
        from utils.db_connection import test_connection
        return test_connection()[0]
    except Exception:
        return False


# ── Signup - not used in this static schema ───────────────────
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    return redirect(url_for('auth.login'))


# ── Login ─────────────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin.panel'))
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        login_id = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # ── Hardcoded Admin bypass ─────────────────────────────
        if login_id.lower() == 'admin' and password == 'admin':
            session['user_id']   = 0
            session['username']  = 'Admin'
            session['role']      = 'admin'
            session['full_name'] = 'System Admin'
            return redirect(url_for('admin.panel'))

        if not _db_ok():
            return render_template('login.html',
                                   error="Database offline. Please start MySQL.",
                                   email=login_id)

        try:
            from utils.db_connection import execute_query

            # Query the LOGIN table
            login_record = execute_query(
                "SELECT * FROM LOGIN WHERE login_id = %s AND password = %s",
                (login_id, password), fetchone=True
            )

            if not login_record:
                # Fallback: try pattern-based auth (StudentN → passN, TeacherN → teachN)
                # This works even if LOGIN table is empty
                import re
                student_match = re.match(r'^Student(\d+)$', login_id, re.IGNORECASE)
                teacher_match = re.match(r'^Teacher(\d+)$', login_id, re.IGNORECASE)

                if student_match and password == f"pass{student_match.group(1)}":
                    student = execute_query(
                        "SELECT * FROM STUDENT WHERE student_id = %s",
                        (int(student_match.group(1)),), fetchone=True
                    )
                    if student:
                        session['user_id']   = student['student_id']
                        session['username']  = student['name']
                        session['role']      = 'student'
                        session['full_name'] = student['name']
                        session['points']    = student.get('points', 0)
                        lvl_map = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
                        session['level'] = lvl_map.get(student.get('level', 'Beginner'), 1)
                        return redirect(url_for('student.dashboard'))

                elif teacher_match and password == f"teach{teacher_match.group(1)}":
                    teacher = execute_query(
                        "SELECT * FROM TEACHER WHERE teacher_id = %s",
                        (int(teacher_match.group(1)),), fetchone=True
                    )
                    if teacher:
                        session['user_id']   = teacher['teacher_id']
                        session['username']  = teacher['name']
                        session['role']      = 'teacher'
                        session['full_name'] = teacher['name']
                        return redirect(url_for('teacher.dashboard'))

                return render_template('login.html',
                                       error="Invalid Login ID or Password.",
                                       email=login_id)

            role = login_record['role']

            if role == 'student':
                student = execute_query(
                    "SELECT * FROM STUDENT WHERE student_id = %s",
                    (login_record['student_id'],), fetchone=True
                )
                if student:
                    session['user_id']   = student['student_id']
                    session['username']  = student['name']
                    session['role']      = 'student'
                    session['full_name'] = student['name']
                    session['points']    = student.get('points', 0)
                    lvl_map = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
                    session['level'] = lvl_map.get(student.get('level', 'Beginner'), 1)
                    return redirect(url_for('student.dashboard'))

            elif role == 'teacher':
                teacher = execute_query(
                    "SELECT * FROM TEACHER WHERE teacher_id = %s",
                    (login_record['teacher_id'],), fetchone=True
                )
                if teacher:
                    session['user_id']   = teacher['teacher_id']
                    session['username']  = teacher['name']
                    session['role']      = 'teacher'
                    session['full_name'] = teacher['name']
                    return redirect(url_for('teacher.dashboard'))

            return render_template('login.html',
                                   error="Login failed. Please try again.",
                                   email=login_id)

        except Exception as e:
            return render_template('login.html',
                                   error=f"Database error: {str(e)}",
                                   email=login_id)

    return render_template('login.html')


# ── Logout ────────────────────────────────────────────────────
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.landing'))


# ── Stub ──────────────────────────────────────────────────────
@auth_bp.route('/api/check-username')
def check_username():
    return jsonify({'available': False})
