# ============================================================
# EduQuest - Dummy Data Fallback
# Used when MySQL is not connected, for demo/development use
# ============================================================
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

# ── Dummy Users ───────────────────────────────────────────────
DUMMY_USERS = [
    {
        'id': 1,
        'username': 'demo',
        'email': 'demo@eduquest.ai',
        'password_hash': generate_password_hash('demo123'),
        'full_name': 'Demo Student',
        'role': 'student',
        'total_points': 1250,
        'current_level': 5,
        'streak_days': 7,
        'last_login': datetime.now() - timedelta(days=1),
        'created_at': datetime(2024, 1, 1),
    },
    {
        'id': 2,
        'username': 'admin',
        'email': 'admin@eduquest.ai',
        'password_hash': generate_password_hash('admin123'),
        'full_name': 'Admin User',
        'role': 'admin',
        'total_points': 9999,
        'current_level': 10,
        'streak_days': 30,
        'last_login': datetime.now(),
        'created_at': datetime(2024, 1, 1),
    },
]

# ── Dummy Subjects ────────────────────────────────────────────
DUMMY_SUBJECTS = [
    {'id': 1, 'name': 'Mathematics',        'icon': '📐', 'color': '#3b82f6'},
    {'id': 2, 'name': 'Science',            'icon': '🔬', 'color': '#10b981'},
    {'id': 3, 'name': 'Computer Science',   'icon': '💻', 'color': '#7c3aed'},
    {'id': 4, 'name': 'History',            'icon': '📜', 'color': '#f59e0b'},
    {'id': 5, 'name': 'English',            'icon': '📚', 'color': '#ec4899'},
    {'id': 6, 'name': 'Geography',          'icon': '🌍', 'color': '#06b6d4'},
]

