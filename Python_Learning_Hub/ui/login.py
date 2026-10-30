import tkinter as tk

import config as cfg
from utils.helpers import clear_window, make_button, make_card
from utils.password import verify_password
from database import find_user


def show_login_page(root, on_login_success, on_show_register, on_back_to_landing=None):

    clear_window(root)
    root.configure(bg=cfg.BG)

    # ---------- Header ----------

    header = tk.Frame(root, bg=cfg.NAVY, height=76)
    header.pack(fill="x")
    header.pack_propagate(False)

    logo = tk.Label(
        header, text="🐍 " + cfg.APP_NAME, bg=cfg.NAVY, fg=cfg.WHITE, font=cfg.FONT_H3,
        cursor="hand2" if on_back_to_landing else "arrow"
    )
    logo.pack(side="left", padx=28, pady=22)
    if on_back_to_landing:
        logo.bind("<Button-1>", lambda e: on_back_to_landing())

    # ---------- Content ----------

    content = tk.Frame(root, bg=cfg.BG)
    content.pack(fill="both", expand=True)

    card = make_card(content)
    card.configure(padx=50, pady=40)
    card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.38, relheight=0.60)

    tk.Label(card, text="Welcome Back", bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_H2).pack(anchor="w", pady=(0, 4))
    tk.Label(
        card, text="Log in to continue your Python journey.", bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_BODY
    ).pack(anchor="w", pady=(0, 25))

    def labeled_entry(label_text, show=None):
        tk.Label(card, text=label_text, bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_BODY_BOLD, anchor="w").pack(fill="x", pady=(0, 4))
        var = tk.StringVar()
        wrapper = tk.Frame(card, bg=cfg.WHITE)
        entry = tk.Entry(wrapper, textvariable=var, bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_BODY, bd=0, highlightthickness=0, show=show)
        entry.pack(fill="x", ipady=8)
        underline = tk.Frame(wrapper, bg=cfg.BORDER, height=2)
        underline.pack(fill="x")
        entry.bind("<FocusIn>", lambda e: underline.configure(bg=cfg.BLUE))
        entry.bind("<FocusOut>", lambda e: underline.configure(bg=cfg.BORDER))
        wrapper.pack(fill="x", pady=(0, 18))
        return entry, var

    user_entry, user_var = labeled_entry("USERNAME OR EMAIL")
    pass_entry, pass_var = labeled_entry("PASSWORD", show="•")

    error_label = tk.Label(card, text="", bg=cfg.WHITE, fg=cfg.RED, font=cfg.FONT_SMALL, wraplength=380, justify="left")
    error_label.pack(anchor="w", pady=(0, 10))

    def attempt_login():
        error_label.configure(text="")
        username = user_var.get().strip()
        password = pass_var.get()

        if not username or not password:
            error_label.configure(text="Please enter your username/email and password.")
            return

        user = find_user(username)
        if not user:
            error_label.configure(text="No account found with that username or email.")
            return

        if not verify_password(password, user["password_hash"]):
            error_label.configure(text="Incorrect password. Please try again.")
            return

        on_login_success({
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
        })

    pass_entry.bind("<Return>", lambda e: attempt_login())
    user_entry.bind("<Return>", lambda e: attempt_login())

    make_button(card, "LOG IN", attempt_login, cfg.BLUE).pack(fill="x", pady=(6, 20), ipady=4)

    switch_frame = tk.Frame(card, bg=cfg.WHITE)
    switch_frame.pack(fill="x")
    tk.Label(switch_frame, text="Don't have an account?", bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_SMALL).pack(side="left")
    register_link = tk.Label(switch_frame, text=" Create one", bg=cfg.WHITE, fg=cfg.BLUE, font=(cfg.FONT_FAMILY, 9, "bold"), cursor="hand2")
    register_link.pack(side="left")
    register_link.bind("<Button-1>", lambda e: on_show_register())

    tk.Label(
        card, text="Demo: admin / Admin@123   •   student / Student@123",
        bg=cfg.WHITE, fg=cfg.BORDER, font=cfg.FONT_SMALL
    ).pack(side="bottom", pady=(15, 0))

    user_entry.focus_set()
