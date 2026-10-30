import tkinter as tk

import config as cfg
from utils.helpers import clear_window, make_button
from modules.registry import ALL_MODULES


def show_landing_page(root, on_get_started, on_login):

    clear_window(root)
    root.configure(bg=cfg.BG)

    # ---------- Header ----------

    header = tk.Frame(root, bg=cfg.NAVY, height=76)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header, text="🐍 " + cfg.APP_NAME, bg=cfg.NAVY, fg=cfg.WHITE, font=cfg.FONT_H3
    ).pack(side="left", padx=28, pady=22)

    make_button(header, "Log In", on_login, cfg.BLUE, padx=18, pady=8).pack(
        side="right", padx=28, pady=16
    )

    # ---------- Hero section ----------

    hero = tk.Frame(root, bg=cfg.BG)
    hero.pack(fill="x", pady=(50, 30))

    tk.Label(
        hero, text=cfg.APP_NAME, bg=cfg.BG, fg=cfg.TEXT, font=cfg.FONT_H1
    ).pack()

    tk.Label(
        hero, text=cfg.APP_TAGLINE, bg=cfg.BG, fg=cfg.MUTED, font=cfg.FONT_BODY
    ).pack(pady=(6, 0))

    tk.Label(
        hero,
        text="7 modules • detailed theory • real code examples • quizzes • mini-apps • certificates",
        bg=cfg.BG, fg=cfg.MUTED, font=cfg.FONT_SMALL
    ).pack(pady=(10, 0))

    make_button(hero, "🚀 Get Started — It's Free", on_get_started, cfg.GREEN, padx=30, pady=14).pack(pady=25)

    # ---------- Module preview cards ----------

    cards_label = tk.Label(
        root, text="What you'll learn", bg=cfg.BG, fg=cfg.TEXT, font=cfg.FONT_H3
    )
    cards_label.pack(pady=(10, 15))

    grid = tk.Frame(root, bg=cfg.BG)
    grid.pack(padx=40, pady=(0, 30))

    for i, module in enumerate(ALL_MODULES):
        row, col = divmod(i, 4)
        color = cfg.MODULE_COLORS[module["id"]]
        light = cfg.MODULE_LIGHT_COLORS[module["id"]]
        icon = cfg.MODULE_ICONS[module["id"]]

        card = tk.Frame(grid, bg=light, width=230, height=140, highlightbackground=cfg.BORDER, highlightthickness=1)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card.grid_propagate(False)

        tk.Label(card, text=icon, bg=light, font=("Segoe UI", 24)).pack(pady=(14, 4))
        tk.Label(
            card, text=f"Module {module['id']}", bg=light, fg=color, font=cfg.FONT_SMALL
        ).pack()
        tk.Label(
            card, text=module["title"], bg=light, fg=cfg.TEXT, font=cfg.FONT_BODY_BOLD,
            wraplength=200, justify="center"
        ).pack(padx=10, pady=(2, 10))

    for col in range(4):
        grid.columnconfigure(col, weight=1)
