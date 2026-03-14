# ============================================================
# LearnQuest AI - Game Routes (Quiz, Puzzle, Concept Match)
# ============================================================
from flask import (Blueprint, render_template, request,
                   session, redirect, url_for, jsonify)
from functools import wraps
import utils.dummy_data as dummy
import json

game_bp = Blueprint('game', __name__)


def _db_ok():
    try:
        from utils.db_connection import test_connection
        ok, _ = test_connection()
        return ok
    except Exception:
        return False


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# ── Quiz Game ─────────────────────────────────────────────────
@game_bp.route('/quiz/<int:quiz_id>')
@login_required
def quiz(quiz_id):
    if not _db_ok():
        quiz_data = dummy.get_quiz_by_id(quiz_id)
        if not quiz_data:
            return redirect(url_for('student.games'))
        questions = quiz_data.get('questions', [])
        # normalize to match template expectations
        for i, q in enumerate(questions):
            q.setdefault('id', i + 1)
        return render_template('quiz_game.html',
                               quiz=quiz_data,
                               questions=questions,
                               questions_json=json.dumps(questions),
                               best_score=0)
    try:
        from models.quiz import Quiz
        from models.progress import Progress
        quiz_data = Quiz.get_by_id(quiz_id)
        if not quiz_data:
            return redirect(url_for('student.games'))
        questions = Quiz.get_questions(quiz_id)
        best      = Progress.get_best_score(session['user_id'], 'quiz', quiz_id)
        return render_template('quiz_game.html',
                               quiz=quiz_data,
                               questions=questions,
                               questions_json=json.dumps(questions),
                               best_score=best['best'] if best else 0)
    except Exception:
        quiz_data = dummy.get_quiz_by_id(quiz_id)
        if not quiz_data:
            return redirect(url_for('student.games'))
        questions = quiz_data.get('questions', [])
        return render_template('quiz_game.html',
                               quiz=quiz_data,
                               questions=questions,
                               questions_json=json.dumps(questions),
                               best_score=0)


# ── Submit Quiz ───────────────────────────────────────────────
@game_bp.route('/api/quiz/submit', methods=['POST'])
@login_required
def submit_quiz():
    data       = request.get_json()
    quiz_id    = data.get('quiz_id')
    answers    = data.get('answers', [])
    total_time = data.get('total_time', 0)
    user_id    = session['user_id']

    # Get quiz (dummy or real)
    if not _db_ok():
        quiz_data = dummy.get_quiz_by_id(quiz_id)
        if not quiz_data:
            return jsonify({'error': 'Quiz not found'}), 404
        questions = {q['id']: q for q in quiz_data.get('questions', [])}
    else:
        try:
            from models.quiz import Quiz
            quiz_data = Quiz.get_by_id(quiz_id)
            questions = {q['id']: q for q in Quiz.get_questions(quiz_id)}
        except Exception:
            quiz_data = dummy.get_quiz_by_id(quiz_id)
            questions = {q['id']: q for q in quiz_data.get('questions', [])} if quiz_data else {}

    if not quiz_data or not questions:
        return jsonify({'error': 'Quiz not found'}), 404

    correct_count = 0
    results       = []
    for ans in answers:
        qid      = ans.get('question_id')
        selected = ans.get('selected', '').upper()
        q        = questions.get(qid)
        if not q:
            continue
        is_correct = (selected == q['correct_answer'])
        if is_correct:
            correct_count += 1
        results.append({
            'question_id':    qid,
            'selected':       selected,
            'correct_answer': q['correct_answer'],
            'is_correct':     is_correct,
            'explanation':    q.get('explanation', '')
        })

    total_q     = len(questions)
    time_limit  = quiz_data.get('time_limit', 30)
    score_pct   = round(correct_count / total_q * 100 if total_q else 0, 1)
    points_earned = int(score_pct * 1.5)

    # Try to persist if DB available
    if _db_ok():
        try:
            from models.progress import Progress
            from utils.gamification_engine import award_points, calculate_quiz_score
            score = calculate_quiz_score(correct_count, total_q, total_time, time_limit)
            Progress.record(user_id, 'quiz', quiz_id, score, total_q * 10,
                            total_time, completed=True)
            gamification = award_points(user_id, score,
                                        reason=f"Quiz: {quiz_data['title']}")
        except Exception:
            gamification = {'new_badges': [], 'level_up': False, 'points_awarded': points_earned}
    else:
        # Update session points for demo feel
        session['points'] = session.get('points', 0) + points_earned
        gamification = {'new_badges': [], 'level_up': False, 'points_awarded': points_earned}

    if correct_count == total_q and total_q > 0:
        gamification['new_badges'].append('Perfect Score 🎯')
    if total_time < 30 and correct_count > 0:
        gamification['new_badges'].append('Speed Demon ⚡')

    return jsonify({
        'score':        score_pct,
        'max_score':    100,
        'correct':      correct_count,
        'total':        total_q,
        'accuracy':     score_pct,
        'results':      results,
        'gamification': gamification
    })


