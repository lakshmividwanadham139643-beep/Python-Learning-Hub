import sqlite3
import tkinter as tk
from tkinter import messagebox

import config as cfg
from utils.helpers import center_window, make_button


# ==========================================
# MINI APPLICATION — Student Records CRUD (real SQLite table)
# ==========================================

def _get_mini_app_connection():
    conn = sqlite3.connect(cfg.DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mini_app_students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def launch_mini_app(parent):
    """A real CRUD app against its own SQLite table — demonstrates
    connecting, CREATE TABLE, INSERT, SELECT, UPDATE, DELETE."""

    win = tk.Toplevel(parent)
    win.title("Mini App — Student Records (SQLite CRUD)")
    win.configure(bg=cfg.WHITE)
    center_window(win, 500, 560)
    win.resizable(False, False)

    tk.Label(
        win, text="🗄️ Student Records (SQLite)", bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_H3
    ).pack(pady=(20, 10))

    form = tk.Frame(win, bg=cfg.WHITE)
    form.pack(fill="x", padx=20)

    name_var = tk.StringVar()
    grade_var = tk.StringVar()

    tk.Label(form, text="Name", bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_SMALL).grid(row=0, column=0, sticky="w")
    tk.Entry(form, textvariable=name_var, font=cfg.FONT_BODY).grid(row=1, column=0, sticky="ew", padx=(0, 8))

    tk.Label(form, text="Grade", bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_SMALL).grid(row=0, column=1, sticky="w")
    tk.Entry(form, textvariable=grade_var, font=cfg.FONT_BODY, width=8).grid(row=1, column=1, sticky="ew")

    form.columnconfigure(0, weight=1)

    listbox = tk.Listbox(win, font=cfg.FONT_BODY, bd=0, highlightthickness=1, highlightbackground=cfg.BORDER)
    listbox.pack(fill="both", expand=True, padx=20, pady=15)

    row_ids = []  # keeps id aligned with each visual listbox row

    def refresh():
        conn = _get_mini_app_connection()
        rows = conn.execute("SELECT id, name, grade FROM mini_app_students ORDER BY name").fetchall()
        conn.close()

        listbox.delete(0, tk.END)
        row_ids.clear()

        for r in rows:
            listbox.insert(tk.END, f"#{r[0]:<4} {r[1]:<20} Grade {r[2]}")
            row_ids.append(r[0])

    def create_record():
        name = name_var.get().strip()
        grade = grade_var.get().strip()
        if not name or not grade:
            messagebox.showwarning("Missing info", "Enter both name and grade.", parent=win)
            return

        conn = _get_mini_app_connection()
        conn.execute(
            "INSERT INTO mini_app_students (name, grade) VALUES (?, ?)",
            (name, grade)
        )
        conn.commit()
        conn.close()

        name_var.set("")
        grade_var.set("")
        refresh()

    def update_selected():
        selection = listbox.curselection()
        if not selection:
            messagebox.showinfo("Select a row", "Click a record in the list first.", parent=win)
            return

        name = name_var.get().strip()
        grade = grade_var.get().strip()
        if not name or not grade:
            messagebox.showwarning("Missing info", "Enter both name and grade to update.", parent=win)
            return

        record_id = row_ids[selection[0]]

        conn = _get_mini_app_connection()
        conn.execute(
            "UPDATE mini_app_students SET name=?, grade=? WHERE id=?",
            (name, grade, record_id)
        )
        conn.commit()
        conn.close()
        refresh()

    def delete_selected():
        selection = listbox.curselection()
        if not selection:
            return

        record_id = row_ids[selection[0]]

        conn = _get_mini_app_connection()
        conn.execute("DELETE FROM mini_app_students WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        refresh()

    def on_select(event):
        selection = listbox.curselection()
        if not selection:
            return
        record_id = row_ids[selection[0]]

        conn = _get_mini_app_connection()
        row = conn.execute(
            "SELECT name, grade FROM mini_app_students WHERE id=?", (record_id,)
        ).fetchone()
        conn.close()

        if row:
            name_var.set(row[0])
            grade_var.set(row[1])

    listbox.bind("<<ListboxSelect>>", on_select)

    btn_row1 = tk.Frame(win, bg=cfg.WHITE)
    btn_row1.pack(fill="x", padx=20)
    make_button(btn_row1, "➕ Create", create_record, cfg.GREEN).pack(side="left", expand=True, fill="x", padx=2)
    make_button(btn_row1, "✏️ Update Selected", update_selected, cfg.BLUE).pack(side="left", expand=True, fill="x", padx=2)

    btn_row2 = tk.Frame(win, bg=cfg.WHITE)
    btn_row2.pack(fill="x", padx=20, pady=(8, 20))
    make_button(btn_row2, "🗑️ Delete Selected", delete_selected, cfg.RED).pack(fill="x")

    refresh()


# ==========================================
# MODULE CONTENT
# ==========================================

MODULE = {
    "id": 6,
    "title": "Database Connectivity",
    "description": "Connect Python to a real database and build data-driven, persistent applications.",
    "topics": [
        {
            "id": 1,
            "title": "Database Introduction",
            "theory": "A database stores structured data permanently, in a way that's fast to search, filter, and update — far more capable than plain text files for anything relational (users, orders, records that reference each other). Databases are organized into tables, similar to spreadsheets, with rows (records) and columns (fields).",
            "key_points": [
                "Databases store structured, searchable, persistent data.",
                "Organized into tables — rows are records, columns are fields.",
                "Much more capable than flat text files for relational data.",
                "SQL (Structured Query Language) is how you talk to most databases.",
                "This whole platform's users/progress/quizzes live in a database."
            ],
            "code_example": "# A table conceptually looks like:\n# id | username  | role\n# ---|-----------|--------\n# 1  | admin     | Admin\n# 2  | student   | Student",
        },
        {
            "id": 2,
            "title": "SQLite",
            "theory": "SQLite is a lightweight, file-based database engine built into Python's standard library via the `sqlite3` module — no server or separate installation needed. The entire database lives in one `.db` file, making it perfect for desktop apps, prototypes, and small-to-medium projects, exactly like this platform.",
            "key_points": [
                "Built into Python — 'import sqlite3', no install needed.",
                "The whole database is a single .db file.",
                "No separate server process required, unlike MySQL/PostgreSQL.",
                "Great for desktop apps, prototypes, and learning SQL.",
                "This platform's data lives at data/python_learning_hub.db"
            ],
            "code_example": "import sqlite3\n\nconn = sqlite3.connect(\"my_app.db\")\ncursor = conn.cursor()\nprint(\"Connected to SQLite!\")\nconn.close()",
        },
        {
            "id": 3,
            "title": "MySQL Introduction",
            "theory": "MySQL is a full client-server database system — unlike SQLite, it runs as a separate server process that multiple applications and users can connect to over a network. It's the typical choice once an app grows beyond a single desktop user, needing concurrent access from many clients (e.g. a website's backend).\n\nPython connects to it using a driver library such as `mysql-connector-python` or `PyMySQL` (not built-in, unlike sqlite3).",
            "key_points": [
                "MySQL is a client-server database — runs as its own service.",
                "Supports many simultaneous connections/users, unlike SQLite.",
                "Needs a separate driver: mysql-connector-python or PyMySQL.",
                "Typical choice for websites and multi-user backend systems.",
                "Same SQL concepts (tables, INSERT, SELECT) apply as in SQLite."
            ],
            "code_example": "# Requires: pip install mysql-connector-python\nimport mysql.connector\n\nconn = mysql.connector.connect(\n    host=\"localhost\", user=\"root\", password=\"...\", database=\"my_db\"\n)\nprint(\"Connected to MySQL!\")",
        },
        {
            "id": 4,
            "title": "Connecting Python to Database",
            "theory": "`sqlite3.connect(path)` opens (or creates) a database file and returns a connection object. From that connection you get a `cursor` — the object you use to actually execute SQL statements. Always close the connection when done, or use it inside a `try/finally` (or `with`) to guarantee it closes.",
            "key_points": [
                "sqlite3.connect(path) opens/creates the .db file.",
                "conn.cursor() gives you the object to run SQL through.",
                "cursor.execute(sql) runs a single SQL statement.",
                "conn.commit() saves changes; without it, writes can be lost.",
                "conn.close() releases the connection when you're done."
            ],
            "code_example": "import sqlite3\n\nconn = sqlite3.connect(\"school.db\")\ncursor = conn.cursor()\n\ncursor.execute(\"SELECT 1\")\nprint(cursor.fetchone())\n\nconn.close()",
        },
        {
            "id": 5,
            "title": "Creating Tables",
            "theory": "`CREATE TABLE IF NOT EXISTS` defines a new table's structure — its columns and their types (`INTEGER`, `TEXT`, `REAL`, etc.) — without erroring if it already exists, which makes your setup code safely re-runnable. `PRIMARY KEY AUTOINCREMENT` gives each row a unique, self-incrementing ID automatically.",
            "key_points": [
                "CREATE TABLE IF NOT EXISTS avoids errors on re-run.",
                "Common types: INTEGER, TEXT, REAL, BLOB.",
                "PRIMARY KEY AUTOINCREMENT gives each row a unique auto ID.",
                "NOT NULL requires a column to always have a value.",
                "UNIQUE ensures no two rows share that column's value."
            ],
            "code_example": "cursor.execute(\"\"\"\n    CREATE TABLE IF NOT EXISTS students (\n        id INTEGER PRIMARY KEY AUTOINCREMENT,\n        name TEXT NOT NULL,\n        grade TEXT NOT NULL\n    )\n\"\"\")\nconn.commit()",
        },
        {
            "id": 6,
            "title": "INSERT",
            "theory": "`INSERT INTO table (columns) VALUES (...)` adds a new row. You should always use `?` placeholders for values (parameterized queries — covered in depth later in this module) rather than pasting values directly into the SQL string, which prevents both bugs and SQL injection attacks.",
            "key_points": [
                "INSERT INTO table (col1, col2) VALUES (?, ?)",
                "Always use ? placeholders, never string-format values in.",
                "Pass the actual values as a tuple, the second argument.",
                "Remember conn.commit() after inserting, or it won't save.",
                "AUTOINCREMENT columns don't need a value supplied."
            ],
            "code_example": "cursor.execute(\n    \"INSERT INTO students (name, grade) VALUES (?, ?)\",\n    (\"Ana\", \"A\")\n)\nconn.commit()\nprint(\"New row id:\", cursor.lastrowid)",
        },
        {
            "id": 7,
            "title": "SELECT",
            "theory": "`SELECT columns FROM table WHERE condition` retrieves rows. `fetchone()` gets a single matching row, `fetchall()` gets every matching row as a list, and `WHERE` filters which rows come back — without it, every row in the table is returned.",
            "key_points": [
                "SELECT * FROM table gets every column of every row.",
                "WHERE condition filters which rows are returned.",
                "fetchone() gets a single row; fetchall() gets all matches.",
                "ORDER BY column sorts the results.",
                "Filter values should still use ? placeholders."
            ],
            "code_example": "cursor.execute(\"SELECT * FROM students WHERE grade = ?\", (\"A\",))\ntop_students = cursor.fetchall()\n\nfor row in top_students:\n    print(row)",
        },
        {
            "id": 8,
            "title": "UPDATE",
            "theory": "`UPDATE table SET column=value WHERE condition` modifies existing rows. The `WHERE` clause is critical — omitting it updates every single row in the table, which is rarely what you want.",
            "key_points": [
                "UPDATE table SET col=? WHERE condition",
                "WHERE targets exactly which row(s) to change.",
                "Forgetting WHERE updates ALL rows — always double-check it.",
                "Multiple columns: SET col1=?, col2=? WHERE id=?",
                "Requires conn.commit() to persist the change."
            ],
            "code_example": "cursor.execute(\n    \"UPDATE students SET grade = ? WHERE name = ?\",\n    (\"A+\", \"Ana\")\n)\nconn.commit()\nprint(\"Rows updated:\", cursor.rowcount)",
        },
        {
            "id": 9,
            "title": "DELETE",
            "theory": "`DELETE FROM table WHERE condition` removes rows permanently. Just like `UPDATE`, forgetting the `WHERE` clause deletes every row in the table — always double check your condition before running a DELETE, ideally testing the same condition with a SELECT first.",
            "key_points": [
                "DELETE FROM table WHERE condition",
                "No WHERE = every row in the table is deleted.",
                "Deletions are permanent — no built-in undo.",
                "Good practice: SELECT the same WHERE first to preview.",
                "Requires conn.commit() to persist."
            ],
            "code_example": "# Preview first!\ncursor.execute(\"SELECT * FROM students WHERE grade = 'F'\")\nprint(cursor.fetchall())\n\ncursor.execute(\"DELETE FROM students WHERE grade = ?\", (\"F\",))\nconn.commit()",
        },
        {
            "id": 10,
            "title": "CRUD Application",
            "theory": "CRUD stands for Create, Read, Update, Delete — the four fundamental operations of any data-driven app. The Mini App above is a complete, working CRUD application: adding a student is Create, the list view is Read, editing a selected row is Update, and the delete button is Delete — all against a real SQLite table.",
            "key_points": [
                "CRUD = Create, Read, Update, Delete.",
                "Nearly every real app is built around these four operations.",
                "The Mini App above demonstrates all four, live.",
                "Good CRUD apps always validate input before writing to the DB.",
                "Refreshing the displayed list after every change keeps the UI in sync."
            ],
            "code_example": "# The four CRUD operations, side by side:\ncursor.execute(\"INSERT INTO students (name, grade) VALUES (?, ?)\", (\"Raj\", \"B\"))  # Create\ncursor.execute(\"SELECT * FROM students\")                                          # Read\ncursor.execute(\"UPDATE students SET grade = ? WHERE name = ?\", (\"A\", \"Raj\"))       # Update\ncursor.execute(\"DELETE FROM students WHERE name = ?\", (\"Raj\",))                    # Delete\nconn.commit()",
        },
        {
            "id": 11,
            "title": "Parameterized Queries",
            "theory": "A parameterized query uses `?` placeholders instead of directly inserting values into the SQL string with string concatenation or f-strings. This is not just style — building SQL with f-strings is vulnerable to SQL injection, where malicious input can alter the query's meaning entirely. Every query in this platform's database.py uses `?` placeholders for exactly this reason.",
            "key_points": [
                "Never build SQL with f-strings/concatenation of user input.",
                "Always use ? placeholders, values passed as a separate tuple.",
                "Prevents SQL injection — a serious, common security flaw.",
                "sqlite3 automatically escapes values passed this way.",
                "This rule applies to EVERY value from a user, no exceptions."
            ],
            "code_example": "# DANGEROUS — never do this:\n# cursor.execute(f\"SELECT * FROM users WHERE username = '{user_input}'\")\n\n# SAFE — always do this:\ncursor.execute(\"SELECT * FROM users WHERE username = ?\", (user_input,))",
        },
        {
            "id": 12,
            "title": "Login System",
            "theory": "A login system checks submitted credentials against stored user records — but storing plain-text passwords is a serious security risk. Passwords should always be hashed (this platform uses salted PBKDF2 via `utils/password.py`) before storing, and verified by hashing the login attempt the same way and comparing.\n\nThis platform's own login screen (ui/login.py) is a working, complete example of exactly this pattern.",
            "key_points": [
                "Never store passwords as plain text.",
                "Hash passwords before storing; verify by re-hashing on login.",
                "This platform hashes with salted PBKDF2 (utils/password.py).",
                "Login queries use ? placeholders — same rule as always.",
                "See ui/login.py in this project for the complete working version."
            ],
            "code_example": "# Simplified concept (see utils/password.py for the real version)\nimport hashlib\n\ndef check_login(cursor, username, password):\n    cursor.execute(\"SELECT password_hash FROM users WHERE username=?\", (username,))\n    row = cursor.fetchone()\n    if not row:\n        return False\n    return hashlib.sha256(password.encode()).hexdigest() == row[0]",
        },
        {
            "id": 13,
            "title": "Progress Database",
            "theory": "This platform tracks your learning progress the same way — a `progress` table records which topics you've completed, a `quiz_scores` table records every quiz attempt, and a `certificates` table records what you've earned. Every checkbox you tick and every quiz you submit runs an INSERT or UPDATE exactly like the ones you just learned.",
            "key_points": [
                "progress table: tracks completed topics per user/module.",
                "quiz_scores table: records every quiz attempt and score.",
                "certificates table: records earned module/final certificates.",
                "Every 'Mark Complete' click runs a real INSERT/UPDATE.",
                "Check database.py in this project to see the real schema."
            ],
            "code_example": "# From this platform's own database.py (simplified):\ncursor.execute(\"\"\"\n    INSERT INTO progress(user_id, module_id, topic_id, completed, updated_at)\n    VALUES (?, ?, ?, 1, ?)\n    ON CONFLICT(user_id, module_id, topic_id)\n    DO UPDATE SET completed=1\n\"\"\", (user_id, module_id, topic_id, updated_at))",
        },
    ],
    "quiz": [
        {"question": "What does SQLite store a whole database as?", "options": ["Multiple server files", "A single .db file", "A cloud service", "A Python object only"], "answer_index": 1},
        {"question": "Which module gives Python built-in SQLite support?", "options": ["mysql", "sqlite3", "database", "sql"], "answer_index": 1},
        {"question": "What's the main difference between MySQL and SQLite?", "options": ["MySQL is file-based, SQLite is a server", "MySQL runs as a server, supports many connections", "They are identical", "SQLite is faster for websites"], "answer_index": 1},
        {"question": "What does conn.commit() do?", "options": ["Closes the connection", "Saves pending changes to the database", "Deletes all rows", "Creates a new table"], "answer_index": 1},
        {"question": "Which SQL statement creates a new table?", "options": ["MAKE TABLE", "NEW TABLE", "CREATE TABLE", "ADD TABLE"], "answer_index": 2},
        {"question": "Why should you use ? placeholders instead of f-strings in SQL?", "options": ["It's faster to type", "Prevents SQL injection", "It's required syntax", "It looks cleaner only"], "answer_index": 1},
        {"question": "What happens if you run UPDATE without a WHERE clause?", "options": ["Nothing changes", "Only the first row updates", "Every row in the table updates", "It raises an error"], "answer_index": 2},
        {"question": "What does CRUD stand for?", "options": ["Create, Run, Undo, Delete", "Create, Read, Update, Delete", "Connect, Read, Use, Debug", "Copy, Read, Update, Duplicate"], "answer_index": 1},
        {"question": "Why should passwords never be stored as plain text?", "options": ["It uses more storage", "It's a serious security risk if the database leaks", "SQLite doesn't support text", "It slows down login"], "answer_index": 1},
        {"question": "Which method retrieves all matching rows from a SELECT?", "options": ["fetchone()", "fetchall()", "getrows()", "selectall()"], "answer_index": 1},
    ],
    "mini_app": {
        "title": "Student Records (SQLite CRUD)",
        "description": "A full Create/Read/Update/Delete app against a real SQLite table in this project's own database file.",
        "launch": launch_mini_app,
    },
}
