import tkinter as tk

import config as cfg
from utils.helpers import make_card, build_progress_bar, percent, friendly_date, ScrollableFrame
from ui.dashboard import build_app_shell
from database import get_all_progress_counts, get_all_best_scores
from modules.registry import ALL_MODULES


def show_progress_page(root, user, callbacks):

    content = build_app_shell(root, user, "progress", callbacks)

    scroller = ScrollableFrame(content)
    scroller.pack(fill="both", expand=True)

    wrap = tk.Frame(scroller.inner, bg=cfg.BG, padx=35, pady=30)
    wrap.pack(fill="both", expand=True)

    tk.Label(wrap, text="📊 Progress Dashboard", bg=cfg.BG, fg=cfg.TEXT, font=cfg.FONT_H1).pack(anchor="w")
    tk.Label(
        wrap, text="Your overall completion, module-by-module progress, and quiz history.",
        bg=cfg.BG, fg=cfg.MUTED, font=cfg.FONT_BODY
    ).pack(anchor="w", pady=(2, 25))

    progress_counts = get_all_progress_counts(user["id"])
    best_scores = get_all_best_scores(user["id"])

    total_topics = sum(len(m["topics"]) for m in ALL_MODULES)
    completed_topics = sum(progress_counts.values())
    overall_pct = percent(completed_topics, total_topics)

    # ---------- Overall summary card ----------

    summary = make_card(wrap)
    summary.configure(padx=26, pady=22)
    summary.pack(fill="x", pady=(0, 25))

    tk.Label(summary, text="Overall Completion", bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_H3).pack(anchor="w")
    tk.Label(
        summary, text=f"{completed_topics} of {total_topics} topics completed across all modules",
        bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_BODY
    ).pack(anchor="w", pady=(2, 12))

    build_progress_bar(summary, overall_pct, cfg.BLUE, width=900, height=16).pack(fill="x")
    tk.Label(summary, text=f"{overall_pct}%", bg=cfg.WHITE, fg=cfg.BLUE, font=cfg.FONT_H3).pack(anchor="e", pady=(6, 0))

    # ---------- Per-module progress ----------

    tk.Label(wrap, text="Module Progress", bg=cfg.BG, fg=cfg.TEXT, font=cfg.FONT_H3).pack(anchor="w", pady=(10, 12))

    for module in ALL_MODULES:
        mid = module["id"]
        color = cfg.MODULE_COLORS[mid]

        completed = progress_counts.get(mid, 0)
        total = len(module["topics"])
        pct = percent(completed, total)

        row_card = make_card(wrap)
        row_card.configure(padx=20, pady=14)
        row_card.pack(fill="x", pady=5)

        top = tk.Frame(row_card, bg=cfg.WHITE)
        top.pack(fill="x")

        tk.Label(
            top, text=f"{cfg.MODULE_ICONS[mid]} Module {mid} — {module['title']}",
            bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_BODY_BOLD
        ).pack(side="left")
        tk.Label(top, text=f"{completed}/{total} · {pct}%", bg=cfg.WHITE, fg=color, font=cfg.FONT_BODY_BOLD).pack(side="right")

        build_progress_bar(row_card, pct, color, width=900).pack(fill="x", pady=(8, 0))

    # ---------- Quiz scores table ----------

    tk.Label(wrap, text="Quiz Scores", bg=cfg.BG, fg=cfg.TEXT, font=cfg.FONT_H3).pack(anchor="w", pady=(25, 12))

    table_card = make_card(wrap)
    table_card.configure(padx=0, pady=0)
    table_card.pack(fill="x")

    header_row = tk.Frame(table_card, bg=cfg.NAVY2, padx=18, pady=10)
    header_row.pack(fill="x")

    for text, width in [("Module", 40), ("Best Score", 18), ("Percentage", 14), ("Status", 14), ("Last Attempt", 20)]:
        tk.Label(header_row, text=text, bg=cfg.NAVY2, fg=cfg.WHITE, font=cfg.FONT_SMALL, width=width, anchor="w").pack(side="left")

    if not best_scores:
        tk.Label(
            table_card, text="No quizzes attempted yet — head to a module and take one!",
            bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_BODY, padx=18, pady=20
        ).pack(fill="x")
    else:
        for module in ALL_MODULES:
            mid = module["id"]
            if mid not in best_scores:
                continue

            score, total, taken_at = best_scores[mid]
            pct = percent(score, total)
            passed = pct >= cfg.PASS_THRESHOLD

            row = tk.Frame(table_card, bg=cfg.WHITE, padx=18, pady=10)
            row.pack(fill="x")
            tk.Frame(table_card, bg=cfg.BORDER, height=1).pack(fill="x")

            tk.Label(row, text=f"Module {mid} — {module['title']}", bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_BODY, width=40, anchor="w").pack(side="left")
            tk.Label(row, text=f"{score}/{total}", bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_BODY, width=18, anchor="w").pack(side="left")
            tk.Label(row, text=f"{pct}%", bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_BODY, width=14, anchor="w").pack(side="left")
            tk.Label(
                row, text="✅ Passed" if passed else "❌ Not passed", bg=cfg.WHITE,
                fg=cfg.GREEN if passed else cfg.RED, font=cfg.FONT_BODY_BOLD, width=14, anchor="w"
            ).pack(side="left")
            tk.Label(row, text=friendly_date(taken_at), bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_SMALL, width=20, anchor="w").pack(side="left")
