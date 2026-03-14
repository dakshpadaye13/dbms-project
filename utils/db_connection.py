# ============================================================
# LearnQuest AI - MySQL Database Connection Utility
# ============================================================
import mysql.connector
from mysql.connector import Error, pooling
from config import config
import logging

logger = logging.getLogger(__name__)

# Connection pool for efficiency
_pool = None


def init_pool():
    """Initialize a MySQL connection pool."""
    global _pool
    try:
        _pool = pooling.MySQLConnectionPool(
            pool_name="learnquest_pool",
            pool_size=5,
            host=config.MYSQL_HOST,
            port=config.MYSQL_PORT,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            charset=config.MYSQL_CHARSET,
            autocommit=False
        )
        logger.info("MySQL connection pool created successfully.")
    except Error as e:
        logger.error(f"Error creating connection pool: {e}")
        _pool = None


def get_connection():
    """
    Retrieve a connection from the pool.
    Falls back to a direct connection if pool is unavailable.
    """
    global _pool
    if _pool is None:
        init_pool()
    try:
        if _pool:
            return _pool.get_connection()
        # Fallback: direct connection
        return mysql.connector.connect(
            host=config.MYSQL_HOST,
            port=config.MYSQL_PORT,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            charset=config.MYSQL_CHARSET
        )
    except Error as e:
        logger.error(f"Database connection error: {e}")
        raise


def execute_query(query, params=None, fetch=False, fetchone=False, lastrowid=False):
    """
    Execute a parameterized SQL query.

    Args:
        query     (str): SQL query string with %s placeholders.
        params   (tuple): Optional query parameters.
        fetch    (bool): Fetch all results.
        fetchone (bool): Fetch a single result.
        lastrowid(bool): Return the last inserted row id.

    Returns:
        Query results or row id depending on flags.
    """
    conn = None
    cursor = None
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())

        if fetch:
            result = cursor.fetchall()
            conn.commit()
            return result
        elif fetchone:
            result = cursor.fetchone()
            conn.commit()
            return result
        elif lastrowid:
            conn.commit()
            return cursor.lastrowid
        else:
            conn.commit()
            return cursor.rowcount

    except Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Query execution error: {e}\nQuery: {query}\nParams: {params}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def execute_many(query, params_list):
    """Execute the same query with multiple parameter sets (batch insert/update)."""
    conn = None
    cursor = None
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.executemany(query, params_list)
        conn.commit()
        return cursor.rowcount
    except Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Batch execution error: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def test_connection():
    """Verify DB connectivity - used on startup."""
    try:
        conn = get_connection()
        if conn.is_connected():
            info = conn.get_server_info()
            conn.close()
            return True, f"Connected to MySQL Server version {info}"
    except Error as e:
        return False, str(e)
