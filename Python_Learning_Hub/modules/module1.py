import tkinter as tk

import config as cfg
from utils.helpers import center_window, make_button


# ==========================================
# MINI APPLICATION — Simple Calculator
# ==========================================

def launch_mini_app(parent):
    """Opens a small working calculator — demonstrates variables, operators,
    input handling, and type conversion, all from Module 1."""

    win = tk.Toplevel(parent)
    win.title("Mini App — Simple Calculator")
    win.configure(bg=cfg.WHITE)
    center_window(win, 360, 460)
    win.resizable(False, False)

    tk.Label(
        win, text="🧮 Simple Calculator", bg=cfg.WHITE, fg=cfg.TEXT,
        font=cfg.FONT_H3
    ).pack(pady=(20, 10))

    display_var = tk.StringVar(value="0")

    display = tk.Entry(
        win, textvariable=display_var, font=("Consolas", 22), justify="right",
        bd=0, bg=cfg.NAVY, fg=cfg.WHITE, insertbackground=cfg.WHITE
    )
    display.pack(fill="x", padx=20, pady=10, ipady=14)

    state = {"first": None, "op": None, "fresh": True}

    def press_digit(d):
        if state["fresh"] or display_var.get() == "0":
            display_var.set(d)
            state["fresh"] = False
        else:
            display_var.set(display_var.get() + d)

    def press_dot():
        if "." not in display_var.get():
            display_var.set(display_var.get() + ".")
            state["fresh"] = False

    def press_op(op):
        state["first"] = float(display_var.get())
        state["op"] = op
        state["fresh"] = True

    def press_equals():
        if state["op"] is None:
            return
        second = float(display_var.get())
        first = state["first"]
        try:
            if state["op"] == "+":
                result = first + second
            elif state["op"] == "-":
                result = first - second
            elif state["op"] == "*":
                result = first * second
            elif state["op"] == "/":
                result = first / second
            elif state["op"] == "%":
                result = first % second
            else:
                result = second

            # Type conversion in action: show ints cleanly, floats trimmed
            display_var.set(str(int(result)) if result == int(result) else str(round(result, 6)))
        except ZeroDivisionError:
            display_var.set("Error: ÷0")

        state["op"] = None
        state["fresh"] = True

    def press_clear():
        display_var.set("0")
        state["first"] = None
        state["op"] = None
        state["fresh"] = True

    buttons_grid = tk.Frame(win, bg=cfg.WHITE)
    buttons_grid.pack(padx=20, pady=10, fill="both", expand=True)

    layout = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["C", "0", ".", "+"],
    ]

    for r, row in enumerate(layout):
        buttons_grid.rowconfigure(r, weight=1)
        for c, label in enumerate(row):
            buttons_grid.columnconfigure(c, weight=1)

            if label.isdigit():
                cmd = lambda d=label: press_digit(d)
                bg = cfg.BLUE_LIGHT
                fg = cfg.TEXT
            elif label == ".":
                cmd = press_dot
                bg = cfg.BLUE_LIGHT
                fg = cfg.TEXT
            elif label == "C":
                cmd = press_clear
                bg = cfg.RED_LIGHT
                fg = cfg.RED
            else:
                cmd = lambda op=label: press_op(op)
                bg = cfg.NAVY2
                fg = cfg.WHITE

            btn = tk.Button(
                buttons_grid, text=label, command=cmd, bg=bg, fg=fg,
                font=("Segoe UI", 14, "bold"), bd=0, cursor="hand2"
            )
            btn.grid(row=r, column=c, sticky="nsew", padx=4, pady=4, ipady=10)

    make_button(win, "=  Calculate", press_equals, cfg.GREEN).pack(
        fill="x", padx=20, pady=(0, 20), ipady=4
    )


# ==========================================
# MODULE CONTENT
# ==========================================

