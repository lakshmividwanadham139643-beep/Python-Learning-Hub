import random
import tkinter as tk

import config as cfg
from utils.helpers import center_window, make_button


# ==========================================
# MINI APPLICATION — Number Guessing Game
# ==========================================

def launch_mini_app(parent):
    """A number guessing game — demonstrates while loops, if-elif-else,
    functions, and break, all from Module 2."""

    win = tk.Toplevel(parent)
    win.title("Mini App — Number Guessing Game")
    win.configure(bg=cfg.WHITE)
    center_window(win, 380, 420)
    win.resizable(False, False)

    secret = random.randint(1, 100)
    attempts = {"count": 0}

    tk.Label(
        win, text="🔁 Guess the Number", bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_H3
    ).pack(pady=(20, 4))

    tk.Label(
        win, text="I'm thinking of a number between 1 and 100.",
        bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_BODY
    ).pack(pady=(0, 20))

    guess_var = tk.StringVar()
    entry = tk.Entry(win, textvariable=guess_var, font=cfg.FONT_BODY, justify="center")
    entry.pack(padx=40, fill="x", ipady=8)
    entry.focus_set()

    feedback = tk.Label(
        win, text="", bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_BODY_BOLD, wraplength=300
    )
    feedback.pack(pady=20)

    def check_guess():
        text = guess_var.get().strip()

        if not text.isdigit():
            feedback.configure(text="Please enter a whole number.", fg=cfg.RED)
            return

        guess = int(text)
        attempts["count"] += 1

        if guess < secret:
            feedback.configure(text=f"📈 Too low! Attempt #{attempts['count']}", fg=cfg.ORANGE)
        elif guess > secret:
            feedback.configure(text=f"📉 Too high! Attempt #{attempts['count']}", fg=cfg.ORANGE)
        else:
            feedback.configure(
                text=f"🎉 Correct! The number was {secret}.\nSolved in {attempts['count']} attempts.",
                fg=cfg.GREEN
            )
            guess_btn.configure(state="disabled")

        guess_var.set("")

    guess_btn = make_button(win, "Submit Guess", check_guess, cfg.BLUE)
    guess_btn.pack(pady=(0, 10), ipadx=10, ipady=4)

    entry.bind("<Return>", lambda e: check_guess())

    def restart():
        nonlocal secret
        secret = random.randint(1, 100)
        attempts["count"] = 0
        feedback.configure(text="New number chosen — guess again!", fg=cfg.TEXT)
        guess_btn.configure(state="normal")

    make_button(win, "🔄 New Game", restart, cfg.NAVY2).pack(ipadx=10, ipady=2)


# ==========================================
# MODULE CONTENT
# ==========================================

