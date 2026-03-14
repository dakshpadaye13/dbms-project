# ============================================================
# LearnQuest AI - Auth Routes (Login / Signup / Logout)
# Adapted for dbmsminipppp schema
# ============================================================
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, jsonify)

auth_bp = Blueprint('auth', __name__)

DB_AVAILABLE = True

try:
    from models.user import User
except Exception:
    DB_AVAILABLE = False


def _db_ok():
    """Quick DB reachability probe."""
    try:
        from utils.db_connection import test_connection
        return test_connection()[0]
    except Exception:
        return False


# ── Signup ────────────────────────────────────────────────────
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # Signup doesn't make sense in this static DBMS schema right now,
    # redirecting to login.
    return redirect(url_for('auth.login'))


# ── Login ─────────────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin.panel'))
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        login_key = request.form.get('email', '').strip() # Reuse the email field for student name/id or admin
        
        # Hardcoded Admin Login
        if login_key.lower() == 'admin':
            session['user_id']   = 0
            session['username']  = 'Admin'
            session['role']      = 'admin'
            session['full_name'] = 'System Admin'
            return redirect(url_for('admin.panel'))

        if not _db_ok():
            flash('⚠ Database offline — cannot resolve student.', 'warning')
            return render_template('login.html', error="Database offline.", email=login_key)

        try:
            # Try to fetch by ID or Name
            user = None
            if login_key.isdigit():
                user = User.get_student_by_id(int(login_key))
            if not user:
                user = User.get_student_by_name(login_key)

            if user:
                session.permanent = True
                session['user_id']   = user['student_id']
                session['username']  = user['name']
                session['role']      = 'student'
                session['full_name'] = user['name']
                session['points']    = user.get('points', 0)
                
                # Assign arbitrary level based on ENUM mapping
                lvl_map = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
                session['level']     = lvl_map.get(user.get('level', 'Beginner'), 1)

                return redirect(url_for('student.dashboard'))
            else:
                return render_template('login.html',
                                       error="Student not found. Please enter a valid Student Name (e.g., Student1) or ID.",
                                       email=login_key)
        except Exception as e:
            return render_template('login.html',
                                   error=f"Database error: {str(e)}",
                                   email=login_key)

    return render_template('login.html')


# ── Logout ────────────────────────────────────────────────────
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.landing'))


# ── API: Check username uniqueness ────────────────────────────
@auth_bp.route('/api/check-username')
def check_username():
    return jsonify({'available': False})
