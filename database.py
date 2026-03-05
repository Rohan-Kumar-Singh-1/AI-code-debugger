import sqlite3
from datetime import datetime

DB_NAME = "sessions.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# Initialize Database
# -------------------------

def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Sessions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        bug_report TEXT,
        original_code TEXT,
        generated_fix TEXT,
        tests TEXT,
        test_result TEXT,
        timestamp TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


# -------------------------
# User Authentication
# -------------------------

def create_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        success = True
    except:
        success = False

    conn.close()
    return success


def authenticate_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    return user


# -------------------------
# Session Management
# -------------------------

def save_session(user_id, bug_report, code, fix, tests, test_result):

    conn = get_connection()
    cursor = conn.cursor()

    title = bug_report.strip().split("\n")[0][:60]

    cursor.execute("""
    INSERT INTO sessions (
        user_id,
        title,
        bug_report,
        original_code,
        generated_fix,
        tests,
        test_result,
        timestamp
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        title,
        bug_report,
        code,
        fix,
        tests,
        test_result,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_sessions(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, title, timestamp
    FROM sessions
    WHERE user_id=?
    ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_session_by_id(session_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM sessions WHERE id=?",
        (session_id,)
    )

    row = cursor.fetchone()
    conn.close()

    return row