MODULE = {
    "id": 1,
    "title": "Python Fundamentals",
    "description": "Get comfortable with Python's basics — syntax, variables, data types, and your first working programs.",
    "topics": [
        {
            "id": 1,
            "title": "Python Introduction",
            "theory": "Python is a high-level, interpreted programming language created by Guido van Rossum and first released in 1991. It's known for readable syntax that reads almost like plain English, which is why it's a popular first language for beginners, while still being powerful enough for web development, data science, automation, and AI.\n\nUnlike compiled languages such as C or Java, Python code is run line-by-line by an interpreter, which makes it great for quick experimentation. Python is also dynamically typed — you don't declare a variable's type before using it; the interpreter figures it out at runtime.",
            "key_points": [
                "Created by Guido van Rossum, first released in 1991.",
                "Interpreted, not compiled — code runs line by line.",
                "Dynamically typed — no need to declare variable types.",
                "Used in web dev, data science, automation, and AI/ML.",
                "Known for clean, readable syntax using indentation."
            ],
            "code_example": "# Your first Python program\nprint(\"Hello, World!\")\nprint(\"Welcome to Python Learning Hub\")",
        },
        {
            "id": 2,
            "title": "Installation and IDE",
            "theory": "To write Python code you need two things: the interpreter (which runs your code) and an editor (where you write it). Download Python from python.org — on Windows, check 'Add Python to PATH' during install, then verify with `python --version` in a terminal.\n\nPopular editors range from lightweight ones like VS Code, to full IDEs like PyCharm, to browser-based notebooks like Jupyter or Google Colab — great for learning without installing anything.",
            "key_points": [
                "Download the interpreter from python.org.",
                "Check 'Add Python to PATH' during Windows installation.",
                "Verify with: python --version",
                "VS Code and PyCharm are the most popular editors.",
                "Jupyter/Colab work well for learning, no install needed."
            ],
            "code_example": "# Run in your terminal to confirm install\npython --version\n\n# Or open the interactive shell\npython",
        },
        {
            "id": 3,
            "title": "Python Syntax",
            "theory": "Python's biggest syntactic difference from most languages is that it uses indentation to define code blocks, instead of curly braces. This isn't a style choice — the interpreter enforces it strictly.\n\nStatements don't need a semicolon, and Python is case-sensitive: `Name` and `name` are different variables. A colon `:` always introduces an indented block, such as after `if`, `for`, or `def`.",
            "key_points": [
                "Indentation defines code blocks — usually 4 spaces.",
                "No curly braces {} or semicolons required.",
                "Python is case-sensitive (myVar ≠ myvar).",
                "A colon ':' starts an indented block.",
                "Consistent indentation is mandatory, not optional."
            ],
            "code_example": "if 5 > 2:\n    print(\"Five is greater than two!\")\n\nfor i in range(3):\n    print(i)",
        },
        {
            "id": 4,
            "title": "Variables",
            "theory": "A variable is a name that refers to a value in memory. You assign one with `=` — no type declaration needed; Python infers the type from the value.\n\nNames must start with a letter or underscore, then letters/digits/underscores, and can't be a reserved keyword like `if`. PEP 8 (Python's style guide) recommends `snake_case` for variable names.",
            "key_points": [
                "Assign with '=' — no type declaration needed.",
                "Names start with a letter/underscore, then letters/digits/underscores.",
                "Case-sensitive; cannot be a Python keyword.",
                "Convention: snake_case, e.g. student_name.",
                "Multiple assignment: a, b = 1, 2"
            ],
            "code_example": "student_name = \"Aarav\"\nage = 20\nheight = 5.9\nis_enrolled = True\n\nx, y, z = 1, 2, 3\nprint(student_name, age, height, is_enrolled)",
        },
        {
            "id": 5,
            "title": "Data Types",
            "theory": "Python's core built-in types are `int` (whole numbers), `float` (decimals), `str` (text), and `bool` (True/False). Beyond these are collection types — `list`, `tuple`, `set`, and `dict` — covered in Module 3.\n\nUse `type()` to check any value's type. Because Python is dynamically typed, a variable can be reassigned to a value of a different type at any time.",
            "key_points": [
                "Core types: int, float, str, bool.",
                "Collections: list, tuple, set, dict (Module 3).",
                "type(value) checks a variable's data type.",
                "Variables can be reassigned to a different type.",
                "None represents 'no value' — Python's null."
            ],
            "code_example": "age = 20\nprice = 99.5\nname = \"Learning Hub\"\nis_active = True\nnothing = None\n\nprint(type(age), type(price), type(name), type(is_active))",
        },
        {
            "id": 6,
            "title": "Type Conversion",
            "theory": "Type conversion (casting) changes a value from one type to another using built-ins: `int()`, `float()`, `str()`, `bool()`.\n\nThis matters most with user input — `input()` always returns a string, even for numbers, so you must convert it with `int()` or `float()` before doing math on it. Converting an invalid string, like `int('abc')`, raises a ValueError.",
            "key_points": [
                "int(), float(), str(), bool() convert between types.",
                "input() always returns a string, even for numbers.",
                "int('abc') raises a ValueError — invalid conversion.",
                "bool() treats 0, '', None, [] as False; else True.",
                "Chain conversions if you need to go type A → B → C."
            ],
            "code_example": "age_text = \"25\"\nage_number = int(age_text)\nprint(age_number + 5)\n\nprice = str(99.99)\nprint(\"Price: $\" + price)\n\nprint(bool(0), bool(1), bool(\"\"), bool(\"hi\"))",
        },
        {
            "id": 7,
            "title": "Operators",
            "theory": "Operators perform actions on values: arithmetic (`+ - * / // % **`), comparison (`== != > < >= <=`), logical (`and or not`), assignment (`= += -= *=`), and membership (`in`, `not in`).\n\nA few Python-specific ones: `//` is floor (integer) division, `%` gives the remainder, and `**` raises to a power.",
            "key_points": [
                "Arithmetic: + - * / // % **",
                "// = floor division, % = remainder, ** = power.",
                "Comparisons return a boolean.",
                "Logical operators combine boolean expressions: and, or, not.",
                "'in' / 'not in' check membership in a sequence."
            ],
            "code_example": "a, b = 10, 3\nprint(a + b, a - b, a * b, a / b)\nprint(a // b, a % b, a ** b)\nprint(a > b and b > 0)\nprint(3 in [1, 2, 3])",
        },
        {
            "id": 8,
            "title": "Input and Output",
            "theory": "`print()` displays output; it accepts multiple values, plus optional `sep` and `end` to customize spacing and line endings.\n\n`input()` pauses the program, waits for the user to type something and press Enter, and always returns a string. F-strings (`f\"Hello, {name}!\"`) are the modern, readable way to embed variables inside printed text.",
            "key_points": [
                "print() sends output to the console.",
                "input(prompt) reads user text, always returns a str.",
                "f-strings embed variables directly in text.",
                "print(sep=..., end=...) customizes spacing/line endings.",
                "Always convert input() before doing math with it."
            ],
            "code_example": "name = input(\"What's your name? \")\nage = int(input(\"What's your age? \"))\n\nprint(f\"Hi {name}, next year you'll be {age + 1}!\")\nprint(\"A\", \"B\", \"C\", sep=\"-\", end=\"!\\n\")",
        },
        {
            "id": 9,
            "title": "Comments",
            "theory": "Comments are notes Python ignores when running — they explain code to humans. A single-line comment starts with `#`. Triple-quoted strings (`'''...'''` or `\"\"\"...\"\"\"`) handle multi-line notes and, placed right after a `def`, become a docstring describing the function.\n\nGood comments explain *why*, not *what* — the code already shows the 'what'.",
            "key_points": [
                "Single-line comments start with #.",
                "Triple quotes create multi-line comments/docstrings.",
                "Comment the 'why', not the obvious 'what'.",
                "A docstring right after def describes the function.",
                "Over-commenting obvious code clutters more than it helps."
            ],
            "code_example": "# Calculates the area of a rectangle\ndef area(width, height):\n    \"\"\"Returns width * height.\"\"\"\n    return width * height\n\nprint(area(4, 5))",
        },
        {
            "id": 10,
            "title": "Practice Project",
            "theory": "Combine everything from this module into a 'Personal Info Card' program:\n\n1. Ask for name, age, and favorite hobby using input().\n2. Convert age to an integer.\n3. Print a formatted card with f-strings showing name, age, age next year, and hobby.\n4. Comment each step.\n\nThis touches variables, data types, type conversion, operators, input/output, and comments — everything from Module 1.",
            "key_points": [
                "Combines variables, types, conversion, operators, I/O, comments.",
                "Goal: a working, readable, well-commented program.",
                "Try adding validation for non-numeric age input.",
                "Extend it: add a 'favorite color' printed in a styled box.",
                "Try the Mini App above for a second example of these ideas in action."
            ],
            "code_example": "name = input(\"Enter your name: \")\nage = int(input(\"Enter your age: \"))\nhobby = input(\"Enter your favorite hobby: \")\n\nprint(\"=\" * 30)\nprint(f\"Name   : {name}\")\nprint(f\"Age    : {age} (next year: {age + 1})\")\nprint(f\"Hobby  : {hobby}\")\nprint(\"=\" * 30)",
        },
    ],
    "quiz": [
        {"question": "Who created Python?", "options": ["Guido van Rossum", "James Gosling", "Dennis Ritchie", "Bjarne Stroustrup"], "answer_index": 0},
        {"question": "What defines a code block in Python?", "options": ["Curly braces {}", "Indentation", "Semicolons", "Parentheses"], "answer_index": 1},
        {"question": "Which of these is NOT a core Python data type?", "options": ["int", "float", "char", "bool"], "answer_index": 2},
        {"question": "What does input() always return?", "options": ["int", "float", "str", "bool"], "answer_index": 2},
        {"question": "Which operator gives the remainder of a division?", "options": ["//", "%", "**", "/"], "answer_index": 1},
        {"question": "How do you start a single-line comment?", "options": ["//", "#", "--", "/*"], "answer_index": 1},
        {"question": "Which function converts a string to an integer?", "options": ["str()", "float()", "int()", "bool()"], "answer_index": 2},
        {"question": "What is the recommended variable naming style (PEP 8)?", "options": ["camelCase", "PascalCase", "snake_case", "kebab-case"], "answer_index": 2},
        {"question": "What does ** do in Python?", "options": ["Multiplication", "Floor division", "Exponentiation", "Modulus"], "answer_index": 2},
        {"question": "Is Python compiled or interpreted?", "options": ["Compiled", "Interpreted", "Both equally", "Neither"], "answer_index": 1},
    ],
    "mini_app": {
        "title": "Simple Calculator",
        "description": "A working four-function calculator built with the operators and I/O you just learned.",
        "launch": launch_mini_app,
    },
}
