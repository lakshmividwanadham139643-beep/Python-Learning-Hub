import re
import tkinter as tk

import config as cfg
from utils.helpers import clear_window, make_button, make_card
from utils.password import hash_password
from database import find_user, create_user

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def show_register_page(root, on_show_login):

    clear_window(root)
    root.configure(bg=cfg.BG)

    header = tk.Frame(root, bg=cfg.NAVY, height=76)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(
        header, text="🐍 " + cfg.APP_NAME, bg=cfg.NAVY, fg=cfg.WHITE, font=cfg.FONT_H3
    ).pack(side="left", padx=28, pady=22)

    content = tk.Frame(root, bg=cfg.BG)
    content.pack(fill="both", expand=True)

    card = make_card(content)
    card.configure(padx=50, pady=35)
    card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.40, relheight=0.82)

    tk.Label(card, text="Create Your Account", bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_H2).pack(anchor="w", pady=(0, 4))
    tk.Label(
        card, text="Start learning Python today — it's free.", bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_BODY
    ).pack(anchor="w", pady=(0, 20))

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
        wrapper.pack(fill="x", pady=(0, 14))
        return entry, var

    user_entry, user_var = labeled_entry("USERNAME")
    email_entry, email_var = labeled_entry("EMAIL")
    pass_entry, pass_var = labeled_entry("PASSWORD", show="•")
    confirm_entry, confirm_var = labeled_entry("CONFIRM PASSWORD", show="•")

    message_label = tk.Label(card, text="", bg=cfg.WHITE, fg=cfg.RED, font=cfg.FONT_SMALL, wraplength=380, justify="left")
    message_label.pack(anchor="w", pady=(0, 10))

    def attempt_register():
        username = user_var.get().strip()
        email = email_var.get().strip()
        password = pass_var.get()
        confirm = confirm_var.get()

        if not username or not email or not password or not confirm:
            message_label.configure(fg=cfg.RED, text="Please fill in all fields.")
            return
        if len(username) < 3:
            message_label.configure(fg=cfg.RED, text="Username must be at least 3 characters long.")
            return
        if not EMAIL_PATTERN.match(email):
            message_label.configure(fg=cfg.RED, text="Please enter a valid email address.")
            return
        if len(password) < 6:
            message_label.configure(fg=cfg.RED, text="Password must be at least 6 characters long.")
            return
        if password != confirm:
            message_label.configure(fg=cfg.RED, text="Passwords do not match.")
            return
        if find_user(username) or find_user(email):
            message_label.configure(fg=cfg.RED, text="An account with that username or email already exists.")
            return

        create_user(username, email, hash_password(password))
        message_label.configure(fg=cfg.GREEN, text="Account created successfully! Redirecting to login...")
        card.after(1200, on_show_login)

    confirm_entry.bind("<Return>", lambda e: attempt_register())

    make_button(card, "CREATE ACCOUNT", attempt_register, cfg.BLUE).pack(fill="x", pady=(6, 20), ipady=4)

    switch_frame = tk.Frame(card, bg=cfg.WHITE)
    switch_frame.pack(fill="x")
    tk.Label(switch_frame, text="Already have an account?", bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_SMALL).pack(side="left")
    login_link = tk.Label(switch_frame, text=" Log in", bg=cfg.WHITE, fg=cfg.BLUE, font=(cfg.FONT_FAMILY, 9, "bold"), cursor="hand2")
    login_link.pack(side="left")
    login_link.bind("<Button-1>", lambda e: on_show_login())

    user_entry.focus_set()
