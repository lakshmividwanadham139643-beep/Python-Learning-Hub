import csv
import tkinter as tk

import config as cfg
from utils.helpers import center_window, make_button


# ==========================================
# MINI APPLICATION — Live Joke Fetcher (real REST API call)
# ==========================================

def launch_mini_app(parent):
    """Fetches a real joke from a public REST API — demonstrates GET
    requests, JSON parsing, and API error handling.

    Requires the 'requests' package and an internet connection.
    Falls back gracefully with a clear message if either is unavailable —
    this itself demonstrates the API Error Handling topic below.
    """

    win = tk.Toplevel(parent)
    win.title("Mini App — Live Joke Fetcher (REST API)")
    win.configure(bg=cfg.WHITE)
    center_window(win, 460, 380)
    win.resizable(False, False)

    tk.Label(
        win, text="🌐 Live Joke Fetcher", bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_H3
    ).pack(pady=(20, 4))

    tk.Label(
        win, text="Calls a public REST API and parses the JSON response live.",
        bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_SMALL
    ).pack(pady=(0, 15))

    joke_label = tk.Label(
        win, text="Click below to fetch a joke...", bg=cfg.WHITE, fg=cfg.TEXT,
        font=cfg.FONT_BODY, wraplength=380, justify="center"
    )
    joke_label.pack(pady=20, padx=20)

    status_label = tk.Label(win, text="", bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_SMALL)
    status_label.pack()

    def fetch_joke():
        joke_label.configure(text="Fetching...")
        win.update_idletasks()

        try:
            import requests  # imported here so the whole app still runs without it installed
        except ImportError:
            joke_label.configure(text="The 'requests' package isn't installed.")
            status_label.configure(
                text="Run:  pip install requests   (see requirements.txt)", fg=cfg.RED
            )
            return

        try:
            response = requests.get(
                "https://official-joke-api.appspot.com/random_joke", timeout=5
            )
            response.raise_for_status()   # raises an error for 4xx/5xx status codes
            data = response.json()        # parses the JSON response body

            joke_label.configure(text=f"{data['setup']}\n\n😄 {data['punchline']}")
            status_label.configure(text="GET request succeeded (200 OK)", fg=cfg.GREEN)

        except requests.exceptions.Timeout:
            joke_label.configure(text="The request timed out.")
            status_label.configure(text="Check your internet connection and try again.", fg=cfg.RED)
        except requests.exceptions.ConnectionError:
            joke_label.configure(text="Could not connect to the API.")
            status_label.configure(text="No internet connection detected.", fg=cfg.RED)
        except requests.exceptions.HTTPError as e:
            joke_label.configure(text="The API returned an error.")
            status_label.configure(text=str(e), fg=cfg.RED)
        except (KeyError, ValueError):
            joke_label.configure(text="Got a response, but couldn't parse it.")
            status_label.configure(text="Unexpected JSON shape from the API.", fg=cfg.RED)

    make_button(win, "🎲 Fetch a Joke", fetch_joke, cfg.BLUE).pack(pady=10, ipadx=10, ipady=4)


# ==========================================
# MODULE CONTENT
# ==========================================