# ── Dummy Quizzes ─────────────────────────────────────────────
DUMMY_QUIZZES = [
    {
        'id': 1, 'title': 'Algebra Basics', 'subject_id': 1,
        'subject_name': 'Mathematics', 'subject_icon': '📐',
        'difficulty': 'Easy', 'time_limit': 30, 'question_count': 10,
        'points_per_question': 10,
        'description': 'Test your knowledge of basic algebra concepts.',
        'questions': [
            {
                'id': 1, 'question_text': 'What is 2 + 2?',
                'option_a': '3', 'option_b': '4', 'option_c': '5', 'option_d': '6',
                'correct_answer': 'B', 'explanation': 'Simple addition: 2+2=4'
            },
            {
                'id': 2, 'question_text': 'Solve for x: 2x = 8',
                'option_a': '2', 'option_b': '4', 'option_c': '6', 'option_d': '8',
                'correct_answer': 'B', 'explanation': 'Divide both sides by 2: x=4'
            },
            {
                'id': 3, 'question_text': 'What is the square root of 16?',
                'option_a': '2', 'option_b': '3', 'option_c': '4', 'option_d': '8',
                'correct_answer': 'C', 'explanation': '4 × 4 = 16'
            },
            {
                'id': 4, 'question_text': 'What is 5² (5 squared)?',
                'option_a': '10', 'option_b': '15', 'option_c': '20', 'option_d': '25',
                'correct_answer': 'D', 'explanation': '5 × 5 = 25'
            },
            {
                'id': 5, 'question_text': 'If y = 3x + 2 and x = 4, what is y?',
                'option_a': '10', 'option_b': '12', 'option_c': '14', 'option_d': '16',
                'correct_answer': 'C', 'explanation': 'y = 3(4) + 2 = 12 + 2 = 14'
            },
        ]
    },
    {
        'id': 2, 'title': 'Python Fundamentals', 'subject_id': 3,
        'subject_name': 'Computer Science', 'subject_icon': '💻',
        'difficulty': 'Medium', 'time_limit': 45, 'question_count': 10,
        'points_per_question': 10,
        'description': 'Core Python programming concepts and syntax.',
        'questions': [
            {
                'id': 1, 'question_text': 'What does `print("Hello")` do in Python?',
                'option_a': 'Saves text', 'option_b': 'Displays text on screen',
                'option_c': 'Creates a variable', 'option_d': 'Reads user input',
                'correct_answer': 'B', 'explanation': 'print() outputs text to the console.'
            },
            {
                'id': 2, 'question_text': 'Which keyword is used to define a function in Python?',
                'option_a': 'func', 'option_b': 'function', 'option_c': 'def', 'option_d': 'define',
                'correct_answer': 'C', 'explanation': 'def is the keyword for function definition.'
            },
            {
                'id': 3, 'question_text': 'What is the output of `len("hello")`?',
                'option_a': '4', 'option_b': '5', 'option_c': '6', 'option_d': 'Error',
                'correct_answer': 'B', 'explanation': '"hello" has 5 characters.'
            },
            {
                'id': 4, 'question_text': 'Which data type is `[1, 2, 3]` in Python?',
                'option_a': 'Tuple', 'option_b': 'Set', 'option_c': 'Dict', 'option_d': 'List',
                'correct_answer': 'D', 'explanation': 'Square brackets [] create a list.'
            },
            {
                'id': 5, 'question_text': 'What does `//` do in Python?',
                'option_a': 'Comment', 'option_b': 'Division', 'option_c': 'Floor division', 'option_d': 'Modulo',
                'correct_answer': 'C', 'explanation': '// performs integer/floor division.'
            },
        ]
    },
    {
        'id': 3, 'title': 'World History: Ancient', 'subject_id': 4,
        'subject_name': 'History', 'subject_icon': '📜',
        'difficulty': 'Hard', 'time_limit': 40, 'question_count': 10,
        'points_per_question': 10,
        'description': 'Test your knowledge of ancient civilizations.',
        'questions': [
            {
                'id': 1, 'question_text': 'Which civilization built the Great Pyramids?',
                'option_a': 'Romans', 'option_b': 'Greeks', 'option_c': 'Egyptians', 'option_d': 'Persians',
                'correct_answer': 'C', 'explanation': 'The Great Pyramids were built by ancient Egyptians.'
            },
            {
                'id': 2, 'question_text': 'In what year did the Roman Empire fall (Western)?',
                'option_a': '376 AD', 'option_b': '410 AD', 'option_c': '455 AD', 'option_d': '476 AD',
                'correct_answer': 'D', 'explanation': 'The Western Roman Empire fell in 476 AD.'
            },
            {
                'id': 3, 'question_text': 'Who was the first Emperor of China?',
                'option_a': 'Kublai Khan', 'option_b': 'Qin Shi Huang', 'option_c': 'Emperor Wu', 'option_d': 'Tang Taizong',
                'correct_answer': 'B', 'explanation': 'Qin Shi Huang unified China in 221 BC.'
            },
        ]
    },
    {
        'id': 4, 'title': 'Science: Physics Basics', 'subject_id': 2,
        'subject_name': 'Science', 'subject_icon': '🔬',
        'difficulty': 'Easy', 'time_limit': 30, 'question_count': 8,
        'points_per_question': 10,
        'description': 'Fundamental physics concepts for beginners.',
        'questions': [
            {
                'id': 1, 'question_text': "What is Newton's First Law of Motion?",
                'option_a': 'F=ma', 'option_b': 'Objects in motion stay in motion',
                'option_c': 'Every action has equal reaction', 'option_d': 'Energy is conserved',
                'correct_answer': 'B', 'explanation': 'The law of inertia — objects continue their state unless acted on.'
            },
            {
                'id': 2, 'question_text': 'What is the speed of light (approx)?',
                'option_a': '300 km/s', 'option_b': '3,000 km/s', 'option_c': '300,000 km/s', 'option_d': '3,000,000 km/s',
                'correct_answer': 'C', 'explanation': 'Light travels at approximately 299,792 km/s.'
            },
        ]
    },
    {
        'id': 5, 'title': 'English Grammar', 'subject_id': 5,
        'subject_name': 'English', 'subject_icon': '📚',
        'difficulty': 'Easy', 'time_limit': 25, 'question_count': 10,
        'points_per_question': 10,
        'description': 'Test your English grammar and vocabulary skills.',
        'questions': [
            {
                'id': 1, 'question_text': 'Which sentence is grammatically correct?',
                'option_a': 'She go to school', 'option_b': 'She goes to school',
                'option_c': 'She going to school', 'option_d': 'She gone to school',
                'correct_answer': 'B', 'explanation': 'Third person singular requires "goes".'
            },
        ]
    },
    {
        'id': 6, 'title': 'World Geography', 'subject_id': 6,
        'subject_name': 'Geography', 'subject_icon': '🌍',
        'difficulty': 'Medium', 'time_limit': 35, 'question_count': 10,
        'points_per_question': 10,
        'description': 'Explore countries, capitals, and geographical features.',
        'questions': [
            {
                'id': 1, 'question_text': 'What is the capital of Australia?',
                'option_a': 'Sydney', 'option_b': 'Melbourne', 'option_c': 'Canberra', 'option_d': 'Brisbane',
                'correct_answer': 'C', 'explanation': 'Canberra is the capital, not Sydney.'
            },
        ]
    },
]

