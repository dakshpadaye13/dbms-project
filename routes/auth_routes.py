# ============================================================
# LearnQuest AI - Auth Routes (Login / Signup / Logout)
# ============================================================
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, jsonify)

auth_bp = Blueprint('auth', __name__)

DB_AVAILABLE = True  # will be set to False if DB fails on import

try:
    from models.user import User
    from utils.gamification_engine import update_streak
except Exception:
    DB_AVAILABLE = False

import utils.dummy_data as dummy


def _db_ok():
    """Quick DB reachability probe."""
    try:
        from utils.db_connection import test_connection
        return test_connection()
    except Exception:
        return False


# ── Signup ────────────────────────────────────────────────────
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        username  = request.form.get('username', '').strip()
        email     = request.form.get('email', '').strip().lower()
        password  = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()

        if not _db_ok():
            # Demo mode: auto-login as demo user
            flash('⚠ Database offline — signed in as Demo user.', 'warning')
            d = dummy.get_user_by_email('demo@learnquest.ai')
            session['user_id']   = d['id']
            session['username']  = d['username']
            session['role']      = d['role']
            session['full_name'] = d['full_name']
            session['points']    = d['total_points']
            session['level']     = d['current_level']
            return redirect(url_for('student.dashboard'))

        errors = []
        if not username or len(username) < 3:
            errors.append("Username must be at least 3 characters.")
        if not email or '@' not in email:
            errors.append("Please enter a valid email address.")
        if not password or len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        try:
            if User.get_by_username(username):
                errors.append("Username already taken.")
            if User.get_by_email(email):
                errors.append("Email already registered.")
        except Exception:
            pass

        if errors:
            return render_template('signup.html', errors=errors,
                                   username=username, email=email,
                                   full_name=full_name)

        try:
            user_id = User.create(username, email, password, full_name)
            session['user_id']   = user_id
            session['username']  = username
            session['role']      = 'student'
            session['full_name'] = full_name or username
            session['points']    = 0
            session['level']     = 1
            return redirect(url_for('student.dashboard'))
        except Exception as e:
            flash('Registration failed. Please try again.', 'error')
            return render_template('signup.html')

    return render_template('signup.html')


# ── Login ─────────────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin.panel'))
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)

        # ── Dummy fallback when DB is unreachable ──────────────
        if not _db_ok():
            user = dummy.get_user_by_email(email)
            if user and dummy.verify_password(user, password):
                session.permanent = bool(remember)
                session['user_id']   = user['id']
                session['username']  = user['username']
                session['role']      = user['role']
                session['full_name'] = user['full_name']
                session['points']    = user['total_points']
                session['level']     = user['current_level']
                flash('⚠ Running in Demo mode — database offline.', 'warning')
                if user['role'] == 'admin':
                    return redirect(url_for('admin.panel'))
                return redirect(url_for('student.dashboard'))
            else:
                # Hint for demo mode
                return render_template('login.html',
                                       error="Invalid credentials. Try demo@learnquest.ai / demo123",
                                       email=email)

        # ── Normal DB login ────────────────────────────────────
        try:
            user = User.get_by_email(email)
            if user and User.verify_password(user, password):
                session.permanent = bool(remember)
                session['user_id']   = user['id']
                session['username']  = user['username']
                session['role']      = user['role']
                session['full_name'] = user['full_name'] or user['username']
                session['points']    = user.get('total_points', 0)
                session['level']     = user.get('current_level', 1)

                try:
                    update_streak(user['id'])
                    User.update_last_login(user['id'])
                except Exception:
                    pass

                if user['role'] == 'admin':
                    return redirect(url_for('admin.panel'))
                return redirect(url_for('student.dashboard'))
            else:
                return render_template('login.html',
                                       error="Invalid email or password.",
                                       email=email)
        except Exception:
            # DB failed mid-request — fallback to dummy
            user = dummy.get_user_by_email(email)
            if user and dummy.verify_password(user, password):
                session['user_id']   = user['id']
                session['username']  = user['username']
                session['role']      = user['role']
                session['full_name'] = user['full_name']
                session['points']    = user['total_points']
                session['level']     = user['current_level']
                flash('⚠ Running in Demo mode — database offline.', 'warning')
                return redirect(url_for('student.dashboard'))
            return render_template('login.html',
                                   error="Database offline. Use demo@learnquest.ai / demo123",
                                   email=email)

    return render_template('login.html')


# ── Logout ────────────────────────────────────────────────────
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.landing'))


# ── API: Check username uniqueness ────────────────────────────
@auth_bp.route('/api/check-username')
def check_username():
    username = request.args.get('username', '').strip()
    try:
        taken = bool(User.get_by_username(username))
    except Exception:
        taken = any(u['username'] == username for u in dummy.DUMMY_USERS)
    return jsonify({'available': not taken})
