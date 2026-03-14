-- ============================================================
-- EduQuest - Seed Data
-- Run AFTER schema.sql
-- ============================================================

USE eduquest_db;

-- ------------------------------------------------------------
-- ADMIN USER (password: Admin@123)
-- Hash generated with werkzeug.security.generate_password_hash
-- ------------------------------------------------------------
INSERT INTO users (username, email, password_hash, role, full_name, total_points, current_level) VALUES
('admin', 'admin@eduquest.ai', 'pbkdf2:sha256:260000$salt$hash_placeholder', 'admin', 'EduQuest Admin', 9999, 99);

-- Note: Replace password_hash with actual generated hash via Flask shell:
-- from werkzeug.security import generate_password_hash
-- generate_password_hash('Admin@123')

-- ------------------------------------------------------------
-- BADGES
-- ------------------------------------------------------------
INSERT INTO badges (name, description, icon, color, points_required) VALUES
('First Steps',   'Complete your first quiz',              '🎯', '#3b82f6',  10),
('Quick Learner', 'Score 100% on any quiz',                '⚡', '#f59e0b',  50),
('Streak Master', 'Login 7 days in a row',                 '🔥', '#ef4444',  0),
('Puzzle Pro',    'Complete 5 puzzles',                    '🧩', '#8b5cf6',  0),
('Scholar',       'Earn 500 total points',                 '🎓', '#10b981',  500),
('Champion',      'Reach the top 3 on leaderboard',        '🏆', '#f59e0b',  0),
('Speed Demon',   'Complete a quiz in under 60 seconds',   '💨', '#06b6d4',  0),
('Knowledge King','Earn 1000 total points',                '👑', '#7c3aed',  1000);

-- ------------------------------------------------------------
-- SUBJECTS
-- ------------------------------------------------------------
INSERT INTO subjects (name, description, icon, color) VALUES
('Mathematics',   'Numbers, algebra, geometry and more', '🔢', '#3b82f6'),
('Science',       'Physics, chemistry and biology',      '🔬', '#10b981'),
('History',       'World history and civilizations',     '📜', '#f59e0b'),
('Computer Science', 'Programming, algorithms and CS concepts', '💻', '#8b5cf6'),
('English',       'Grammar, vocabulary and literature',  '📖', '#ec4899'),
('Geography',     'Maps, countries and ecosystems',      '🌍', '#06b6d4');

-- ------------------------------------------------------------
-- QUIZZES
-- ------------------------------------------------------------
-- Math Quiz 1
INSERT INTO quizzes (subject_id, title, description, difficulty, time_limit, points_per_question, created_by) VALUES
(1, 'Algebra Basics', 'Test your algebra fundamentals', 'easy', 300, 10, 1),
(1, 'Geometry Challenge', 'Shapes, angles and area calculations', 'medium', 360, 15, 1),
(2, 'Physics Fundamentals', 'Newton laws and energy concepts', 'medium', 300, 10, 1),
(2, 'Chemistry Crash Course', 'Elements, compounds and reactions', 'medium', 300, 10, 1),
(4, 'Python Basics', 'Variables, loops and functions in Python', 'easy', 300, 10, 1),
(3, 'World War II', 'Key events, figures and outcomes', 'medium', 300, 10, 1);

-- ------------------------------------------------------------
-- QUIZ QUESTIONS - Algebra Basics (quiz_id = 1)
-- ------------------------------------------------------------
INSERT INTO quiz_questions (quiz_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation) VALUES
(1, 'What is the value of x if 2x + 4 = 10?',
   '2', '3', '4', '5', 'B',
   '2x = 10 - 4 = 6, so x = 3'),

(1, 'Simplify: 3(x + 4) - 2x',
   'x + 12', 'x + 4', '5x + 12', 'x + 8', 'A',
   '3x + 12 - 2x = x + 12'),

(1, 'What is the slope of y = 3x + 7?',
   '7', '3', '1/3', '-3', 'B',
   'In y = mx + b, the slope m = 3'),

(1, 'Solve: x² = 16',
   'x = 4', 'x = ±4', 'x = 8', 'x = 2', 'B',
   'Square root of 16 gives ±4'),

