import tkinter as tk
from tkinter import messagebox

import config as cfg
from utils.helpers import center_window, make_button


# ==========================================
# MINI APPLICATION — Contact Book
# ==========================================

def launch_mini_app(parent):
    """An in-memory contact book — demonstrates lists, dicts, and string
    methods, all from Module 3."""

    win = tk.Toplevel(parent)
    win.title("Mini App — Contact Book")
    win.configure(bg=cfg.WHITE)
    center_window(win, 460, 520)
    win.resizable(False, False)

    contacts = []  # list of dicts: {"name": ..., "phone": ...}

    tk.Label(
        win, text="🗂️ Contact Book", bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_H3
    ).pack(pady=(20, 10))

    form = tk.Frame(win, bg=cfg.WHITE)
    form.pack(fill="x", padx=20)

    name_var = tk.StringVar()
    phone_var = tk.StringVar()

    tk.Label(form, text="Name", bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_SMALL).grid(row=0, column=0, sticky="w")
    tk.Entry(form, textvariable=name_var, font=cfg.FONT_BODY).grid(row=1, column=0, sticky="ew", padx=(0, 8))

    tk.Label(form, text="Phone", bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_SMALL).grid(row=0, column=1, sticky="w")
    tk.Entry(form, textvariable=phone_var, font=cfg.FONT_BODY).grid(row=1, column=1, sticky="ew")

    form.columnconfigure(0, weight=1)
    form.columnconfigure(1, weight=1)

    listbox = tk.Listbox(win, font=cfg.FONT_BODY, bd=0, highlightthickness=1, highlightbackground=cfg.BORDER)
    listbox.pack(fill="both", expand=True, padx=20, pady=15)

    def refresh_list():
        listbox.delete(0, tk.END)
        # sorted() + a lambda key — string methods (.title()) applied per entry
        for c in sorted(contacts, key=lambda c: c["name"].lower()):
            listbox.insert(tk.END, f"{c['name'].title():<20} {c['phone']}")

    def add_contact():
        name = name_var.get().strip()
        phone = phone_var.get().strip()

        if not name or not phone:
            messagebox.showwarning("Missing info", "Please enter both a name and a phone number.", parent=win)
            return

        contacts.append({"name": name, "phone": phone})
        name_var.set("")
        phone_var.set("")
        refresh_list()

    def delete_selected():
        selection = listbox.curselection()
        if not selection:
            return
        # Map the visually sorted position back to the underlying list
        sorted_contacts = sorted(contacts, key=lambda c: c["name"].lower())
        target = sorted_contacts[selection[0]]
        contacts.remove(target)
        refresh_list()

    btn_row = tk.Frame(win, bg=cfg.WHITE)
    btn_row.pack(fill="x", padx=20, pady=(0, 20))

    make_button(btn_row, "➕ Add Contact", add_contact, cfg.GREEN).pack(side="left", expand=True, fill="x", padx=(0, 5))
    make_button(btn_row, "🗑️ Delete Selected", delete_selected, cfg.RED).pack(side="left", expand=True, fill="x", padx=(5, 0))


# ==========================================
# MODULE CONTENT
# ==========================================

