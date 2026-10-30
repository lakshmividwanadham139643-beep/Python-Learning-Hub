import tkinter as tk
import webbrowser
import urllib.parse

import config as cfg
from utils.helpers import clear_window, make_button, make_card
from ui.dashboard import build_app_shell
from database import mark_topic_complete, get_completed_topic_ids
from modules.registry import get_module


def show_module_page(root, user, module_id, topic_id, callbacks, on_open_topic, on_open_quiz, on_open_mini_app):
    """Renders one topic within a module. topic_id is 1-based within module['topics']."""

    module = get_module(module_id)
    topics = module["topics"]
    topic = next((t for t in topics if t["id"] == topic_id), topics[0])

    content = build_app_shell(root, user, "modules", callbacks)
    color = cfg.MODULE_COLORS[module_id]
    light = cfg.MODULE_LIGHT_COLORS[module_id]

    completed_ids = get_completed_topic_ids(user["id"], module_id)

    # ---------- Module strip ----------

    strip = tk.Frame(content, bg=light, height=60)
    strip.pack(fill="x")
    strip.pack_propagate(False)

    tk.Label(
        strip, text=f"{cfg.MODULE_ICONS[module_id]}  Module {module_id} — {module['title']}",
        bg=light, fg=color, font=cfg.FONT_BODY_BOLD
    ).pack(side="left", padx=24, pady=18)

    make_button(
        strip, "🧠 Take Quiz", lambda: on_open_quiz(module_id), color, padx=16, pady=6
    ).pack(side="right", padx=(6, 24), pady=14)

    make_button(
        strip, f"🚀 {module['mini_app']['title']}", lambda: on_open_mini_app(module_id), cfg.NAVY2, padx=16, pady=6
    ).pack(side="right", padx=6, pady=14)

    # ---------- Body: topic sidebar + main panel ----------

    body = tk.Frame(content, bg=cfg.BG)
    body.pack(fill="both", expand=True)

    topic_list = tk.Frame(body, bg=cfg.WHITE, width=260, highlightbackground=cfg.BORDER, highlightthickness=1)
    topic_list.pack(side="left", fill="y")
    topic_list.pack_propagate(False)

    tk.Label(
        topic_list, text="TOPICS", bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_SMALL, anchor="w"
    ).pack(fill="x", padx=18, pady=(18, 6))

    topics_canvas = tk.Canvas(topic_list, bg=cfg.WHITE, highlightthickness=0)
    topics_canvas.pack(fill="both", expand=True, padx=4)

    topics_inner = tk.Frame(topics_canvas, bg=cfg.WHITE)
    topics_canvas.create_window((0, 0), window=topics_inner, anchor="nw", width=250)
    topics_inner.bind("<Configure>", lambda e: topics_canvas.configure(scrollregion=topics_canvas.bbox("all")))

    for t in topics:
        is_current = (t["id"] == topic["id"])
        is_done = t["id"] in completed_ids

        row = tk.Button(
            topics_inner,
            text=f"{'✅' if is_done else '⬜'}  {t['id']}. {t['title']}",
            anchor="w",
            bg=light if is_current else cfg.WHITE,
            fg=color if is_current else cfg.TEXT,
            activebackground=light,
            font=cfg.FONT_BODY_BOLD if is_current else cfg.FONT_BODY,
            bd=0, padx=14, pady=10, cursor="hand2",
            command=lambda tid=t["id"]: on_open_topic(module_id, tid)
        )
        row.pack(fill="x")

    # ---------- Main topic panel ----------

    main_panel = tk.Frame(body, bg=cfg.BG)
    main_panel.pack(side="left", fill="both", expand=True)

    scroll_canvas = tk.Canvas(main_panel, bg=cfg.BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(main_panel, orient="vertical", command=scroll_canvas.yview)
    inner = tk.Frame(scroll_canvas, bg=cfg.BG)

    inner.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))
    win_id = scroll_canvas.create_window((0, 0), window=inner, anchor="nw")
    scroll_canvas.configure(yscrollcommand=scrollbar.set)
    scroll_canvas.bind("<Configure>", lambda e: scroll_canvas.itemconfig(win_id, width=e.width))

    def _wheel(event):
        scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    scroll_canvas.bind_all("<MouseWheel>", _wheel)

    scroll_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    pad = tk.Frame(inner, bg=cfg.BG, padx=35, pady=25)
    pad.pack(fill="both", expand=True)

    tk.Label(
        pad, text=f"{topic['id']}. {topic['title']}", bg=cfg.BG, fg=cfg.TEXT, font=cfg.FONT_H1
    ).pack(anchor="w", pady=(0, 15))

    # ---------- Theory ----------

    theory_card = make_card(pad)
    theory_card.configure(padx=24, pady=20)
    theory_card.pack(fill="x", pady=(0, 15))

    tk.Label(theory_card, text="📖 Detailed Theory", bg=cfg.WHITE, fg=color, font=cfg.FONT_BODY_BOLD).pack(anchor="w", pady=(0, 8))
    for paragraph in topic["theory"].split("\n\n"):
        tk.Label(
            theory_card, text=paragraph, bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_BODY,
            wraplength=760, justify="left"
        ).pack(anchor="w", pady=(0, 8))

    # ---------- Key points ----------

    if topic["key_points"]:
        kp_card = make_card(pad)
        kp_card.configure(padx=24, pady=20, bg=light)
        kp_card.pack(fill="x", pady=(0, 15))

        tk.Label(kp_card, text="💡 Key Points", bg=light, fg=color, font=cfg.FONT_BODY_BOLD).pack(anchor="w", pady=(0, 8))
        for point in topic["key_points"]:
            tk.Label(
                kp_card, text=f"•  {point}", bg=light, fg=cfg.TEXT, font=cfg.FONT_BODY,
                wraplength=760, justify="left"
            ).pack(anchor="w", pady=2)

    # ---------- Code example ----------

    code_card = tk.Frame(pad, bg=cfg.NAVY, padx=24, pady=20)
    code_card.pack(fill="x", pady=(0, 15))

    tk.Label(code_card, text="💻 Code Example", bg=cfg.NAVY, fg="#94A3B8", font=cfg.FONT_BODY_BOLD).pack(anchor="w", pady=(0, 10))
    tk.Label(
        code_card, text=topic["code_example"], bg=cfg.NAVY, fg="#E2E8F0", font=cfg.FONT_MONO,
        justify="left", anchor="w"
    ).pack(anchor="w", fill="x")

    # ---------- Video button ----------

    video_row = tk.Frame(pad, bg=cfg.BG)
    video_row.pack(fill="x", pady=(0, 20))

    def open_video():
        query = urllib.parse.quote(f"Python {topic['title']}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    make_button(video_row, "🎥 Watch Video Lessons", open_video, cfg.RED).pack(side="left")

    # ---------- Navigation + mark complete ----------

    nav_row = tk.Frame(pad, bg=cfg.BG)
    nav_row.pack(fill="x", pady=(10, 30))

    idx = topics.index(topic)

    def go_prev():
        if idx > 0:
            on_open_topic(module_id, topics[idx - 1]["id"])

    def go_next():
        if idx < len(topics) - 1:
            on_open_topic(module_id, topics[idx + 1]["id"])

    def mark_done():
        mark_topic_complete(user["id"], module_id, topic["id"])
        if idx < len(topics) - 1:
            go_next()
        else:
            on_open_topic(module_id, topic["id"])  # refresh to show checkmark

    if idx > 0:
        make_button(nav_row, "← Previous", go_prev, cfg.NAVY2).pack(side="left")

    is_done = topic["id"] in completed_ids
    make_button(
        nav_row,
        "✅ Completed" if is_done else "✍ Mark as Complete",
        mark_done,
        cfg.GREEN if not is_done else cfg.MUTED
    ).pack(side="left", padx=10)

    if idx < len(topics) - 1:
        make_button(nav_row, "Next →", go_next, color).pack(side="right")
    else:
        make_button(nav_row, "🧠 Go to Quiz →", lambda: on_open_quiz(module_id), color).pack(side="right")