# ── Dummy Puzzles ─────────────────────────────────────────────
DUMMY_PUZZLES = [
    {
        'id': 1, 'title': 'Match the Planets', 'subject_id': 2,
        'subject_name': 'Science', 'subject_icon': '🔬',
        'puzzle_type': 'concept_match', 'difficulty': 'Easy',
        'points': 50,
        'description': 'Match each planet to its correct description.',
        'puzzle_data': {
            'pairs': [
                {'term': 'Mercury', 'definition': 'Closest planet to the Sun'},
                {'term': 'Venus',   'definition': 'Hottest planet in the solar system'},
                {'term': 'Earth',   'definition': 'The Blue Planet — our home'},
                {'term': 'Mars',    'definition': 'The Red Planet with two moons'},
                {'term': 'Jupiter', 'definition': 'Largest planet in the solar system'},
            ]
        }
    },
    {
        'id': 2, 'title': 'Python Keywords Sort', 'subject_id': 3,
        'subject_name': 'Computer Science', 'subject_icon': '💻',
        'puzzle_type': 'drag_drop', 'difficulty': 'Medium',
        'points': 50,
        'description': 'Sort Python keywords into the correct categories.',
        'puzzle_data': {
            'categories': ['Loop Keywords', 'Condition Keywords', 'Function Keywords'],
            'items': {
                'for':    'Loop Keywords',
                'while':  'Loop Keywords',
                'if':     'Condition Keywords',
                'elif':   'Condition Keywords',
                'else':   'Condition Keywords',
                'def':    'Function Keywords',
                'return': 'Function Keywords',
                'lambda': 'Function Keywords',
            }
        }
    },
    {
        'id': 3, 'title': 'Historical Events Timeline', 'subject_id': 4,
        'subject_name': 'History', 'subject_icon': '📜',
        'puzzle_type': 'concept_match', 'difficulty': 'Hard',
        'points': 50,
        'description': 'Match historical events to their correct years.',
        'puzzle_data': {
            'pairs': [
                {'term': '1776',  'definition': 'American Declaration of Independence'},
                {'term': '1789',  'definition': 'French Revolution begins'},
                {'term': '1865',  'definition': 'American Civil War ends'},
                {'term': '1945',  'definition': 'World War II ends'},
                {'term': '1969',  'definition': 'First Moon Landing'},
            ]
        }
    },
]

# ── Dummy Progress / Activity ─────────────────────────────────
DUMMY_HISTORY = [
    {'activity_type': 'quiz', 'activity_title': 'Algebra Basics', 'score': 85, 'max_score': 100, 'points_earned': 120, 'completed_at': datetime.now() - timedelta(hours=2), 'attempt_number': 1},
    {'activity_type': 'puzzle', 'activity_title': 'Match the Planets', 'score': 100, 'max_score': 100, 'points_earned': 50, 'completed_at': datetime.now() - timedelta(hours=5), 'attempt_number': 1},
    {'activity_type': 'quiz', 'activity_title': 'Python Fundamentals', 'score': 72, 'max_score': 100, 'points_earned': 90, 'completed_at': datetime.now() - timedelta(days=1), 'attempt_number': 1},
    {'activity_type': 'quiz', 'activity_title': 'English Grammar', 'score': 90, 'max_score': 100, 'points_earned': 130, 'completed_at': datetime.now() - timedelta(days=2), 'attempt_number': 1},
    {'activity_type': 'puzzle', 'activity_title': 'Python Keywords Sort', 'score': 80, 'max_score': 100, 'points_earned': 50, 'completed_at': datetime.now() - timedelta(days=3), 'attempt_number': 2},
]

DUMMY_STATS = {
    'total_activities': 24,
    'completed': 22,
    'total_score': 1250,
    'avg_accuracy': 83.5,
    'best_score': 100,
}

