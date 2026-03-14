-- ============================================================
-- EduQuest - MySQL Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS eduquest_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE eduquest_db;

-- ------------------------------------------------------------
-- USERS TABLE
-- Stores both students and admins
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    username     VARCHAR(50)  NOT NULL UNIQUE,
    email        VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role         ENUM('student', 'admin') NOT NULL DEFAULT 'student',
    full_name    VARCHAR(100),
    avatar_url   VARCHAR(255),
    total_points INT          NOT NULL DEFAULT 0,
    current_level INT         NOT NULL DEFAULT 1,
    streak_days  INT          NOT NULL DEFAULT 0,
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login   DATETIME,
    is_active    BOOLEAN      NOT NULL DEFAULT TRUE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- BADGES TABLE
-- Defines all available badges
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS badges (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon        VARCHAR(50)  NOT NULL,   -- emoji or icon class
    color       VARCHAR(20)  NOT NULL DEFAULT '#7c3aed',
    points_required INT NOT NULL DEFAULT 0,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- USER BADGES (junction table)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_badges (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT NOT NULL,
    badge_id   INT NOT NULL,
    earned_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)  REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (badge_id) REFERENCES badges(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_badge (user_id, badge_id)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- SUBJECTS TABLE
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS subjects (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon        VARCHAR(50)  NOT NULL DEFAULT '📚',
    color       VARCHAR(20)  NOT NULL DEFAULT '#7c3aed',
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- QUIZZES TABLE
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS quizzes (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    subject_id  INT NOT NULL,
    title       VARCHAR(200) NOT NULL,
    description TEXT,
    difficulty  ENUM('easy', 'medium', 'hard') NOT NULL DEFAULT 'medium',
    time_limit  INT NOT NULL DEFAULT 300,  -- seconds
    points_per_question INT NOT NULL DEFAULT 10,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_by  INT,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id)  REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by)  REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- QUIZ QUESTIONS TABLE
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS quiz_questions (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    quiz_id     INT NOT NULL,
    question    TEXT NOT NULL,
    option_a    VARCHAR(500) NOT NULL,
    option_b    VARCHAR(500) NOT NULL,
    option_c    VARCHAR(500) NOT NULL,
    option_d    VARCHAR(500) NOT NULL,
    correct_answer ENUM('A','B','C','D') NOT NULL,
    explanation TEXT,
    difficulty  ENUM('easy','medium','hard') NOT NULL DEFAULT 'medium',
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- PUZZLES TABLE
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS puzzles (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    subject_id  INT NOT NULL,
    title       VARCHAR(200) NOT NULL,
    description TEXT,
    puzzle_type ENUM('drag_drop', 'concept_match', 'word_sort') NOT NULL DEFAULT 'drag_drop',
    difficulty  ENUM('easy','medium','hard') NOT NULL DEFAULT 'medium',
    puzzle_data JSON NOT NULL,   -- stores puzzle config as JSON
    points      INT NOT NULL DEFAULT 50,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_by  INT,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id)    ON DELETE SET NULL
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- STUDENT PROGRESS TABLE
-- Tracks completion per user per quiz/puzzle
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS student_progress (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    activity_type ENUM('quiz','puzzle','concept_match') NOT NULL,
    activity_id INT NOT NULL,
    score       INT NOT NULL DEFAULT 0,
    max_score   INT NOT NULL DEFAULT 0,
    time_taken  INT,                 -- seconds
    completed   BOOLEAN NOT NULL DEFAULT FALSE,
    attempt_number INT NOT NULL DEFAULT 1,
    completed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- SCORES TABLE
-- Detailed answer log per quiz attempt
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS scores (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT NOT NULL,
    quiz_id      INT NOT NULL,
    question_id  INT NOT NULL,
    selected_answer ENUM('A','B','C','D'),
    is_correct   BOOLEAN NOT NULL DEFAULT FALSE,
    time_taken   INT,              -- seconds on this question
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)     REFERENCES users(id)          ON DELETE CASCADE,
    FOREIGN KEY (quiz_id)     REFERENCES quizzes(id)        ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES quiz_questions(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- LEADERBOARD VIEW (derived; also keep a materialized cache)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS leaderboard (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL UNIQUE,
    total_points INT NOT NULL DEFAULT 0,
    total_games  INT NOT NULL DEFAULT 0,
    win_rate     DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    rank_position INT,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- INDEXES for performance
-- ------------------------------------------------------------
CREATE INDEX idx_progress_user    ON student_progress(user_id);
CREATE INDEX idx_progress_type    ON student_progress(activity_type, activity_id);
CREATE INDEX idx_scores_user_quiz ON scores(user_id, quiz_id);
CREATE INDEX idx_quiz_subject     ON quizzes(subject_id);
CREATE INDEX idx_puzzle_subject   ON puzzles(subject_id);

-- ============================================================
-- END OF SCHEMA
-- ============================================================