MODULE = {
    "id": 7,
    "title": "API, Automation & Reporting",
    "description": "Talk to web APIs, automate repetitive tasks, and turn data into reports and charts.",
    "topics": [
        {
            "id": 1,
            "title": "API Introduction",
            "theory": "An API (Application Programming Interface) lets two programs talk to each other over a defined set of rules. A web API typically lets your Python program request data from a remote server — weather, currency rates, jokes, anything — over the internet, and get a structured response back, usually as JSON.",
            "key_points": [
                "API = a defined way for two programs to communicate.",
                "Web APIs usually communicate over HTTP.",
                "You send a request; the server sends back a response.",
                "Responses are commonly formatted as JSON.",
                "APIs let your app use data/services it doesn't own itself."
            ],
            "code_example": "# Conceptually:\n# Your program  --request-->  Weather API server\n# Your program  <--response-- {\"temp\": 24, \"condition\": \"Sunny\"}",
        },
        {
            "id": 2,
            "title": "REST API",
            "theory": "REST (Representational State Transfer) is the most common style of web API — resources (like 'users' or 'jokes') are accessed via URLs, and standard HTTP methods (GET, POST, PUT, DELETE) describe the action. A REST API is stateless: each request contains everything needed to understand it, with no memory of previous requests.",
            "key_points": [
                "REST APIs expose 'resources' via URLs (endpoints).",
                "HTTP methods describe the action: GET, POST, PUT, DELETE.",
                "Stateless — each request is independent, self-contained.",
                "Responses usually come back as JSON.",
                "Most public APIs today (weather, jokes, currency) are REST-based."
            ],
            "code_example": "# Example REST endpoints for a 'jokes' resource:\n# GET  /jokes/random   -> fetch one random joke\n# GET  /jokes/42        -> fetch joke with id 42\n# POST /jokes            -> create a new joke (if allowed)",
        },
        {
            "id": 3,
            "title": "GET Request",
            "theory": "A GET request retrieves data from a server without changing anything on it — it's the method used for reading/fetching. In Python, the third-party `requests` library makes this simple: `requests.get(url)` sends the request and returns a response object with the status code and body.",
            "key_points": [
                "GET retrieves data — doesn't change anything server-side.",
                "requests.get(url) sends the request.",
                "response.status_code tells you if it succeeded (200 = OK).",
                "response.json() parses a JSON body into Python data.",
                "Always set a timeout to avoid hanging forever."
            ],
            "code_example": "import requests\n\nresponse = requests.get(\"https://official-joke-api.appspot.com/random_joke\", timeout=5)\nprint(response.status_code)\nprint(response.json())",
        },
        {
            "id": 4,
            "title": "POST Request",
            "theory": "A POST request sends data to a server, typically to create something new — like submitting a form or creating a new record. The data you're sending goes in the request body, usually as JSON, passed to `requests.post(url, json=data)`.",
            "key_points": [
                "POST sends data to the server, often to create a resource.",
                "requests.post(url, json=data) sends a JSON body.",
                "The server usually responds with the created resource + an ID.",
                "Status code 201 commonly means 'Created' on success.",
                "Many public demo APIs (like JSONPlaceholder) let you test POST safely."
            ],
            "code_example": "import requests\n\nnew_post = {\"title\": \"Hello\", \"body\": \"My first API post\", \"userId\": 1}\nresponse = requests.post(\"https://jsonplaceholder.typicode.com/posts\", json=new_post)\nprint(response.status_code)\nprint(response.json())",
        },
        {
            "id": 5,
            "title": "JSON",
            "theory": "JSON (JavaScript Object Notation) is a lightweight, text-based data format that maps naturally onto Python dictionaries and lists — objects become dicts, arrays become lists. Python's built-in `json` module converts between JSON text and Python objects: `json.loads()` parses a JSON string, `json.dumps()` creates one.",
            "key_points": [
                "JSON objects {} map to Python dicts; arrays [] map to lists.",
                "json.loads(text) parses a JSON string into Python data.",
                "json.dumps(data) converts Python data into a JSON string.",
                "requests' response.json() does the parsing step for you automatically.",
                "Almost every modern REST API speaks JSON."
            ],
            "code_example": "import json\n\ndata = {\"name\": \"Ana\", \"scores\": [88, 92]}\ntext = json.dumps(data)\nprint(text, type(text))\n\nparsed = json.loads(text)\nprint(parsed[\"name\"], type(parsed))",
        },
        {
            "id": 6,
            "title": "Requests Library",
            "theory": "`requests` is the standard third-party library for making HTTP calls in Python — install it with `pip install requests`. It wraps up the low-level details (connections, headers, encoding) behind a simple, readable API: `requests.get()`, `.post()`, `.put()`, `.delete()`.",
            "key_points": [
                "Install with: pip install requests (see requirements.txt).",
                "Not part of the standard library — must be installed.",
                "requests.get/post/put/delete cover the common HTTP methods.",
                "response.headers, response.text, response.json() expose the reply.",
                "The Mini App above uses this exact library for its API call."
            ],
            "code_example": "import requests\n\nresponse = requests.get(\"https://api.github.com\")\nprint(response.headers[\"Content-Type\"])\nprint(response.json())",
        },
        {
            "id": 7,
            "title": "API Error Handling",
            "theory": "Network calls fail in more ways than local code: no internet connection, a slow/timing-out server, an invalid URL, or an error status from the server itself (like 404 or 500). Always wrap API calls in try/except, catching `requests.exceptions.ConnectionError`, `.Timeout`, and using `response.raise_for_status()` to catch bad HTTP status codes as exceptions.",
            "key_points": [
                "requests.exceptions.ConnectionError — no internet/can't reach host.",
                "requests.exceptions.Timeout — server took too long to respond.",
                "response.raise_for_status() raises an error on 4xx/5xx status codes.",
                "Never assume an API call will always succeed — always try/except it.",
                "The Mini App above handles all of these exact cases live."
            ],
            "code_example": "import requests\n\ntry:\n    response = requests.get(\"https://api.example.com/data\", timeout=5)\n    response.raise_for_status()\n    data = response.json()\nexcept requests.exceptions.Timeout:\n    print(\"Request timed out.\")\nexcept requests.exceptions.ConnectionError:\n    print(\"No internet connection.\")\nexcept requests.exceptions.HTTPError as e:\n    print(f\"Server returned an error: {e}\")",
        },
        {
            "id": 8,
            "title": "Automation",
            "theory": "Automation means writing a script that performs a repetitive task without manual effort each time — checking an API on a schedule, renaming a batch of files, or generating a daily report. Python is popular for this because its standard library already covers files, dates, and processes, and it's easy to glue together with third-party libraries.",
            "key_points": [
                "Automation = a script doing a repetitive task without manual work.",
                "Common examples: file organizing, report generation, data syncing.",
                "Python's ecosystem makes it a top choice for automation scripts.",
                "Automations are often triggered on a schedule (see Scheduling).",
                "Good automation scripts log what they did (see Module 4's logging)."
            ],
            "code_example": "import os\n\n# Simple automation: organize files in a folder by extension\nfor filename in os.listdir(\".\"):\n    if \".\" in filename:\n        ext = filename.split(\".\")[-1]\n        print(f\"{filename} -> would move to /{ext}_files/\")",
        },
        {
            "id": 9,
            "title": "Scheduling",
            "theory": "Scheduling runs a script automatically at set times, without a person triggering it. On your own machine, that's typically an OS tool — Windows Task Scheduler or a cron job on macOS/Linux — running `python my_script.py` at whatever interval you configure, rather than something built into the script itself.",
            "key_points": [
                "Scheduling = running a script automatically, on a timer.",
                "Windows: Task Scheduler. macOS/Linux: cron jobs.",
                "The script itself usually doesn't need special code for this.",
                "In-script alternative: the 'schedule' package for simple timers.",
                "Common use: nightly reports, periodic data checks, backups."
            ],
            "code_example": "# Example crontab entry (Linux/macOS) — runs daily at 8:00 AM:\n# 0 8 * * * /usr/bin/python3 /path/to/daily_report.py\n\n# In-script alternative using the 'schedule' package:\n# import schedule, time\n# schedule.every().day.at(\"08:00\").do(run_report)\n# while True:\n#     schedule.run_pending()\n#     time.sleep(60)",
        },
        {
            "id": 10,
            "title": "CSV Reporting",
            "theory": "Turning collected data into a CSV report is a common automation output — anyone can open it in Excel or Google Sheets. Python's built-in `csv` module (from Module 4) writes rows of data straight into a report file, ready to share or archive.",
            "key_points": [
                "CSV reports are simple, universal, and Excel/Sheets-friendly.",
                "csv.writer(file).writerow([...]) writes one row at a time.",
                "Always include a header row naming each column.",
                "Great output format for progress/quiz-score summaries.",
                "This platform could export your Progress Dashboard this way."
            ],
            "code_example": "import csv\n\nstudents = [(\"Ana\", 92), (\"Raj\", 85), (\"Priya\", 78)]\n\nwith open(\"score_report.csv\", \"w\", newline=\"\") as f:\n    writer = csv.writer(f)\n    writer.writerow([\"Name\", \"Score\"])\n    writer.writerows(students)\n\nprint(\"Report saved to score_report.csv\")",
        },
        {
            "id": 11,
            "title": "Pandas",
            "theory": "Pandas is a powerful third-party library for working with tabular data in Python, built around the `DataFrame` — think of it as a supercharged spreadsheet you can filter, sort, and analyze with code. It's the standard tool for any serious data analysis or reporting work. Install with `pip install pandas` (also listed in requirements.txt).",
            "key_points": [
                "pip install pandas — not in the standard library.",
                "DataFrame = a table structure with rows, columns, and labels.",
                "pd.read_csv(path) loads a CSV straight into a DataFrame.",
                "df['column'] selects a column; df[df['score'] > 80] filters rows.",
                "Common next step after collecting data via CSV or an API."
            ],
            "code_example": "# Requires: pip install pandas\nimport pandas as pd\n\ndf = pd.DataFrame({\n    \"name\": [\"Ana\", \"Raj\", \"Priya\"],\n    \"score\": [92, 85, 78]\n})\n\nprint(df)\nprint(\"Average score:\", df[\"score\"].mean())\nprint(df[df[\"score\"] > 80])",
        },
        {
            "id": 12,
            "title": "Matplotlib",
            "theory": "Matplotlib is the standard Python library for turning data into charts — line graphs, bar charts, pie charts, and more. It pairs naturally with Pandas: plot a DataFrame column directly, or feed it plain lists. Install with `pip install matplotlib` (also listed in requirements.txt).",
            "key_points": [
                "pip install matplotlib — not in the standard library.",
                "import matplotlib.pyplot as plt is the standard import.",
                "plt.plot(), plt.bar(), plt.pie() cover the common chart types.",
                "plt.savefig('chart.png') saves a chart as an image file.",
                "Pairs naturally with Pandas DataFrames for quick visual reports."
            ],
            "code_example": "# Requires: pip install matplotlib\nimport matplotlib.pyplot as plt\n\nmodules = [\"Mod 1\", \"Mod 2\", \"Mod 3\"]\nscores = [90, 75, 82]\n\nplt.bar(modules, scores, color=\"#2563EB\")\nplt.title(\"Quiz Scores by Module\")\nplt.ylabel(\"Score (%)\")\nplt.savefig(\"scores_chart.png\")\nprint(\"Chart saved to scores_chart.png\")",
        },
        {
            "id": 13,
            "title": "Final Dashboard Project",
            "theory": "Bring the whole platform full circle: build a small reporting script that\n\n1. Connects to this platform's own database.py and reads a user's quiz_scores.\n2. Uses Pandas to compute the average score per module.\n3. Exports the summary to a CSV report using the csv module.\n4. Uses Matplotlib to save a bar chart image of scores per module.\n\nThis mirrors exactly what this platform's own Progress Dashboard (ui/progress.py) shows you on-screen — just turned into a shareable file-based report instead.",
            "key_points": [
                "Combines database queries, Pandas analysis, CSV export, and charts.",
                "Reads real data from this platform's own quiz_scores table.",
                "Produces two deliverables: a CSV report and a PNG chart.",
                "This is the same data ui/progress.py already visualizes live.",
                "A great capstone tying together every module in this course."
            ],
            "code_example": "import pandas as pd\nimport matplotlib.pyplot as plt\nfrom database import get_connection\n\nconn = get_connection()\nrows = conn.execute(\"SELECT module_id, score, total FROM quiz_scores\").fetchall()\nconn.close()\n\ndf = pd.DataFrame(rows, columns=[\"module_id\", \"score\", \"total\"])\ndf[\"pct\"] = df[\"score\"] / df[\"total\"] * 100\n\nsummary = df.groupby(\"module_id\")[\"pct\"].mean()\nsummary.to_csv(\"final_report.csv\")\n\nsummary.plot(kind=\"bar\", color=\"#7C3AED\", title=\"Average Score by Module\")\nplt.savefig(\"final_dashboard.png\")",
        },
    ],
    "quiz": [
        {"question": "What does API stand for?", "options": ["Application Programming Interface", "Automated Program Instruction", "Application Process Integration", "Advanced Programming Index"], "answer_index": 0},
        {"question": "In REST APIs, which HTTP method retrieves data?", "options": ["POST", "DELETE", "GET", "PUT"], "answer_index": 2},
        {"question": "Which library is standard for making HTTP requests in Python?", "options": ["urllib-fast", "requests", "http-client", "web"], "answer_index": 1},
        {"question": "What does response.json() do?", "options": ["Sends a JSON request", "Parses the response body as JSON", "Deletes the response", "Converts JSON to CSV"], "answer_index": 1},
        {"question": "Which exception indicates no internet connection with requests?", "options": ["requests.exceptions.Timeout", "requests.exceptions.ConnectionError", "requests.exceptions.HTTPError", "KeyError"], "answer_index": 1},
        {"question": "What does response.raise_for_status() do?", "options": ["Always succeeds silently", "Raises an exception on 4xx/5xx status codes", "Prints the status code", "Retries the request automatically"], "answer_index": 1},
        {"question": "Where does Python usually get its scheduling from for scripts?", "options": ["Built into every script automatically", "OS tools like Task Scheduler or cron", "The requests library", "The csv module"], "answer_index": 1},
        {"question": "What is Pandas' core data structure called?", "options": ["Series only", "DataFrame", "Table", "Array"], "answer_index": 1},
        {"question": "Which library is used to create charts in Python?", "options": ["pandas", "requests", "matplotlib", "csv"], "answer_index": 2},
        {"question": "What format do most modern REST APIs use for responses?", "options": ["CSV", "JSON", "XML only", "Plain text only"], "answer_index": 1},
    ],
    "mini_app": {
        "title": "Live Joke Fetcher (REST API)",
        "description": "A real GET request to a public API with full JSON parsing and error handling (needs internet + 'requests').",
        "launch": launch_mini_app,
    },
}