# ── Puzzle Game ───────────────────────────────────────────────
@game_bp.route('/puzzle/<int:puzzle_id>')
@login_required
def puzzle(puzzle_id):
    if not _db_ok():
        puzzle_data = dummy.get_puzzle_by_id(puzzle_id)
        if not puzzle_data:
            return redirect(url_for('student.games'))
        return render_template('puzzle_game.html',
                               puzzle=puzzle_data,
                               puzzle_json=json.dumps(puzzle_data.get('puzzle_data', {})))
    try:
        from models.quiz import Puzzle
        puzzle_data = Puzzle.get_by_id(puzzle_id)
        if not puzzle_data:
            return redirect(url_for('student.games'))
        if isinstance(puzzle_data.get('puzzle_data'), str):
            puzzle_data['puzzle_data'] = json.loads(puzzle_data['puzzle_data'])
        return render_template('puzzle_game.html',
                               puzzle=puzzle_data,
                               puzzle_json=json.dumps(puzzle_data['puzzle_data']))
    except Exception:
        puzzle_data = dummy.get_puzzle_by_id(puzzle_id)
        if not puzzle_data:
            return redirect(url_for('student.games'))
        return render_template('puzzle_game.html',
                               puzzle=puzzle_data,
                               puzzle_json=json.dumps(puzzle_data.get('puzzle_data', {})))


# ── Submit Puzzle ─────────────────────────────────────────────
@game_bp.route('/api/puzzle/submit', methods=['POST'])
@login_required
def submit_puzzle():
    data       = request.get_json()
    puzzle_id  = data.get('puzzle_id')
    score      = data.get('score', 0)
    max_score  = data.get('max_score', 100)
    time_taken = data.get('time_taken', 0)
    user_id    = session['user_id']

    points_earned = int(score * 0.5)

    if _db_ok():
        try:
            from models.quiz import Puzzle
            from models.progress import Progress
            from utils.gamification_engine import award_points
            puzzle_data  = Puzzle.get_by_id(puzzle_id)
            Progress.record(user_id, 'puzzle', puzzle_id, score, max_score,
                            time_taken, completed=True)
            gamification = award_points(user_id, score,
                                        reason=f"Puzzle: {puzzle_data['title']}" if puzzle_data else "Puzzle")
        except Exception:
            gamification = {'new_badges': [], 'level_up': False, 'points_awarded': points_earned}
    else:
        session['points'] = session.get('points', 0) + points_earned
        gamification = {'new_badges': [], 'level_up': False, 'points_awarded': points_earned}

    return jsonify({'score': score, 'max_score': max_score, 'gamification': gamification})


# ── API helpers ───────────────────────────────────────────────
@game_bp.route('/api/quizzes')
@login_required
def api_quizzes():
    subject_id = request.args.get('subject_id', type=int)
    difficulty = request.args.get('difficulty')
    if not _db_ok():
        q = dummy.DUMMY_QUIZZES
        if subject_id:
            q = [x for x in q if x['subject_id'] == subject_id]
        if difficulty:
            q = [x for x in q if x['difficulty'].lower() == difficulty.lower()]
        return jsonify(q)
    try:
        from models.quiz import Quiz
        return jsonify(Quiz.get_all(subject_id=subject_id, difficulty=difficulty))
    except Exception:
        return jsonify(dummy.DUMMY_QUIZZES)


@game_bp.route('/api/puzzles')
@login_required
def api_puzzles():
    subject_id  = request.args.get('subject_id', type=int)
    puzzle_type = request.args.get('type')
    if not _db_ok():
        p = dummy.DUMMY_PUZZLES
        if subject_id:
            p = [x for x in p if x['subject_id'] == subject_id]
        if puzzle_type:
            p = [x for x in p if x['puzzle_type'] == puzzle_type]
        return jsonify(p)
    try:
        from models.quiz import Puzzle
        return jsonify(Puzzle.get_all(subject_id=subject_id, puzzle_type=puzzle_type))
    except Exception:
        return jsonify(dummy.DUMMY_PUZZLES)