(1, 'Which is a polynomial?',
   '√x + 1', '2x² + 3x - 5', '1/x + 2', 'x^(-1)', 'B',
   'Polynomials have non-negative integer exponents only');

-- ------------------------------------------------------------
-- QUIZ QUESTIONS - Python Basics (quiz_id = 5)
-- ------------------------------------------------------------
INSERT INTO quiz_questions (quiz_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation) VALUES
(5, 'Which keyword is used to define a function in Python?',
   'function', 'define', 'def', 'func', 'C',
   'In Python, `def` keyword is used to define functions'),

(5, 'What is the output of: print(type(3.14))?',
   "<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'double'>", 'B',
   '3.14 is a floating-point number'),

(5, 'Which data structure uses key-value pairs?',
   'list', 'tuple', 'dictionary', 'set', 'C',
   'Python dictionaries store key-value pairs'),

(5, 'How do you create a list in Python?',
   'list = {}', 'list = ()', 'list = []', 'list = <>','C',
   'Square brackets [] are used for lists'),

(5, 'What does len([1, 2, 3, 4]) return?',
   '3', '4', '5', 'None', 'B',
   'len() returns the number of elements; the list has 4 elements');

-- ------------------------------------------------------------
-- QUIZ QUESTIONS - Physics Fundamentals (quiz_id = 3)
-- ------------------------------------------------------------
INSERT INTO quiz_questions (quiz_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation) VALUES
(3, 'What is Newton''s Second Law?',
   'F = ma', 'E = mc²', 'PV = nRT', 'F = mg', 'A',
   'Force equals mass times acceleration'),

(3, 'What is the unit of force?',
   'Watt', 'Joule', 'Newton', 'Pascal', 'C',
   'Force is measured in Newtons (N)'),

(3, 'Light travels at approximately what speed?',
   '3×10⁸ m/s', '3×10⁶ m/s', '3×10¹⁰ m/s', '3×10⁴ m/s', 'A',
   'Speed of light c ≈ 3×10⁸ metres per second'),

(3, 'Which type of energy is stored in a stretched spring?',
   'Kinetic energy', 'Thermal energy', 'Nuclear energy', 'Potential energy', 'D',
   'Elastic potential energy is stored in deformed objects'),

(3, 'What does a voltmeter measure?',
   'Current', 'Resistance', 'Voltage', 'Power', 'C',
   'Voltmeters measure electrical potential difference');

-- ------------------------------------------------------------
-- PUZZLES - Concept Match
-- ------------------------------------------------------------
INSERT INTO puzzles (subject_id, title, description, puzzle_type, difficulty, puzzle_data, points, created_by) VALUES
(4, 'Python Concepts Match',
   'Match each Python concept to its definition',
   'concept_match', 'easy',
   '{"pairs": [
      {"term": "Variable",    "definition": "A named storage location for data"},
      {"term": "Loop",        "definition": "Repeats a block of code"},
      {"term": "Function",    "definition": "A reusable block of code"},
      {"term": "List",        "definition": "An ordered collection of items"},
      {"term": "Dictionary",  "definition": "Stores key-value pairs"}
   ]}',
   50, 1),

(1, 'Math Terms Drag & Drop',
   'Drag the math terms to their correct category',
   'drag_drop', 'medium',
   '{"categories": ["Algebra", "Geometry", "Statistics"],
     "items": [
       {"text": "Variable",   "category": "Algebra"},
       {"text": "Triangle",   "category": "Geometry"},
       {"text": "Mean",       "category": "Statistics"},
       {"text": "Equation",   "category": "Algebra"},
       {"text": "Area",       "category": "Geometry"},
       {"text": "Median",     "category": "Statistics"}
     ]}',
   60, 1),

(2, 'Science Word Sort',
   'Sort these science terms into correct categories',
   'word_sort', 'medium',
   '{"categories": ["Physics", "Chemistry", "Biology"],
     "items": [
       {"text": "Atom",       "category": "Chemistry"},
       {"text": "Cell",       "category": "Biology"},
       {"text": "Force",      "category": "Physics"},
       {"text": "DNA",        "category": "Biology"},
       {"text": "Electron",   "category": "Chemistry"},
       {"text": "Velocity",   "category": "Physics"}
     ]}',
   60, 1);

-- ------------------------------------------------------------
-- END OF SEED DATA
-- ============================================================
