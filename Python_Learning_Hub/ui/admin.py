import tkinter as tk

import config as cfg
from utils.helpers import clear_window, make_button, make_card, percent, friendly_date
from database import (
    get_all_students, count_all_certificates, count_certificates_by_type,
    get_all_progress_counts, get_all_best_scores, get_user_certificates
)
from modules.registry import ALL_MODULES


# ==========================================
# ADMIN SHELL (header + logout, no student sidebar)
# ==========================================

def build_admin_shell(root, user, callbacks):
    clear_window(root)
    root.configure(bg=cfg.BG)

    header = tk.Frame(root, bg=cfg.NAVY, height=70)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)

    tk.Label(
        header, text="🐍 " + cfg.APP_NAME + "   ·   Admin Panel",
        bg=cfg.NAVY, fg=cfg.WHITE, font=cfg.FONT_H3
    ).pack(side="left", padx=28, pady=20)

    user_frame = tk.Frame(header, bg=cfg.NAVY)
    user_frame.pack(side="right", padx=28)

    tk.Label(
        user_frame, text=f"👤 {user['username']}  ·  {user['role']}",
        bg=cfg.NAVY, fg="#CBD5E1", font=cfg.FONT_SMALL
    ).pack(side="left", padx=(0, 15))

    make_button(user_frame, "Logout", callbacks["logout"], cfg.RED, padx=14, pady=6).pack(side="left")

    body = tk.Frame(root, bg=cfg.BG)
    body.pack(fill="both", expand=True)

    return body


# ==========================================
# ADMIN DASHBOARD SCREEN
# ==========================================

def show_admin_dashboard_page(root, user, callbacks):

    body = build_admin_shell(root, user, callbacks)

    # ---------- Scrollable content ----------

    canvas = tk.Canvas(body, bg=cfg.BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(body, orient="vertical", command=canvas.yview)
    scroll = tk.Frame(canvas, bg=cfg.BG, padx=35, pady=30)

    scroll.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    win_id = canvas.create_window((0, 0), window=scroll, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(
        scroll, text=f"📊 Welcome, {user['username']} (Admin)", bg=cfg.BG, fg=cfg.TEXT, font=cfg.FONT_H1
    ).pack(anchor="w")
    tk.Label(
        scroll, text="An overview of everyone enrolled in the course.",
        bg=cfg.BG, fg=cfg.MUTED, font=cfg.FONT_BODY
    ).pack(anchor="w", pady=(2, 25))

    # ---------- Gather data ----------

    students = get_all_students()
    total_students = len(students)
    total_topics = sum(len(m["topics"]) for m in ALL_MODULES)

    total_certs = count_all_certificates()
    total_final_certs = count_certificates_by_type("final")

    per_student = []
    pct_sum = 0

    for s in students:
        progress_counts = get_all_progress_counts(s["id"])
        completed_topics = sum(progress_counts.values())
        pct = percent(completed_topics, total_topics)
        pct_sum += pct

        best_scores = get_all_best_scores(s["id"])
        modules_passed = sum(
            1 for mid, (score, total, _) in best_scores.items()
            if mid != 0 and total and (score / total * 100) >= cfg.PASS_THRESHOLD
        )

        certs = get_user_certificates(s["id"])
        has_final = any(c["certificate_type"] == "final" for c in certs)

        per_student.append({
            "user": s,
            "pct": pct,
            "modules_passed": modules_passed,
            "cert_count": len(certs),
            "has_final": has_final,
        })

    avg_completion = round(pct_sum / total_students) if total_students else 0

    # ---------- Stat cards ----------

    stats_row = tk.Frame(scroll, bg=cfg.BG)
    stats_row.pack(fill="x", pady=(0, 30))

    def stat_card(parent, title, value, color):
        card = make_card(parent)
        card.configure(padx=22, pady=18)
        card.pack(side="left", fill="both", expand=True, padx=8)
        tk.Label(card, text=value, bg=cfg.WHITE, fg=color, font=cfg.FONT_H1).pack(anchor="w")
        tk.Label(card, text=title, bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_BODY).pack(anchor="w")
        return card

    stat_card(stats_row, "Enrolled Students", str(total_students), cfg.BLUE)
    stat_card(stats_row, "Certificates Issued", str(total_certs), cfg.GOLD)
    stat_card(stats_row, "Final Certificates Earned", str(total_final_certs), cfg.PURPLE)
    stat_card(stats_row, "Avg. Course Completion", f"{avg_completion}%", cfg.GREEN)

    # ---------- Student table ----------

    header_row_wrap = tk.Frame(scroll, bg=cfg.BG)
    header_row_wrap.pack(fill="x", pady=(10, 0))

    tk.Label(
        header_row_wrap, text=f"Enrolled Students ({total_students})",
        bg=cfg.BG, fg=cfg.TEXT, font=cfg.FONT_H3
    ).pack(side="left")

    def refresh():
        show_admin_dashboard_page(root, user, callbacks)

    make_button(header_row_wrap, "🔄 Refresh", refresh, cfg.NAVY2, padx=12, pady=6).pack(side="right")

    tk.Label(scroll, text="", bg=cfg.BG).pack(pady=(0, 10))  # spacer

    if not students:
        empty_card = make_card(scroll)
        empty_card.configure(padx=20, pady=20)
        empty_card.pack(fill="x")
        tk.Label(
            empty_card, text="No students have registered yet.",
            bg=cfg.WHITE, fg=cfg.MUTED, font=cfg.FONT_BODY
        ).pack(anchor="w")
        return

    columns = [
        ("Student", 2),
        ("Email", 3),
        ("Joined", 2),
        ("Progress", 1),
        ("Modules Passed", 1),
        ("Certificates", 1),
        ("Final Cert", 1),
    ]

    table = tk.Frame(scroll, bg=cfg.WHITE, highlightbackground=cfg.BORDER, highlightthickness=1)
    table.pack(fill="x")

    for col_index, (label, weight) in enumerate(columns):
        table.columnconfigure(col_index, weight=weight)
        tk.Label(
            table, text=label, bg=cfg.NAVY2, fg=cfg.WHITE, font=cfg.FONT_SMALL,
            anchor="w", padx=10, pady=10
        ).grid(row=0, column=col_index, sticky="nsew")

    for row_index, row_data in enumerate(per_student, start=1):
        s = row_data["user"]
        row_bg = cfg.WHITE if row_index % 2 == 1 else cfg.BLUE_LIGHT

        values = [
            s["username"],
            s["email"],
            friendly_date(s["created_at"]),
            f"{row_data['pct']}%",
            f"{row_data['modules_passed']}/{len(ALL_MODULES)}",
            str(row_data["cert_count"]),
            "✅ Yes" if row_data["has_final"] else "—",
        ]

        for col_index, value in enumerate(values):
            fg = cfg.GREEN if (col_index == 6 and row_data["has_final"]) else cfg.TEXT
            tk.Label(
                table, text=value, bg=row_bg, fg=fg, font=cfg.FONT_SMALL,
                anchor="w", padx=10, pady=8
            ).grid(row=row_index, column=col_index, sticky="nsew")
