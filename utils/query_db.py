
import sqlite3
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import config

def query(sql_command):
    try:
        conn = sqlite3.connect(config.DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql_command)
        
        if sql_command.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            if not rows:
                print("No results found.")
                return
            
            # Print headers
            headers = rows[0].keys()
            print(" | ".join(headers))
            print("-" * (len(" | ".join(headers)) + 2))
            
            # Print rows
            for row in rows:
                print(" | ".join(str(row[h]) for h in headers))
        else:
            conn.commit()
            print(f"Executed successfully. Rows affected: {cursor.rowcount}")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sql = " ".join(sys.argv[1:])
        query(sql)
    else:
        print("Usage: python query_db.py \"SELECT * FROM STUDENT\"")
        print("\nAvailable tables: STUDENT, TEACHER, COURSE, ENROLL, QUIZ, PUZZLE, SCRAMBLE, BADGE, LEADERBOARD, LOGIN")
