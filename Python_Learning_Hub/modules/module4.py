import os
import tkinter as tk
from tkinter import messagebox

import config as cfg
from utils.helpers import center_window, make_button

NOTES_FILE = os.path.join(cfg.DATA_FOLDER, "mini_app_notes.txt")


# ==========================================
# MINI APPLICATION — Notes App (real file I/O)
# ==========================================

def launch_mini_app(parent):
    """A notes app that actually reads/writes a text file on disk —
    demonstrates file modes, reading, writing, and exception handling."""

    win = tk.Toplevel(parent)
    win.title("Mini App — Notes App (File Storage)")
    win.configure(bg=cfg.WHITE)
    center_window(win, 480, 520)
    win.resizable(False, False)

    tk.Label(
        win, text="📁 Notes App", bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_H3
    ).pack(pady=(20, 4))

    tk.Label(
        win, text=f"Saved to: {NOTES_FILE}", bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_SMALL
    ).pack(pady=(0, 15))

    text_area = tk.Text(win, font=cfg.FONT_BODY, wrap="word", bd=1, relief="solid")
    text_area.pack(fill="both", expand=True, padx=20)

    status = tk.Label(win, text="", bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_SMALL)
    status.pack(pady=(6, 0))

    def load_notes():
        try:
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, content)
            status.configure(text="Notes loaded from file.", fg=cfg.GREEN)
        except FileNotFoundError:
            status.configure(text="No saved notes yet — write something and save!", fg=cfg.MUTED)
        except OSError as e:
            status.configure(text=f"Could not read file: {e}", fg=cfg.RED)

    def save_notes():
        try:
            with open(NOTES_FILE, "w", encoding="utf-8") as f:
                f.write(text_area.get("1.0", tk.END).strip())
            status.configure(text="✅ Notes saved to disk.", fg=cfg.GREEN)
        except OSError as e:
            status.configure(text=f"Could not save file: {e}", fg=cfg.RED)

    def append_note():
        note = text_area.get("1.0", tk.END).strip()
        if not note:
            messagebox.showinfo("Nothing to append", "Write something first.", parent=win)
            return
        try:
            with open(NOTES_FILE, "a", encoding="utf-8") as f:
                f.write("\n" + note)
            status.configure(text="➕ Appended to existing file.", fg=cfg.GREEN)
        except OSError as e:
            status.configure(text=f"Could not append: {e}", fg=cfg.RED)

    btn_row = tk.Frame(win, bg=cfg.WHITE)
    btn_row.pack(fill="x", padx=20, pady=20)

    make_button(btn_row, "📂 Load", load_notes, cfg.NAVY2).pack(side="left", expand=True, fill="x", padx=2)
    make_button(btn_row, "💾 Save (overwrite)", save_notes, cfg.BLUE).pack(side="left", expand=True, fill="x", padx=2)
    make_button(btn_row, "➕ Append", append_note, cfg.GREEN).pack(side="left", expand=True, fill="x", padx=2)

    load_notes()


# ==========================================
# MODULE CONTENT
# ==========================================

