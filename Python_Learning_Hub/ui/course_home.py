import tkinter as tk

import config as cfg
from utils.helpers import make_card, make_button, build_progress_bar, percent, ScrollableFrame
from ui.dashboard import build_app_shell
from database import get_all_progress_counts, get_all_best_scores
from modules.registry import ALL_MODULES


def show_course_home_page(root, user, callbacks, on_open_module):

    content = build_app_shell(root, user, "modules", callbacks)

    scroller = ScrollableFrame(content)
    scroller.pack(fill="both", expand=True)

    wrap = tk.Frame(scroller.inner, bg=cfg.BG)
    wrap.pack(fill="both", expand=True, padx=35, pady=30)

    tk.Label(wrap, text="📚 Python Modules", bg=cfg.BG, fg=cfg.TEXT, font=cfg.FONT_H1).pack(anchor="w")
    tk.Label(
        wrap, text="Work through each module in order — theory, examples, quiz, and a mini-app.",
        bg=cfg.BG, fg=cfg.MUTED, font=cfg.FONT_BODY
    ).pack(anchor="w", pady=(2, 25))

    progress_counts = get_all_progress_counts(user["id"])
    best_scores = get_all_best_scores(user["id"])

    for module in ALL_MODULES:
        mid = module["id"]
        color = cfg.MODULE_COLORS[mid]
        light = cfg.MODULE_LIGHT_COLORS[mid]
        icon = cfg.MODULE_ICONS[mid]

        completed = progress_counts.get(mid, 0)
        total_topics = len(module["topics"])
        pct = percent(completed, total_topics)

        best = best_scores.get(mid)
        quiz_text = "Not attempted yet"
        quiz_color = cfg.MUTED
        if best:
            score, qtotal, _ = best
            qpct = percent(score, qtotal)
            quiz_text = f"Best score: {score}/{qtotal} ({qpct}%)"
            quiz_color = cfg.GREEN if qpct >= cfg.PASS_THRESHOLD else cfg.ORANGE

        card = make_card(wrap)
        card.configure(padx=0, pady=0)
        card.pack(fill="x", pady=10)

        top = tk.Frame(card, bg=light, padx=24, pady=18)
        top.pack(fill="x")

        left = tk.Frame(top, bg=light)
        left.pack(side="left", fill="x", expand=True)

        tk.Label(left, text=f"{icon}  Module {mid} — {module['title']}", bg=light, fg=cfg.TEXT, font=cfg.FONT_H3).pack(anchor="w")
        tk.Label(left, text=module["description"], bg=light, fg=cfg.MUTED, font=cfg.FONT_BODY, wraplength=650, justify="left").pack(anchor="w", pady=(4, 10))

        meta_row = tk.Frame(left, bg=light)
        meta_row.pack(anchor="w")
        tk.Label(meta_row, text=f"{completed}/{total_topics} topics completed", bg=light, fg=cfg.TEXT, font=cfg.FONT_SMALL).pack(side="left", padx=(0, 20))
        tk.Label(meta_row, text=quiz_text, bg=light, fg=quiz_color, font=(cfg.FONT_FAMILY, 9, "bold")).pack(side="left")

        build_progress_bar(left, pct, color, width=650).pack(anchor="w", pady=(10, 0))

        right = tk.Frame(top, bg=light)
        right.pack(side="right", padx=(20, 0))

        label = "Continue" if completed > 0 else "Start Module"
        make_button(right, f"{label} →", lambda m=mid: on_open_module(m), color, padx=22, pady=12).pack()
