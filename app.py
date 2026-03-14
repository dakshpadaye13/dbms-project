# ============================================================
# EduQuest - Flask Application Entry Point
# ============================================================
from flask import Flask, render_template, session, redirect, url_for
from config import config
from utils.db_connection import test_connection
import logging

# ── Logging Setup ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if config.DEBUG else logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    # ── Register Blueprints ───────────────────────────────────
    from routes.auth_routes    import auth_bp
    from routes.student_routes import student_bp
    from routes.admin_routes   import admin_bp
    from routes.game_routes    import game_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(game_bp)

    # ── Landing Page (main route) ─────────────────────────────
    from flask import Blueprint
    main_bp = Blueprint('main', __name__)

    @main_bp.route('/')
    def landing():
        if 'user_id' in session:
            if session.get('role') == 'admin':
                return redirect(url_for('admin.panel'))
            return redirect(url_for('student.dashboard'))
        return render_template('landing.html')

    app.register_blueprint(main_bp)

    # ── Error Handlers ────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return render_template('error.html', code=404,
                               message="Page not found"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('error.html', code=500,
                               message="Internal server error"), 500

    # ── Template Globals ──────────────────────────────────────
    @app.context_processor
    def inject_globals():
        from utils.gamification_engine import get_level_name
        return {
            'app_name': 'EduQuest',
            'get_level_name': get_level_name
        }

    # ── DB Health Check on Start ──────────────────────────────
    ok, msg = test_connection()
    if ok:
        logger.info(f"Database: {msg}")
    else:
        logger.warning(f"Database connection failed: {msg}")

    return app


# ── Run ───────────────────────────────────────────────────────
if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=3000,
        debug=config.DEBUG
    )