DUMMY_SUBJECT_STATS = [
    {'name': 'Mathematics',      'icon': '📐', 'color': '#3b82f6', 'points_earned': 450, 'games_played': 8},
    {'name': 'Computer Science', 'icon': '💻', 'color': '#7c3aed', 'points_earned': 320, 'games_played': 6},
    {'name': 'History',          'icon': '📜', 'color': '#f59e0b', 'points_earned': 150, 'games_played': 4},
    {'name': 'Science',          'icon': '🔬', 'color': '#10b981', 'points_earned': 180, 'games_played': 3},
    {'name': 'English',          'icon': '📚', 'color': '#ec4899', 'points_earned': 150, 'games_played': 3},
]

DUMMY_BADGES = [
    {'name': 'First Steps',   'icon': '🎯', 'color': '#3b82f6', 'description': 'Completed your first quiz', 'earned_at': datetime.now() - timedelta(days=5)},
    {'name': 'Quick Learner', 'icon': '⚡', 'color': '#f59e0b', 'description': 'Completed 5 games in one day', 'earned_at': datetime.now() - timedelta(days=4)},
    {'name': '7-Day Streak',  'icon': '🔥', 'color': '#ef4444', 'description': 'Maintained a 7-day learning streak', 'earned_at': datetime.now() - timedelta(days=1)},
    {'name': 'Math Wizard',   'icon': '📐', 'color': '#3b82f6', 'description': 'Scored 100% on a Math quiz', 'earned_at': datetime.now() - timedelta(days=3)},
    {'name': 'Scholar',       'icon': '📚', 'color': '#ec4899', 'description': 'Earned 1000+ total points', 'earned_at': datetime.now() - timedelta(days=2)},
]

DUMMY_LEADERBOARD = [
    {'rank': 1,  'username': 'TopLearner',  'full_name': 'Riya Sharma',    'total_points': 4200, 'current_level': 9,  'streak_days': 21, 'total_games': 45},
    {'rank': 2,  'username': 'AceStudent',  'full_name': 'Arjun Mehta',    'total_points': 3800, 'current_level': 8,  'streak_days': 14, 'total_games': 38},
    {'rank': 3,  'username': 'demo',        'full_name': 'Demo Student',    'total_points': 1250, 'current_level': 5,  'streak_days': 7,  'total_games': 24},
    {'rank': 4,  'username': 'BrainBox',    'full_name': 'Nisha Kapoor',   'total_points': 1100, 'current_level': 4,  'streak_days': 5,  'total_games': 18},
    {'rank': 5,  'username': 'QuizKing',    'full_name': 'Dev Patel',      'total_points': 980,  'current_level': 4,  'streak_days': 3,  'total_games': 15},
    {'rank': 6,  'username': 'StudyPro',    'full_name': 'Meera Nair',     'total_points': 850,  'current_level': 3,  'streak_days': 2,  'total_games': 12},
    {'rank': 7,  'username': 'FastLearner', 'full_name': 'Aditya Roy',     'total_points': 720,  'current_level': 3,  'streak_days': 1,  'total_games': 10},
    {'rank': 8,  'username': 'Genius99',    'full_name': 'Priya Singh',    'total_points': 600,  'current_level': 2,  'streak_days': 0,  'total_games': 8},
    {'rank': 9,  'username': 'Challenger',  'full_name': 'Rohan Kumar',    'total_points': 450,  'current_level': 2,  'streak_days': 0,  'total_games': 6},
    {'rank': 10, 'username': 'NewComer',    'full_name': 'Anjali Verma',   'total_points': 200,  'current_level': 1,  'streak_days': 0,  'total_games': 3},
]

# ── Lookup helpers ────────────────────────────────────────────
def get_user_by_email(email):
    return next((u for u in DUMMY_USERS if u['email'] == email), None)

def get_user_by_id(user_id):
    return next((u for u in DUMMY_USERS if u['id'] == user_id), None)

def get_quiz_by_id(quiz_id):
    return next((q for q in DUMMY_QUIZZES if q['id'] == int(quiz_id)), None)

def get_puzzle_by_id(puzzle_id):
    return next((p for p in DUMMY_PUZZLES if p['id'] == int(puzzle_id)), None)

def verify_password(user, password):
    return check_password_hash(user['password_hash'], password)