MODULE = {
    "id": 4,
    "title": "File & Exception Handling",
    "description": "Read and write real files safely, and handle errors gracefully instead of crashing.",
    "topics": [
        {
            "id": 1,
            "title": "File Introduction",
            "theory": "Files let a program store data permanently, beyond a single run — unlike variables, which disappear when the program ends. Python's built-in `open()` function is the gateway to reading and writing files of any kind: text, CSV, logs, and more.\n\nA file must be opened, used, then closed — leaving files open wastes resources and can lose unsaved data.",
            "key_points": [
                "Files persist data beyond a single program run.",
                "open(path, mode) is the entry point for file access.",
                "Always close a file when done (or use 'with', see below).",
                "Text files store readable characters; binary stores raw bytes.",
                "File paths can be relative or absolute."
            ],
            "code_example": "f = open(\"notes.txt\", \"w\")\nf.write(\"Hello, file!\")\nf.close()  # must close, or changes may not save",
        },
        {
            "id": 2,
            "title": "File Modes",
            "theory": "The second argument to `open()` is the mode: `\"r\"` reads (file must exist), `\"w\"` writes and overwrites/creates, `\"a\"` appends to the end without erasing existing content, and `\"x\"` creates a file but fails if it already exists. Add `\"b\"` for binary mode.",
            "key_points": [
                "'r' = read (error if file doesn't exist).",
                "'w' = write, overwrites the whole file (creates if missing).",
                "'a' = append, adds to the end without erasing.",
                "'x' = create new, fails if the file already exists.",
                "'rb' / 'wb' work in binary mode for non-text files."
            ],
            "code_example": "open(\"data.txt\", \"r\")   # read\nopen(\"data.txt\", \"w\")   # overwrite/create\nopen(\"data.txt\", \"a\")   # append\nopen(\"image.png\", \"rb\") # read binary",
        },
        {
            "id": 3,
            "title": "Reading Files",
            "theory": "Once opened in read mode, `.read()` returns the whole file as one string, `.readline()` reads a single line, and `.readlines()` returns a list of lines. Looping directly over the file object with `for line in f:` is the most memory-efficient way for large files.\n\nThe `with` statement is the preferred way to open files — it closes the file automatically, even if an error occurs inside the block.",
            "key_points": [
                "with open(path) as f: auto-closes the file, even on errors.",
                "f.read() returns the entire file as one string.",
                "f.readlines() returns a list, one string per line.",
                "for line in f: is memory-efficient for large files.",
                "Lines from readlines()/iteration keep their trailing newline."
            ],
            "code_example": "with open(\"data.txt\", \"r\") as f:\n    content = f.read()\n    print(content)\n\nwith open(\"data.txt\", \"r\") as f:\n    for line in f:\n        print(line.strip())",
        },
        {
            "id": 4,
            "title": "Writing Files",
            "theory": "`\"w\"` mode writes new content, completely replacing anything already in the file — if the file doesn't exist, it's created. Use `.write(text)` for a single string, or `.writelines(list_of_strings)` for many at once (note: it does not add newlines automatically between them).",
            "key_points": [
                "'w' mode replaces the entire file's contents.",
                ".write(text) writes one string exactly as given.",
                ".writelines(list) writes multiple strings back-to-back.",
                "You must add '\\n' yourself between lines if needed.",
                "Always use 'with' so the file is properly closed/saved."
            ],
            "code_example": "with open(\"report.txt\", \"w\") as f:\n    f.write(\"Learning Report\\n\")\n    f.write(\"================\\n\")\n    f.writelines([\"Line 1\\n\", \"Line 2\\n\"])",
        },
        {
            "id": 5,
            "title": "Appending Files",
            "theory": "`\"a\"` mode adds new content to the end of a file without erasing what's already there — perfect for logs, journals, or any growing record. If the file doesn't exist yet, append mode creates it, just like write mode.",
            "key_points": [
                "'a' mode preserves existing content, adds after it.",
                "Creates the file if it doesn't already exist.",
                "Ideal for logs, journals, and running histories.",
                "Each append call adds to the end, not the start.",
                "Remember to add '\\n' if you want each entry on its own line."
            ],
            "code_example": "with open(\"log.txt\", \"a\") as f:\n    f.write(\"User logged in\\n\")\n\n# Run this multiple times — each call adds a new line,\n# nothing gets overwritten.",
        },
        {
            "id": 6,
            "title": "CSV Files",
            "theory": "CSV (Comma-Separated Values) is a common plain-text format for tabular data — each line is a row, values separated by commas. Python's built-in `csv` module handles the tricky edge cases (commas inside quoted fields, etc.) so you don't parse it by hand.\n\n`csv.writer` writes rows; `csv.reader` reads them back as lists of strings; `csv.DictWriter`/`DictReader` work with dictionaries using column headers.",
            "key_points": [
                "CSV = plain text, comma-separated, one row per line.",
                "import csv; csv.writer(file).writerow([...])",
                "csv.reader(file) yields each row as a list of strings.",
                "DictReader/DictWriter map rows to/from dictionaries by header.",
                "Always open CSV files with newline='' to avoid blank rows."
            ],
            "code_example": "import csv\n\nwith open(\"scores.csv\", \"w\", newline=\"\") as f:\n    writer = csv.writer(f)\n    writer.writerow([\"Name\", \"Score\"])\n    writer.writerow([\"Ana\", 92])\n\nwith open(\"scores.csv\", \"r\", newline=\"\") as f:\n    for row in csv.reader(f):\n        print(row)",
        },
        {
            "id": 7,
            "title": "try",
            "theory": "A `try` block lets you run code that *might* fail, without crashing the whole program if it does. Python attempts everything inside `try`; if an error (exception) occurs, execution jumps straight to a matching `except` block instead of stopping the program.",
            "key_points": [
                "try: wraps code that might raise an exception.",
                "If no error occurs, except blocks are simply skipped.",
                "If an error occurs, execution jumps to a matching except.",
                "Without try/except, an error crashes the whole program.",
                "Only wrap the specific risky lines, not your whole program."
            ],
            "code_example": "try:\n    number = int(\"not a number\")\n    print(number)\nexcept ValueError:\n    print(\"That wasn't a valid number!\")\n\nprint(\"Program continues normally.\")",
        },
        {
            "id": 8,
            "title": "except",
            "theory": "`except` catches a specific type of error and lets you respond to it gracefully — show a friendly message, use a default value, or log the problem. You can have multiple `except` blocks for different error types, and a bare `except:` catches anything (use sparingly, since it can hide real bugs).",
            "key_points": [
                "except ErrorType: catches only that kind of error.",
                "Multiple except blocks can handle different errors differently.",
                "except Exception as e: lets you inspect the error message.",
                "A bare 'except:' catches everything — use it carefully.",
                "Order matters: put more specific exceptions first."
            ],
            "code_example": "try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print(\"Can't divide by zero!\")\nexcept ValueError as e:\n    print(f\"Value error: {e}\")",
        },
        {
            "id": 9,
            "title": "finally",
            "theory": "A `finally` block runs no matter what — whether the `try` succeeded, failed, or even hit a `return` — making it the right place for cleanup code like closing a file or a database connection. `finally` is optional but pairs well with resources that must always be released.",
            "key_points": [
                "finally: always executes, error or not.",
                "Ideal for cleanup — closing files, connections, etc.",
                "Runs even if the try/except block returns early.",
                "Optional — not every try/except needs a finally.",
                "'with' statements often make manual finally unnecessary for files."
            ],
            "code_example": "try:\n    f = open(\"data.txt\", \"r\")\n    print(f.read())\nexcept FileNotFoundError:\n    print(\"File not found!\")\nfinally:\n    print(\"Cleanup step always runs.\")",
        },
        {
            "id": 10,
            "title": "Custom Exceptions",
            "theory": "You can define your own exception types by creating a class that inherits from `Exception`. Custom exceptions make error handling more descriptive and specific to your program's rules — e.g. `InsufficientFundsError` is clearer than a generic `ValueError`.\n\nYou raise a custom exception with the `raise` keyword, and catch it just like a built-in one.",
            "key_points": [
                "class MyError(Exception): pass defines a custom exception.",
                "raise MyError('message') triggers it.",
                "Caught the same way: except MyError as e:",
                "Makes error handling specific to your program's domain.",
                "Custom exceptions can carry extra data via __init__."
            ],
            "code_example": "class InsufficientFundsError(Exception):\n    pass\n\ndef withdraw(balance, amount):\n    if amount > balance:\n        raise InsufficientFundsError(\"Not enough balance!\")\n    return balance - amount\n\ntry:\n    withdraw(100, 500)\nexcept InsufficientFundsError as e:\n    print(e)",
        },
        {
            "id": 11,
            "title": "Logging",
            "theory": "The built-in `logging` module is a more capable alternative to scattering `print()` statements — it supports severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL), timestamps, and writing to a file instead of just the console, which is exactly what production apps need.",
            "key_points": [
                "logging has severity levels: DEBUG < INFO < WARNING < ERROR < CRITICAL.",
                "logging.basicConfig(filename=...) sends logs to a file.",
                "Unlike print(), logs include timestamps and severity automatically.",
                "Levels let you filter noise — show only WARNING and above in production.",
                "This app writes its own logs to the logs/ folder."
            ],
            "code_example": "import logging\n\nlogging.basicConfig(\n    filename=\"app.log\",\n    level=logging.INFO,\n    format=\"%(asctime)s - %(levelname)s - %(message)s\"\n)\n\nlogging.info(\"Application started\")\nlogging.warning(\"Low disk space\")\nlogging.error(\"Failed to save file\")",
        },
        {
            "id": 12,
            "title": "Practice Project",
            "theory": "Build a 'Safe File Logger':\n\n1. Write a function that appends a timestamped message to a log file, using 'a' mode.\n2. Wrap the file operations in try/except to handle a missing folder gracefully.\n3. Add a finally block that always prints 'Log attempt finished'.\n4. Define a custom exception EmptyMessageError, raised if the message is blank.\n\nThis combines file modes, appending, try/except/finally, and custom exceptions.",
            "key_points": [
                "Combines file writing, exceptions, and finally cleanup.",
                "Custom exceptions make validation errors clearer.",
                "finally guarantees cleanup code always runs.",
                "Try the Notes App Mini App above for real file I/O in action.",
                "This is the same pattern this whole platform uses to save your progress!"
            ],
            "code_example": "class EmptyMessageError(Exception):\n    pass\n\ndef log_message(message):\n    try:\n        if not message.strip():\n            raise EmptyMessageError(\"Message cannot be empty!\")\n        with open(\"activity.log\", \"a\") as f:\n            f.write(message + \"\\n\")\n        print(\"Logged successfully.\")\n    except EmptyMessageError as e:\n        print(e)\n    except OSError as e:\n        print(f\"File error: {e}\")\n    finally:\n        print(\"Log attempt finished.\")\n\nlog_message(\"User completed Module 4\")",
        },
    ],
    "quiz": [
        {"question": "Which mode overwrites an existing file completely?", "options": ["'a'", "'r'", "'w'", "'x'"], "answer_index": 2},
        {"question": "Which mode adds content without erasing existing data?", "options": ["'w'", "'a'", "'r'", "'x'"], "answer_index": 1},
        {"question": "What's the main benefit of 'with open(...) as f:'?", "options": ["Faster reading", "Auto-closes the file, even on error", "Allows binary mode only", "Required for CSV files"], "answer_index": 1},
        {"question": "What does f.readlines() return?", "options": ["A single string", "A list of lines", "A dictionary", "A file object"], "answer_index": 1},
        {"question": "Which built-in module handles CSV parsing correctly?", "options": ["json", "os", "csv", "sys"], "answer_index": 2},
        {"question": "What happens to code after an error inside a try block?", "options": ["It keeps running normally", "It's skipped; control jumps to except", "The program always crashes", "It restarts the try block"], "answer_index": 1},
        {"question": "When does a finally block run?", "options": ["Only if no error occurs", "Only if an error occurs", "Always, error or not", "Never automatically"], "answer_index": 2},
        {"question": "How do you define a custom exception?", "options": ["def MyError():", "class MyError(Exception): pass", "raise MyError", "except MyError:"], "answer_index": 1},
        {"question": "Which logging level is most severe?", "options": ["DEBUG", "INFO", "WARNING", "CRITICAL"], "answer_index": 3},
        {"question": "What keyword triggers a custom exception?", "options": ["throw", "raise", "except", "error"], "answer_index": 1},
    ],
    "mini_app": {
        "title": "Notes App (File Storage)",
        "description": "A real notes app that reads, writes, and appends to an actual text file on disk.",
        "launch": launch_mini_app,
    },
}
