import sqlite3

import config as cfg
from utils.password import hash_password
from utils.helpers import now_iso


# ==========================================
# CREATE DATABASE CONNECTION
# ==========================================

def get_connection():
    conn = sqlite3.connect(cfg.DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- USERS TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'Student',
            created_at TEXT NOT NULL
        )
    """)

    # ---------------- TOPIC PROGRESS TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            module_id INTEGER NOT NULL,
            topic_id INTEGER NOT NULL,
            completed INTEGER DEFAULT 0,
            updated_at TEXT NOT NULL,
            UNIQUE(user_id, module_id, topic_id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # ---------------- QUIZ SCORES TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            module_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            taken_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # ---------------- CERTIFICATES TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            certificate_type TEXT NOT NULL,
            module_id INTEGER,
            file_path TEXT,
            issued_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # ==========================================
    # DEFAULT DEMO ACCOUNTS
    # ==========================================

    admin = cursor.execute(
        "SELECT id FROM users WHERE username=?", ("admin",)
    ).fetchone()

    if not admin:
        cursor.execute(
            """INSERT INTO users(username, email, password_hash, role, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            ("admin", "admin@pythonhub.local", hash_password("Admin@123"), "Admin", now_iso())
        )

    student = cursor.execute(
        "SELECT id FROM users WHERE username=?", ("student",)
    ).fetchone()

    if not student:
        cursor.execute(
            """INSERT INTO users(username, email, password_hash, role, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            ("student", "student@pythonhub.local", hash_password("Student@123"), "Student", now_iso())
        )

    conn.commit()
    conn.close()


# ==========================================
# AUTH QUERIES
# ==========================================

def find_user(username_or_email):
    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username=? OR email=?",
        (username_or_email, username_or_email)
    ).fetchone()
    conn.close()
    return user


def create_user(username, email, password_hash, role="Student"):
    conn = get_connection()
    conn.execute(
        """INSERT INTO users(username, email, password_hash, role, created_at)
           VALUES (?, ?, ?, ?, ?)""",
        (username, email, password_hash, role, now_iso())
    )
    conn.commit()
    conn.close()


# ==========================================
# PROGRESS QUERIES
# ==========================================

def mark_topic_complete(user_id, module_id, topic_id):
    conn = get_connection()
    conn.execute(
        """INSERT INTO progress(user_id, module_id, topic_id, completed, updated_at)
           VALUES (?, ?, ?, 1, ?)
           ON CONFLICT(user_id, module_id, topic_id)
           DO UPDATE SET completed=1, updated_at=excluded.updated_at""",
        (user_id, module_id, topic_id, now_iso())
    )
    conn.commit()
    conn.close()


def get_completed_topic_ids(user_id, module_id):
    conn = get_connection()
    rows = conn.execute(
        """SELECT topic_id FROM progress
           WHERE user_id=? AND module_id=? AND completed=1""",
        (user_id, module_id)
    ).fetchall()
    conn.close()
    return {row["topic_id"] for row in rows}


def get_all_progress_counts(user_id):
    """Returns {module_id: completed_topic_count} for a user."""
    conn = get_connection()
    rows = conn.execute(
        """SELECT module_id, COUNT(*) as completed_count FROM progress
           WHERE user_id=? AND completed=1
           GROUP BY module_id""",
        (user_id,)
    ).fetchall()
    conn.close()
    return {row["module_id"]: row["completed_count"] for row in rows}


# ==========================================
# QUIZ SCORE QUERIES
# ==========================================

def save_quiz_score(user_id, module_id, score, total):
    conn = get_connection()
    conn.execute(
        """INSERT INTO quiz_scores(user_id, module_id, score, total, taken_at)
           VALUES (?, ?, ?, ?, ?)""",
        (user_id, module_id, score, total, now_iso())
    )
    conn.commit()
    conn.close()


def get_best_quiz_score(user_id, module_id):
    """Returns (score, total, taken_at) for the user's best attempt, or None."""
    conn = get_connection()
    row = conn.execute(
        """SELECT score, total, taken_at FROM quiz_scores
           WHERE user_id=? AND module_id=?
           ORDER BY (score * 1.0 / total) DESC LIMIT 1""",
        (user_id, module_id)
    ).fetchone()
    conn.close()
    if not row:
        return None
    return row["score"], row["total"], row["taken_at"]


def get_all_best_scores(user_id):
    """Returns {module_id: (score, total, taken_at)} for a user's best attempts."""
    conn = get_connection()
    rows = conn.execute(
        """SELECT module_id, score, total, taken_at FROM quiz_scores
           WHERE user_id=?""",
        (user_id,)
    ).fetchall()
    conn.close()

    best = {}
    for row in rows:
        mid = row["module_id"]
        pct = row["score"] / row["total"] if row["total"] else 0
        if mid not in best or pct > (best[mid][0] / best[mid][1]):
            best[mid] = (row["score"], row["total"], row["taken_at"])
    return best


# ==========================================
# CERTIFICATE QUERIES
# ==========================================

def has_certificate(user_id, certificate_type, module_id=None):
    conn = get_connection()
    row = conn.execute(
        """SELECT id FROM certificates
           WHERE user_id=? AND certificate_type=? AND
                 (module_id=? OR (? IS NULL AND module_id IS NULL))""",
        (user_id, certificate_type, module_id, module_id)
    ).fetchone()
    conn.close()
    return row is not None


def issue_certificate(user_id, certificate_type, module_id, file_path):
    conn = get_connection()
    conn.execute(
        """INSERT INTO certificates(user_id, certificate_type, module_id, file_path, issued_at)
           VALUES (?, ?, ?, ?, ?)""",
        (user_id, certificate_type, module_id, file_path, now_iso())
    )
    conn.commit()
    conn.close()


def get_user_certificates(user_id):
    conn = get_connection()
    rows = conn.execute(
        """SELECT * FROM certificates WHERE user_id=? ORDER BY issued_at DESC""",
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


# ==========================================
# ADMIN QUERIES
# ==========================================

def count_users_by_role(role):
    conn = get_connection()
    row = conn.execute(
        "SELECT COUNT(*) as c FROM users WHERE role=?", (role,)
    ).fetchone()
    conn.close()
    return row["c"]


def get_all_students():
    """Every user with the 'Student' role, newest signups first."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM users WHERE role=? ORDER BY created_at DESC", ("Student",)
    ).fetchall()
    conn.close()
    return rows


def count_all_certificates():
    conn = get_connection()
    row = conn.execute("SELECT COUNT(*) as c FROM certificates").fetchone()
    conn.close()
    return row["c"]


def count_certificates_by_type(certificate_type):
    conn = get_connection()
    row = conn.execute(
        "SELECT COUNT(*) as c FROM certificates WHERE certificate_type=?",
        (certificate_type,)
    ).fetchone()
    conn.close()
    return row["c"]


# ==========================================
# TEST DATABASE
# ==========================================

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")
    print("Database location:", cfg.DB_FILE)