MODULE = {
    "id": 2,
    "title": "Control Flow & Functions",
    "description": "Make decisions, repeat actions, and organize logic into clean, reusable functions.",
    "topics": [
        {
            "id": 1,
            "title": "Boolean Values",
            "theory": "A boolean is a data type with exactly two values: `True` or `False`. Booleans are the backbone of decision-making in code — every `if` statement and loop condition ultimately evaluates to a boolean.\n\nComparison operators (`==`, `>`, `<`, etc.) produce booleans, and Python treats many other values as 'truthy' or 'falsy' when used in a condition — 0, empty strings, empty lists, and None are all falsy.",
            "key_points": [
                "Only two boolean values: True and False (capitalized).",
                "Comparisons like a == b evaluate to a boolean.",
                "0, '', [], {}, and None are 'falsy'; most else is 'truthy'.",
                "bool(x) converts any value to True/False.",
                "Booleans are the foundation of every if/loop condition."
            ],
            "code_example": "is_raining = True\ntemperature = 15\n\nprint(is_raining, type(is_raining))\nprint(temperature > 20)\nprint(bool(\"\"), bool(\"text\"), bool(0), bool(42))",
        },
        {
            "id": 2,
            "title": "if Statement",
            "theory": "An `if` statement runs a block of code only when its condition is `True`. The condition is followed by a colon, and the code to run is indented beneath it.\n\nIf the condition is `False`, the indented block is simply skipped and the program continues after it.",
            "key_points": [
                "Syntax: if condition:  (then an indented block).",
                "The block only runs when the condition is True.",
                "If False, the block is skipped entirely.",
                "Conditions are usually comparisons or boolean variables.",
                "No parentheses required around the condition (unlike C/Java)."
            ],
            "code_example": "age = 20\n\nif age >= 18:\n    print(\"You are an adult.\")",
        },
        {
            "id": 3,
            "title": "if-else",
            "theory": "`if-else` lets you run one block when a condition is True, and a different block when it's False — covering both outcomes with one structure. Exactly one of the two blocks will ever run.",
            "key_points": [
                "else has no condition — it's the 'otherwise' case.",
                "Exactly one branch executes per run.",
                "else must align with its matching if.",
                "Great for binary (yes/no, pass/fail) decisions.",
                "Both blocks must be indented consistently."
            ],
            "code_example": "age = 15\n\nif age >= 18:\n    print(\"You can vote.\")\nelse:\n    print(\"Not old enough to vote yet.\")",
        },
        {
            "id": 4,
            "title": "if-elif-else",
            "theory": "When you have more than two possible outcomes, `elif` (short for 'else if') lets you check additional conditions in sequence. Python checks each condition top to bottom and runs the first one that's True, then skips the rest — even if a later condition would also be True.",
            "key_points": [
                "elif checks another condition if the previous ones were False.",
                "Only the first matching branch runs — the rest are skipped.",
                "The final else is optional, and catches everything else.",
                "Order matters — put more specific conditions first.",
                "You can chain as many elif blocks as needed."
            ],
            "code_example": "score = 82\n\nif score >= 90:\n    grade = \"A\"\nelif score >= 75:\n    grade = \"B\"\nelif score >= 60:\n    grade = \"C\"\nelse:\n    grade = \"F\"\n\nprint(f\"Grade: {grade}\")",
        },
        {
            "id": 5,
            "title": "Nested Conditions",
            "theory": "An `if` statement can contain another `if` inside it — this is called nesting, and it's useful when a decision depends on more than one factor. Each level of nesting needs its own indentation, so deeply nested code can get hard to read; often it's cleaner to combine conditions with `and`/`or` instead.",
            "key_points": [
                "An if/else block can contain another if/else inside it.",
                "Each nested level needs one more indentation step.",
                "Useful when a decision depends on multiple factors.",
                "Too much nesting hurts readability — consider 'and'/'or'.",
                "Nested conditions are still evaluated top-to-bottom, inside out."
            ],
            "code_example": "age = 25\nhas_license = True\n\nif age >= 18:\n    if has_license:\n        print(\"You can drive.\")\n    else:\n        print(\"Get a license first.\")\nelse:\n    print(\"Too young to drive.\")",
        },
        {
            "id": 6,
            "title": "for Loop",
            "theory": "A `for` loop repeats a block of code once for each item in a sequence — a list, string, or a range of numbers via `range()`. `range(5)` produces 0, 1, 2, 3, 4; `range(1, 6)` produces 1 through 5; `range(0, 10, 2)` steps by 2.",
            "key_points": [
                "for item in sequence: runs once per item.",
                "range(n) generates numbers 0 to n-1.",
                "range(start, stop, step) controls the sequence precisely.",
                "Works directly over lists, strings, and other sequences.",
                "The loop variable holds the current item each iteration."
            ],
            "code_example": "for i in range(5):\n    print(i)\n\nfor letter in \"Hub\":\n    print(letter)\n\nfor num in range(0, 10, 2):\n    print(num)",
        },
        {
            "id": 7,
            "title": "while Loop",
            "theory": "A `while` loop repeats a block as long as its condition stays True. Unlike `for`, it doesn't automatically know when to stop — you must update something inside the loop that eventually makes the condition False, or you get an infinite loop.",
            "key_points": [
                "while condition: repeats as long as condition is True.",
                "You must update a variable inside to eventually stop it.",
                "Forgetting to update the condition causes an infinite loop.",
                "Great when you don't know the exact number of iterations upfront.",
                "Ctrl+C stops a runaway loop in the terminal."
            ],
            "code_example": "count = 0\n\nwhile count < 5:\n    print(f\"Count is {count}\")\n    count += 1  # without this, the loop never ends",
        },
        {
            "id": 8,
            "title": "break",
            "theory": "`break` immediately exits the closest enclosing loop, skipping any remaining iterations. It's commonly used to stop searching once a match is found, or to end a loop based on a condition checked mid-iteration.",
            "key_points": [
                "break exits the loop immediately, no more iterations.",
                "Works in both for and while loops.",
                "Common use: stop as soon as you find what you need.",
                "Only breaks the innermost loop if loops are nested.",
                "Code after the loop still runs normally."
            ],
            "code_example": "numbers = [4, 8, 15, 16, 23, 42]\n\nfor n in numbers:\n    if n == 16:\n        print(\"Found 16!\")\n        break\n    print(f\"Checked {n}\")",
        },
        {
            "id": 9,
            "title": "continue",
            "theory": "`continue` skips the rest of the current iteration and jumps straight to the next one — the loop keeps running, it just skips over that one pass. It's useful for filtering out certain items without stopping the whole loop.",
            "key_points": [
                "continue skips to the next iteration immediately.",
                "The loop keeps running — only that one pass is skipped.",
                "Useful for filtering values inside a loop.",
                "Different from break, which stops the loop entirely.",
                "Works in both for and while loops."
            ],
            "code_example": "for n in range(1, 11):\n    if n % 2 != 0:\n        continue  # skip odd numbers\n    print(n)  # only even numbers print",
        },
        {
            "id": 10,
            "title": "Functions",
            "theory": "A function is a named, reusable block of code defined with `def`. Functions let you avoid repeating yourself — write the logic once, then call it by name whenever you need it.\n\nA function is only executed when it's *called*; defining it alone does nothing. Good functions do one clear thing and are named after what they do.",
            "key_points": [
                "Defined with def name(): followed by an indented body.",
                "Functions run only when called, not when defined.",
                "Reduces repeated code — write once, call many times.",
                "Should ideally do one clear, well-named thing.",
                "Can be called from anywhere after they're defined."
            ],
            "code_example": "def greet():\n    print(\"Hello from a function!\")\n\ngreet()\ngreet()  # can be called as many times as needed",
        },
        {
            "id": 11,
            "title": "Parameters",
            "theory": "Parameters let a function accept input values, making it flexible instead of hardcoded. You list parameter names in the function definition, then pass matching arguments when you call it.\n\nPython also supports default parameter values (used when no argument is given) and keyword arguments (naming which parameter each value goes to).",
            "key_points": [
                "Parameters are placeholders defined in def func(param):.",
                "Arguments are the actual values passed when calling.",
                "Default values: def func(x=10): used if no argument given.",
                "Keyword arguments: func(name=\"Ana\") — order-independent.",
                "A function can take any number of parameters."
            ],
            "code_example": "def greet(name, greeting=\"Hello\"):\n    print(f\"{greeting}, {name}!\")\n\ngreet(\"Aarav\")\ngreet(\"Priya\", greeting=\"Namaste\")",
        },
        {
            "id": 12,
            "title": "Return Values",
            "theory": "`return` sends a value back from a function to wherever it was called, so the result can be stored or used further. A function without a `return` statement implicitly returns `None`.\n\n`return` also immediately ends the function — any code after it in the same block won't run.",
            "key_points": [
                "return sends a value back to the caller.",
                "A function with no return statement returns None.",
                "return immediately ends the function's execution.",
                "You can return multiple values as a tuple: return a, b",
                "print() displays a value; return hands it back to use later."
            ],
            "code_example": "def add(a, b):\n    return a + b\n\nresult = add(4, 5)\nprint(result)  # 9, stored for later use\n\ndef min_max(numbers):\n    return min(numbers), max(numbers)\n\nlow, high = min_max([3, 7, 1, 9])\nprint(low, high)",
        },
        {
            "id": 13,
            "title": "Lambda",
            "theory": "A lambda is a small, anonymous (unnamed) function written in a single line: `lambda arguments: expression`. It's handy for short throwaway functions, especially when passed as an argument to another function like `sorted()` or `map()`.\n\nLambdas can only contain a single expression — no statements, loops, or multiple lines — so anything more complex should be a regular `def` function.",
            "key_points": [
                "Syntax: lambda args: expression",
                "Anonymous — doesn't need a def or a name to exist.",
                "Limited to one expression, automatically returned.",
                "Common with sorted(), filter(), map() as the 'key' function.",
                "Use a regular def for anything beyond one simple expression."
            ],
            "code_example": "square = lambda x: x ** 2\nprint(square(5))\n\npeople = [(\"Ana\", 25), (\"Raj\", 19)]\npeople.sort(key=lambda person: person[1])\nprint(people)",
        },
        {
            "id": 14,
            "title": "Recursion",
            "theory": "Recursion is when a function calls itself to solve a smaller version of the same problem, until it reaches a 'base case' that stops it. Every recursive function needs: (1) a base case that stops the recursion, and (2) a recursive case that moves toward that base case.\n\nWithout a proper base case, recursion runs forever and eventually crashes with a RecursionError.",
            "key_points": [
                "A recursive function calls itself with a smaller input.",
                "Must have a base case to stop the recursion.",
                "Must have a recursive case that approaches the base case.",
                "Missing a base case causes infinite recursion → crash.",
                "Anything recursive can also be written with a loop."
            ],
            "code_example": "def factorial(n):\n    if n <= 1:          # base case\n        return 1\n    return n * factorial(n - 1)  # recursive case\n\nprint(factorial(5))  # 120",
        },
        {
            "id": 15,
            "title": "Practice Project",
            "theory": "Build a 'Grade Calculator' that uses everything from this module:\n\n1. Write a function `calculate_grade(score)` that uses if-elif-else to return a letter grade.\n2. Use a while loop to keep asking for scores until the user types 'done'.\n3. Use a for loop to print every grade collected at the end.\n4. Add a lambda to sort the scores before printing them.\n\nThis combines conditions, loops, functions, parameters, return values, and lambdas.",
            "key_points": [
                "Combines conditions, loops, functions, and lambdas.",
                "while loop for repeated input until a sentinel value.",
                "for loop to display collected results.",
                "Function with parameters and a return value at its core.",
                "Try the Mini App above for another example of these ideas."
            ],
            "code_example": "def calculate_grade(score):\n    if score >= 90:\n        return \"A\"\n    elif score >= 75:\n        return \"B\"\n    elif score >= 60:\n        return \"C\"\n    return \"F\"\n\nscores = []\nwhile True:\n    entry = input(\"Enter a score (or 'done'): \")\n    if entry == \"done\":\n        break\n    scores.append(int(entry))\n\nfor s in sorted(scores):\n    print(s, \"->\", calculate_grade(s))",
        },
    ],
    "quiz": [
        {"question": "What are the two boolean values in Python?", "options": ["true / false", "True / False", "1 / 0 only", "Yes / No"], "answer_index": 1},
        {"question": "What runs if an if condition is False and there's an else block?", "options": ["Nothing runs", "The if block", "The else block", "Both run"], "answer_index": 2},
        {"question": "In an if-elif-else chain, how many branches execute?", "options": ["All matching ones", "Only the first matching one", "Always the else", "None"], "answer_index": 1},
        {"question": "What does range(1, 6) produce?", "options": ["1,2,3,4,5,6", "0,1,2,3,4,5", "1,2,3,4,5", "1,2,3,4,5,6,7"], "answer_index": 2},
        {"question": "What's required to avoid an infinite while loop?", "options": ["A break statement only", "Updating the loop condition inside it", "Using range()", "Nothing, while loops always stop"], "answer_index": 1},
        {"question": "What does 'break' do?", "options": ["Skips to next iteration", "Exits the loop immediately", "Pauses the program", "Restarts the loop"], "answer_index": 1},
        {"question": "What does 'continue' do?", "options": ["Exits the loop", "Skips the rest of the current iteration only", "Ends the program", "Repeats the last iteration"], "answer_index": 1},
        {"question": "What does a function with no return statement return?", "options": ["0", "An error", "None", "An empty string"], "answer_index": 2},
        {"question": "What is a lambda?", "options": ["A loop type", "A small anonymous function", "A data type", "A module"], "answer_index": 1},
        {"question": "What must every recursive function have to avoid crashing?", "options": ["A loop", "A base case", "A return of None", "A lambda"], "answer_index": 1},
    ],
    "mini_app": {
        "title": "Number Guessing Game",
        "description": "A classic guessing game showing while loops, if-elif-else, and functions working together.",
        "launch": launch_mini_app,
    },
}
