# ============================================================
# LearnQuest AI - Admin Routes (DBMS Viewer)
# ============================================================
from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps
from utils.db_connection import execute_query

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# ── Admin Panel (Database Viewer) ─────────────────────────────
@admin_bp.route('/admin')
@admin_required
def panel():
    tables_data = {}
    try:
        tables_data['STUDENT'] = execute_query("SELECT * FROM STUDENT", fetch=True)
        tables_data['TEACHER'] = execute_query("SELECT * FROM TEACHER", fetch=True)
        tables_data['COURSE']  = execute_query("SELECT * FROM COURSE", fetch=True)
        tables_data['ENROLL']  = execute_query("SELECT * FROM ENROLL", fetch=True)
        tables_data['QUIZ']    = execute_query("SELECT * FROM QUIZ", fetch=True)
        tables_data['PUZZLE']  = execute_query("SELECT * FROM PUZZLE", fetch=True)
        tables_data['SCRAMBLE']= execute_query("SELECT * FROM SCRAMBLE", fetch=True)
        tables_data['BADGE']   = execute_query("SELECT * FROM BADGE", fetch=True)
        tables_data['LEADERBOARD'] = execute_query("SELECT * FROM LEADERBOARD", fetch=True)
    except Exception as e:
        print(f"Error fetching admin data: {e}")

    return render_template('admin_panel.html', tables_data=tables_data)
