# ============================================================
# EduQuest - SQLite Database Connection Utility
# ============================================================
import sqlite3
import os
from config import config
import logging

logger = logging.getLogger(__name__)

def get_connection():
    """Establish a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(config.DB_PATH)
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        # Ensure results are returned as dictionaries (row factories)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

def _convert_query(query):
    """Convert MySQL-style placeholders (%s) to SQLite (?) style."""
    return query.replace('%s', '?')

def execute_query(query, params=None, fetch=False, fetchone=False, lastrowid=False):
    """
    Execute a parameterized SQL query.
    """
    conn = None
    cursor = None
    query = _convert_query(query)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())

        if fetch:
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            conn.commit()
            return result
        elif fetchone:
            row = cursor.fetchone()
            result = dict(row) if row else None
            conn.commit()
            return result
        elif lastrowid:
            conn.commit()
            return cursor.lastrowid
        else:
            conn.commit()
            return cursor.rowcount

    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Query execution error: {e}\nQuery: {query}\nParams: {params}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def execute_many(query, params_list):
    """Execute the same query with multiple parameter sets."""
    conn = None
    cursor = None
    query = _convert_query(query)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.executemany(query, params_list)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Batch execution error: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def test_connection():
    """Verify DB connectivity."""
    try:
        if not os.path.exists(os.path.dirname(config.DB_PATH)):
            os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return True, "Connected to SQLite database"
    except Exception as e:
        return False, str(e)