MODULE = {
    "id": 3,
    "title": "Data Structures",
    "description": "Store and organize collections of data using lists, tuples, sets, dictionaries, and strings.",
    "topics": [
        {
            "id": 1,
            "title": "Lists",
            "theory": "A list is an ordered, changeable (mutable) collection written with square brackets: `[1, 2, 3]`. Lists can hold mixed types, grow or shrink at runtime, and are one of the most-used data structures in Python.\n\nItems are accessed by their position (index), starting at 0.",
            "key_points": [
                "Ordered, mutable collection: my_list = [1, 2, 3]",
                "Can hold mixed types in the same list.",
                "Indexing starts at 0.",
                "Grows/shrinks with append(), remove(), etc.",
                "len(my_list) gives the number of items."
            ],
            "code_example": "fruits = [\"apple\", \"banana\", \"cherry\"]\nfruits.append(\"mango\")\nprint(fruits[0], fruits[-1])\nprint(len(fruits))",
        },
        {
            "id": 2,
            "title": "List Methods",
            "theory": "Lists come with many built-in methods: `append()` adds to the end, `insert()` adds at a position, `remove()` deletes the first matching value, `pop()` removes and returns an item by index, `sort()` orders it in place, and `reverse()` flips the order.",
            "key_points": [
                "append(x) adds to the end; insert(i, x) adds at position i.",
                "remove(x) deletes the first match; pop(i) removes by index.",
                "sort() orders in place; sorted(list) returns a new sorted copy.",
                "reverse() flips the list order in place.",
                "count(x) counts occurrences; index(x) finds the position."
            ],
            "code_example": "nums = [4, 1, 3, 2]\nnums.sort()\nprint(nums)\n\nnums.append(10)\nnums.remove(1)\nprint(nums)\nprint(nums.count(2), nums.index(3))",
        },
        {
            "id": 3,
            "title": "Tuples",
            "theory": "A tuple is like a list but immutable — once created, it can't be changed. Written with parentheses: `(1, 2, 3)`. Tuples are useful for fixed collections of values that shouldn't change, like coordinates, and they're slightly faster than lists.",
            "key_points": [
                "Ordered but immutable: point = (10, 20)",
                "Cannot append, remove, or modify items after creation.",
                "Useful for fixed data — coordinates, RGB colors, etc.",
                "Supports indexing and slicing just like lists.",
                "A single-item tuple needs a trailing comma: (5,)"
            ],
            "code_example": "point = (10, 20)\nprint(point[0], point[1])\n\n# point[0] = 99  # this would raise a TypeError\nx, y = point  # unpacking\nprint(x, y)",
        },
        {
            "id": 4,
            "title": "Sets",
            "theory": "A set is an unordered collection of unique values, written with curly braces: `{1, 2, 3}`. Duplicate values are automatically removed, which makes sets great for de-duplicating data or checking membership quickly.",
            "key_points": [
                "Unordered, unique values only: {1, 2, 2, 3} → {1, 2, 3}",
                "No indexing — sets have no fixed order.",
                "add(x) adds an item; remove(x) removes one.",
                "Very fast membership checks: x in my_set",
                "Great for removing duplicates from a list: set(my_list)"
            ],
            "code_example": "tags = {\"python\", \"beginner\", \"python\"}\nprint(tags)  # duplicate 'python' removed\n\ntags.add(\"tutorial\")\nprint(\"beginner\" in tags)",
        },
        {
            "id": 5,
            "title": "Set Operations",
            "theory": "Sets support mathematical set operations: union (`|`) combines two sets, intersection (`&`) keeps only shared items, difference (`-`) keeps items in one but not the other, and symmetric difference (`^`) keeps items in either but not both.",
            "key_points": [
                "union: a | b — all items from both sets.",
                "intersection: a & b — only items in both.",
                "difference: a - b — in a but not in b.",
                "symmetric_difference: a ^ b — in either, not both.",
                "Also available as methods: a.union(b), a.intersection(b)"
            ],
            "code_example": "a = {1, 2, 3, 4}\nb = {3, 4, 5, 6}\n\nprint(a | b)  # union\nprint(a & b)  # intersection\nprint(a - b)  # difference\nprint(a ^ b)  # symmetric difference",
        },
        {
            "id": 6,
            "title": "Dictionaries",
            "theory": "A dictionary stores key-value pairs, written with curly braces: `{\"name\": \"Ana\", \"age\": 20}`. Unlike lists, you access values by key instead of position, which makes dictionaries perfect for representing structured records.",
            "key_points": [
                "Key-value pairs: student = {\"name\": \"Ana\", \"age\": 20}",
                "Access a value with student[\"name\"] or .get(\"name\").",
                "Keys must be unique and immutable (usually strings).",
                "Add/update with student[\"key\"] = value.",
                "Dictionaries preserve insertion order (Python 3.7+)."
            ],
            "code_example": "student = {\"name\": \"Ana\", \"age\": 20}\nprint(student[\"name\"])\n\nstudent[\"age\"] = 21  # update\nstudent[\"grade\"] = \"A\"  # add new key\nprint(student)",
        },
        {
            "id": 7,
            "title": "Dictionary Methods",
            "theory": "Dictionaries offer useful methods: `.keys()` returns all keys, `.values()` returns all values, `.items()` returns key-value pairs (great for looping), `.get(key, default)` safely fetches a value without crashing if the key is missing, and `.pop(key)` removes a key and returns its value.",
            "key_points": [
                ".keys(), .values(), .items() give views for looping.",
                ".get(key, default) avoids a KeyError if key is missing.",
                ".pop(key) removes a key and returns its value.",
                "'key' in my_dict checks if a key exists.",
                "for k, v in my_dict.items(): loops over pairs."
            ],
            "code_example": "student = {\"name\": \"Ana\", \"age\": 20}\n\nfor key, value in student.items():\n    print(key, \"->\", value)\n\nprint(student.get(\"grade\", \"Not set\"))",
        },
        {
            "id": 8,
            "title": "Strings",
            "theory": "A string is an immutable sequence of characters, written in single, double, or triple quotes. Strings support concatenation (`+`), repetition (`*`), and are iterable — you can loop over each character with a `for` loop.",
            "key_points": [
                "Immutable — string methods return a new string.",
                "Concatenate with +, repeat with *.",
                "Iterable — for char in my_string: works directly.",
                "len(my_string) gives the character count.",
                "Triple quotes allow multi-line strings."
            ],
            "code_example": "greeting = \"Hello\" + \" \" + \"World\"\nprint(greeting * 2)\n\nfor char in \"Hub\":\n    print(char)\n\nprint(len(greeting))",
        },
        {
            "id": 9,
            "title": "Indexing",
            "theory": "Indexing accesses a single character (or list item) by its position, using square brackets. Python indexing starts at 0, and negative indices count backwards from the end — `-1` is the last item.",
            "key_points": [
                "Positive index: 0 is first, 1 is second, etc.",
                "Negative index: -1 is last, -2 is second-to-last.",
                "Works the same way on strings, lists, and tuples.",
                "Indexing out of range raises an IndexError.",
                "my_string[0] gets the first character."
            ],
            "code_example": "word = \"Python\"\nprint(word[0])   # 'P'\nprint(word[-1])  # 'n'\n\nnums = [10, 20, 30]\nprint(nums[1], nums[-2])",
        },
        {
            "id": 10,
            "title": "Slicing",
            "theory": "Slicing extracts a sub-section of a sequence using `[start:stop:step]`. `start` is inclusive, `stop` is exclusive, and `step` controls direction/spacing. Omitting a value uses a sensible default — omit `start` to begin from 0, omit `stop` to go to the end.",
            "key_points": [
                "Syntax: sequence[start:stop:step]",
                "start is included, stop is excluded.",
                "[::2] takes every 2nd item; [::-1] reverses the sequence.",
                "Omitting start/stop uses the beginning/end by default.",
                "Works identically on strings, lists, and tuples."
            ],
            "code_example": "word = \"Python Learning\"\nprint(word[0:6])    # 'Python'\nprint(word[7:])     # 'Learning'\nprint(word[::-1])   # reversed\n\nnums = [0, 1, 2, 3, 4, 5]\nprint(nums[::2])    # every 2nd item",
        },
        {
            "id": 11,
            "title": "String Methods",
            "theory": "Strings come with many built-in methods for common transformations: `.upper()`/`.lower()` change case, `.strip()` removes surrounding whitespace, `.split()` breaks a string into a list, `.join()` does the reverse, and `.replace()` swaps substrings.",
            "key_points": [
                ".upper(), .lower(), .title() change casing.",
                ".strip() removes leading/trailing whitespace.",
                ".split(sep) breaks a string into a list.",
                "\"-\".join(list) joins a list back into a string.",
                ".replace(old, new) swaps every occurrence."
            ],
            "code_example": "text = \"  Hello Python World  \"\nprint(text.strip().upper())\n\nwords = text.strip().split(\" \")\nprint(words)\nprint(\"_\".join(words))\nprint(text.replace(\"Python\", \"Learning\"))",
        },
        {
            "id": 12,
            "title": "Nested Data Structures",
            "theory": "Data structures can contain other data structures — a list of dictionaries, a dictionary of lists, and so on. This is how real-world structured data (like JSON from an API) is usually represented in Python, and it's essential for Modules 6 and 7.",
            "key_points": [
                "A list can contain dictionaries: [{...}, {...}]",
                "A dictionary can contain lists as values.",
                "Access nested data by chaining brackets: data[0][\"name\"]",
                "This shape mirrors JSON, used heavily in Module 7 (APIs).",
                "Loop through nested structures with nested for loops."
            ],
            "code_example": "students = [\n    {\"name\": \"Ana\", \"scores\": [88, 92]},\n    {\"name\": \"Raj\", \"scores\": [75, 80]},\n]\n\nfor student in students:\n    avg = sum(student[\"scores\"]) / len(student[\"scores\"])\n    print(f\"{student['name']}: {avg:.1f}\")",
        },
        {
            "id": 13,
            "title": "Practice Project",
            "theory": "Build a 'Student Records' mini-tool:\n\n1. Store several students as a list of dictionaries, each with name and a list of scores.\n2. Loop through and print each student's average score using nested data access.\n3. Use a set to collect all unique scores across every student.\n4. Use string methods to format each student's name in Title Case in the output.\n\nThis combines lists, dicts, sets, strings, and nested structures — the whole module.",
            "key_points": [
                "Combines lists, dicts, sets, strings, and nesting.",
                "Nested access: student['scores'][0]",
                "Sets are handy for 'all unique X across everything'.",
                "String formatting makes output presentation-ready.",
                "Try the Contact Book Mini App above for a similar structure."
            ],
            "code_example": "students = [\n    {\"name\": \"ana\", \"scores\": [88, 92, 79]},\n    {\"name\": \"raj\", \"scores\": [75, 80, 91]},\n]\n\nall_scores = set()\nfor s in students:\n    all_scores.update(s[\"scores\"])\n    avg = sum(s[\"scores\"]) / len(s[\"scores\"])\n    print(f\"{s['name'].title()}: avg {avg:.1f}\")\n\nprint(\"Unique scores:\", sorted(all_scores))",
        },
    ],
    "quiz": [
        {"question": "Which of these is mutable?", "options": ["Tuple", "String", "List", "int"], "answer_index": 2},
        {"question": "What does fruits.append('mango') do?", "options": ["Removes mango", "Adds mango to the end", "Sorts the list", "Finds mango's index"], "answer_index": 1},
        {"question": "Can you modify a tuple after creating it?", "options": ["Yes, always", "No, tuples are immutable", "Only if it has numbers", "Only with .append()"], "answer_index": 1},
        {"question": "What happens to duplicates in a set?", "options": ["Kept as-is", "Automatically removed", "Cause an error", "Converted to a list"], "answer_index": 1},
        {"question": "Which operator gives the union of two sets?", "options": ["&", "-", "|", "^"], "answer_index": 2},
        {"question": "How do you access a dictionary value safely without a KeyError?", "options": ["dict[key]", "dict.get(key, default)", "dict.pop(key)", "dict.keys()"], "answer_index": 1},
        {"question": "What does my_dict.items() return?", "options": ["Just the keys", "Just the values", "Key-value pairs", "The dictionary size"], "answer_index": 2},
        {"question": "What does word[-1] return for a string?", "options": ["First character", "Last character", "An error", "Empty string"], "answer_index": 1},
        {"question": "What does word[::-1] do?", "options": ["Duplicates the string", "Reverses the string", "Removes vowels", "Uppercases the string"], "answer_index": 1},
        {"question": "Which method splits a string into a list?", "options": [".join()", ".replace()", ".split()", ".strip()"], "answer_index": 2},
    ],
    "mini_app": {
        "title": "Contact Book",
        "description": "An in-memory contact manager showing lists of dictionaries, sorting, and string methods together.",
        "launch": launch_mini_app,
    },
}
