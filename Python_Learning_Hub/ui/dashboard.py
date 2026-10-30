import tkinter as tk

import config as cfg
from utils.helpers import clear_window, make_button, make_card, build_progress_bar, percent
from database import get_all_progress_counts, get_all_best_scores, get_user_certificates
from modules.registry import ALL_MODULES


# ==========================================
# SHARED APP SHELL (sidebar + header, used by every post-login screen)
# ==========================================

NAV_ITEMS = [
    ("home", "🏠  Dashboard"),
    ("modules", "📚  Modules"),
    ("progress", "📊  Progress"),
    ("certificates", "🏆  Certificates"),
]


def build_app_shell(root, user, active_tab, callbacks):
    """Builds the header + sidebar shared by every screen after login.
    Returns the empty content Frame where the specific screen renders itself.

    callbacks: dict with keys 'home', 'modules', 'progress', 'certificates', 'logout'
    """

    clear_window(root)
    root.configure(bg=cfg.BG)

    # ---------- Header ----------

    header = tk.Frame(root, bg=cfg.NAVY, height=70)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)

    tk.Label(
        header, text="🐍 " + cfg.APP_NAME, bg=cfg.NAVY, fg=cfg.WHITE, font=cfg.FONT_H3,
        cursor="hand2"
    ).pack(side="left", padx=28, pady=20)
    header.children[list(header.children.keys())[0]].bind("<Button-1>", lambda e: callbacks["home"]())

    user_frame = tk.Frame(header, bg=cfg.NAVY)
    user_frame.pack(side="right", padx=28)

    tk.Label(
        user_frame, text=f"👤 {user['username']}  ·  {user['role']}", bg=cfg.NAVY, fg="#CBD5E1", font=cfg.FONT_SMALL
    ).pack(side="left", padx=(0, 15))

    make_button(user_frame, "Logout", callbacks["logout"], cfg.RED, padx=14, pady=6).pack(side="left")

    # ---------- Body: sidebar + content ----------

    body = tk.Frame(root, bg=cfg.BG)
    body.pack(fill="both", expand=True)

    sidebar = tk.Frame(body, bg=cfg.NAVY2, width=210)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    for key, label in NAV_ITEMS:
        is_active = (key == active_tab)
        btn = tk.Button(
            sidebar, text=label, anchor="w",
            bg=cfg.NAVY3 if is_active else cfg.NAVY2,
            fg=cfg.WHITE,
            activebackground=cfg.NAVY3, activeforeground=cfg.WHITE,
            font=cfg.FONT_BODY_BOLD if is_active else cfg.FONT_BODY,
            bd=0, padx=24, pady=14, cursor="hand2",
            command=callbacks.get(key, lambda: None)
        )
        btn.pack(fill="x")

    content = tk.Frame(body, bg=cfg.BG)
    content.pack(side="left", fill="both", expand=True)

    return content


# ==========================================
# DASHBOARD HOME SCREEN
# ==========================================

def show_dashboard_page(root, user, callbacks):

    content = build_app_shell(root, user, "home", callbacks)

    scroll = tk.Frame(content, bg=cfg.BG)
    scroll.pack(fill="both", expand=True, padx=35, pady=30)

    tk.Label(
        scroll, text=f"Welcome back, {user['username']}! 👋", bg=cfg.BG, fg=cfg.TEXT, font=cfg.FONT_H1
    ).pack(anchor="w")
    tk.Label(
        scroll, text="Here's where you left off.", bg=cfg.BG, fg=cfg.MUTED, font=cfg.FONT_BODY
    ).pack(anchor="w", pady=(2, 25))

    # ---------- Stat cards ----------

    stats_row = tk.Frame(scroll, bg=cfg.BG)
    stats_row.pack(fill="x", pady=(0, 30))

    progress_counts = get_all_progress_counts(user["id"])
    best_scores = get_all_best_scores(user["id"])
    certificates = get_user_certificates(user["id"])

    total_topics = sum(len(m["topics"]) for m in ALL_MODULES)
    completed_topics = sum(progress_counts.values())
    overall_pct = percent(completed_topics, total_topics)

    modules_passed = sum(
        1 for mid, (score, total, _) in best_scores.items()
        if total and (score / total * 100) >= cfg.PASS_THRESHOLD
    )

    def stat_card(parent, title, value, color):
        card = make_card(parent)
        card.configure(padx=22, pady=18)
        card.pack(side="left", fill="both", expand=True, padx=8)
        tk.Label(card, text=value, bg=cfg.WHITE, fg=color, font=cfg.FONT_H1).pack(anchor="w")
        tk.Label(card, text=title, bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_BODY).pack(anchor="w")
        return card

    stat_card(stats_row, "Overall Progress", f"{overall_pct}%", cfg.BLUE)
    stat_card(stats_row, "Topics Completed", f"{completed_topics}/{total_topics}", cfg.GREEN)
    stat_card(stats_row, "Modules Passed", f"{modules_passed}/7", cfg.PURPLE)
    stat_card(stats_row, "Certificates Earned", str(len(certificates)), cfg.GOLD)

    # ---------- Module progress overview ----------

    tk.Label(
        scroll, text="Your Modules", bg=cfg.BG, fg=cfg.TEXT, font=cfg.FONT_H3
    ).pack(anchor="w", pady=(10, 15))

    grid = tk.Frame(scroll, bg=cfg.BG)
    grid.pack(fill="x")

    for i, module in enumerate(ALL_MODULES):
        row, col = divmod(i, 2)
        color = cfg.MODULE_COLORS[module["id"]]
        light = cfg.MODULE_LIGHT_COLORS[module["id"]]
        icon = cfg.MODULE_ICONS[module["id"]]

        completed = progress_counts.get(module["id"], 0)
        total = len(module["topics"])
        pct = percent(completed, total)

        card = tk.Frame(grid, bg=cfg.WHITE, highlightbackground=cfg.BORDER, highlightthickness=1)
        card.grid(row=row, column=col, sticky="ew", padx=8, pady=8)
        grid.columnconfigure(col, weight=1)

        inner = tk.Frame(card, bg=cfg.WHITE, padx=18, pady=14)
        inner.pack(fill="x")

        top_row = tk.Frame(inner, bg=cfg.WHITE)
        top_row.pack(fill="x")

        tk.Label(top_row, text=icon, bg=cfg.WHITE, font=("Segoe UI", 18)).pack(side="left")
        tk.Label(
            top_row, text=f"  Module {module['id']} — {module['title']}", bg=cfg.WHITE, fg=cfg.TEXT,
            font=cfg.FONT_BODY_BOLD
        ).pack(side="left")
        tk.Label(top_row, text=f"{pct}%", bg=cfg.WHITE, fg=color, font=cfg.FONT_BODY_BOLD).pack(side="right")

        build_progress_bar(inner, pct, color, width=380).pack(fill="x", pady=(8, 0))

    make_button(scroll, "Go to Modules →", callbacks["modules"], cfg.BLUE).pack(anchor="w", pady=25, ipadx=10, ipady=4)
