import os
import tkinter as tk
import webbrowser
from datetime import datetime

import config as cfg
from utils.helpers import make_card, make_button, friendly_date, percent, ScrollableFrame
from ui.dashboard import build_app_shell
from database import (
    get_completed_topic_ids, get_best_quiz_score, get_all_progress_counts,
    get_all_best_scores, has_certificate, issue_certificate, get_user_certificates
)
from modules.registry import ALL_MODULES, get_module, get_final_assessment_quiz, FINAL_ASSESSMENT_MODULE_ID


# ==========================================
# ELIGIBILITY CHECKS
# ==========================================

def is_module_eligible(user_id, module_id):
    module = get_module(module_id)
    completed = get_completed_topic_ids(user_id, module_id)
    all_topics_done = len(completed) >= len(module["topics"])

    best = get_best_quiz_score(user_id, module_id)
    quiz_passed = bool(best and best[1] and percent(best[0], best[1]) >= cfg.PASS_THRESHOLD)

    return all_topics_done and quiz_passed


def all_modules_complete(user_id):
    return all(is_module_eligible(user_id, m["id"]) for m in ALL_MODULES)


def is_final_assessment_passed(user_id):
    best = get_best_quiz_score(user_id, FINAL_ASSESSMENT_MODULE_ID)
    return bool(best and best[1] and percent(best[0], best[1]) >= cfg.PASS_THRESHOLD)


def is_final_assessment_unlocked(user_id):
    """The Final Assessment only becomes available once every module is done —
    it's a cumulative check, not something to attempt module-by-module."""
    return all_modules_complete(user_id)


def is_final_eligible(user_id):
    """Final Python Certificate requires BOTH: every module individually
    completed and passed, AND the cumulative Final Assessment passed."""
    return all_modules_complete(user_id) and is_final_assessment_passed(user_id)


# ==========================================
# CERTIFICATE FILE GENERATION
# ==========================================

def _certificate_id(user_id, cert_type, module_id):
    suffix = f"M{module_id}" if module_id else "FINAL"
    return f"PLH-{user_id}-{suffix}-{datetime.now().strftime('%Y%m%d%H%M%S')}"


def _generate_image_certificate(recipient_name, title_text, subtitle_text, cert_id, path):
    from PIL import Image, ImageDraw, ImageFont

    width, height = 1400, 990
    navy = (15, 23, 42)
    gold = (202, 138, 4)
    text_dark = (17, 24, 39)
    muted = (100, 116, 139)
    border_gray = (203, 213, 225)

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    border_margin = 40
    draw.rectangle(
        [border_margin, border_margin, width - border_margin, height - border_margin],
        outline=navy, width=6
    )
    draw.rectangle(
        [border_margin + 14, border_margin + 14, width - border_margin - 14, height - border_margin - 14],
        outline=gold, width=2
    )

    def font(size, bold=False):
        candidates = (
            ["arialbd.ttf", "DejaVuSans-Bold.ttf"] if bold
            else ["arial.ttf", "DejaVuSans.ttf"]
        )
        for name in candidates:
            try:
                return ImageFont.truetype(name, size)
            except (OSError, IOError):
                continue
        return ImageFont.load_default()

    def italic_font(size):
        for name in ["ariali.ttf", "DejaVuSans-Oblique.ttf"]:
            try:
                return ImageFont.truetype(name, size)
            except (OSError, IOError):
                continue
        return font(size)

    def centered_text(y, text, f, color):
        bbox = draw.textbbox((0, 0), text, font=f)
        w = bbox[2] - bbox[0]
        draw.text(((width - w) / 2, y), text, font=f, fill=color)
        return bbox[3] - bbox[1]

    # ---------- University logo (top center) ----------
    # Drop a PNG at config.LOGO_PATH to have it appear here automatically.
    logo_bottom = 95
    if os.path.exists(cfg.LOGO_PATH):
        try:
            logo = Image.open(cfg.LOGO_PATH).convert("RGBA")
            max_h = 100
            scale = max_h / logo.height
            logo = logo.resize((int(logo.width * scale), max_h))
            img.paste(logo, (int((width - logo.width) / 2), 55), logo)
            logo_bottom = 55 + max_h + 15
        except Exception:
            pass  # a broken/corrupt logo file should never break certificate generation

    centered_text(logo_bottom, cfg.APP_NAME, font(30, bold=True), navy)
    centered_text(logo_bottom + 65, "CERTIFICATE OF COMPLETION", font(42, bold=True), gold)
    centered_text(logo_bottom + 145, "This certifies that", font(20), muted)
    centered_text(logo_bottom + 190, recipient_name, font(48, bold=True), text_dark)
    centered_text(logo_bottom + 275, "has successfully completed", font(20), muted)
    centered_text(logo_bottom + 320, title_text, font(32, bold=True), navy)

    y_cursor = logo_bottom + 375
    if subtitle_text:
        centered_text(y_cursor, subtitle_text, font(18), muted)
        y_cursor += 40

    centered_text(y_cursor + 15, f"Awarded on {datetime.now().strftime('%d %B %Y')}", font(18), muted)

    # ---------- Authority signature (bottom) ----------
    # Drop a PNG at config.SIGNATURE_PATH (a scanned/transparent signature) to
    # have it appear above the line automatically; otherwise the line and
    # printed name/title still render on their own.
    sig_line_y = height - 175
    sig_line_half_w = 140
    sig_center_x = width / 2

    if os.path.exists(cfg.SIGNATURE_PATH):
        try:
            sig = Image.open(cfg.SIGNATURE_PATH).convert("RGBA")
            max_h = 70
            scale = max_h / sig.height
            sig = sig.resize((int(sig.width * scale), max_h))
            img.paste(sig, (int(sig_center_x - sig.width / 2), sig_line_y - max_h - 5), sig)
        except Exception:
            pass

    draw.line(
        [sig_center_x - sig_line_half_w, sig_line_y, sig_center_x + sig_line_half_w, sig_line_y],
        fill=border_gray, width=2
    )
    centered_text(sig_line_y + 10, cfg.SIGNATORY_NAME, font(18, bold=True), text_dark)
    centered_text(sig_line_y + 36, cfg.SIGNATORY_TITLE, font(15), muted)

    centered_text(height - 85, f"Certificate ID: {cert_id}", font(14), muted)

    img.save(path)
    return path


def _generate_text_certificate(recipient_name, title_text, subtitle_text, cert_id, path):
    lines = [
        "=" * 60,
        f"{cfg.APP_NAME.upper()} — CERTIFICATE OF COMPLETION".center(60),
        "=" * 60,
        "",
        "This certifies that".center(60),
        "",
        recipient_name.upper().center(60),
        "",
        "has successfully completed".center(60),
        "",
        title_text.center(60),
    ]
    if subtitle_text:
        lines.append(subtitle_text.center(60))

    lines += [
        "",
        f"Awarded on {datetime.now().strftime('%d %B %Y')}".center(60),
        "",
        "_" * 30,
        cfg.SIGNATORY_NAME.center(60),
        cfg.SIGNATORY_TITLE.center(60),
        "",
        f"Certificate ID: {cert_id}".center(60),
        "=" * 60,
    ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def generate_certificate_file(recipient_name, title_text, subtitle_text, cert_id):
    os.makedirs(cfg.CERT_FOLDER, exist_ok=True)
    try:
        path = os.path.join(cfg.CERT_FOLDER, f"{cert_id}.png")
        return _generate_image_certificate(recipient_name, title_text, subtitle_text, cert_id, path)
    except ImportError:
        path = os.path.join(cfg.CERT_FOLDER, f"{cert_id}.txt")
        return _generate_text_certificate(recipient_name, title_text, subtitle_text, cert_id, path)


# ==========================================
# ISSUING CERTIFICATES
# ==========================================

def issue_module_certificate_if_eligible(user, module_id):
    module = get_module(module_id)

    if has_certificate(user["id"], "module", module_id):
        return False, "already_issued"

    if not is_module_eligible(user["id"], module_id):
        return False, "not_eligible"

    cert_id = _certificate_id(user["id"], "module", module_id)
    path = generate_certificate_file(
        user["username"], f"Module {module_id}: {module['title']}", cfg.APP_NAME, cert_id
    )
    issue_certificate(user["id"], "module", module_id, path)
    return True, path


def issue_final_certificate_if_eligible(user):
    if has_certificate(user["id"], "final", None):
        return False, "already_issued"

    if not is_final_eligible(user["id"]):
        return False, "not_eligible"

    cert_id = _certificate_id(user["id"], "final", None)
    path = generate_certificate_file(
        user["username"], "The Complete Python Learning Hub Course",
        "All 7 Modules + Final Assessment", cert_id
    )
    issue_certificate(user["id"], "final", None, path)
    return True, path


# ==========================================
# CERTIFICATES SCREEN
# ==========================================

def show_certificates_page(root, user, callbacks, on_take_final_assessment=None):

    content = build_app_shell(root, user, "certificates", callbacks)

    scroller = ScrollableFrame(content)
    scroller.pack(fill="both", expand=True)

    wrap = tk.Frame(scroller.inner, bg=cfg.BG, padx=35, pady=30)
    wrap.pack(fill="both", expand=True)

    tk.Label(wrap, text="🏆 Certificates", bg=cfg.BG, fg=cfg.TEXT, font=cfg.FONT_H1).pack(anchor="w")
    tk.Label(
        wrap, text="8 certificates in total — one per module, plus the Final Python Certificate.",
        bg=cfg.BG, fg=cfg.MUTED, font=cfg.FONT_BODY
    ).pack(anchor="w", pady=(2, 25))

    def open_file(path):
        try:
            webbrowser.open(f"file://{os.path.abspath(path)}")
        except Exception:
            pass

    def cert_number_badge(parent, number, bg_color):
        badge = tk.Label(
            parent, text=str(number), bg=bg_color, fg=cfg.WHITE, font=cfg.FONT_BODY_BOLD,
            width=2, height=1
        )
        badge.pack(side="left", padx=(0, 14))
        return badge

    def refresh():
        for widget in wrap.winfo_children()[2:]:
            widget.destroy()

        earned_types = {}
        for c in get_user_certificates(user["id"]):
            earned_types[(c["certificate_type"], c["module_id"])] = c["file_path"]

        # ---------- Module certificates (1-7) ----------

        for module in ALL_MODULES:
            mid = module["id"]
            color = cfg.MODULE_COLORS[mid]
            light = cfg.MODULE_LIGHT_COLORS[mid]

            card = make_card(wrap)
            card.configure(padx=20, pady=16, bg=light)
            card.pack(fill="x", pady=6)

            key = ("module", mid)
            already_issued = key in earned_types

            row = tk.Frame(card, bg=light)
            row.pack(fill="x")

            badge_col = tk.Frame(row, bg=light)
            badge_col.pack(side="left")
            cert_number_badge(badge_col, mid, color)

            left = tk.Frame(row, bg=light)
            left.pack(side="left", fill="x", expand=True)

            tk.Label(
                left, text=f"{cfg.MODULE_ICONS[mid]}  Module {mid} — {module['title']}",
                bg=light, fg=cfg.TEXT, font=cfg.FONT_BODY_BOLD
            ).pack(anchor="w")

            if already_issued:
                tk.Label(left, text="✅ Certificate earned", bg=light, fg=cfg.GREEN, font=cfg.FONT_SMALL).pack(anchor="w", pady=(4, 0))
            elif is_module_eligible(user["id"], mid):
                tk.Label(left, text="🔓 Eligible — claim it!", bg=light, fg=color, font=cfg.FONT_SMALL).pack(anchor="w", pady=(4, 0))
            else:
                tk.Label(left, text="🔒 Complete all topics + pass the quiz to unlock", bg=light, fg=cfg.MUTED, font=cfg.FONT_SMALL).pack(anchor="w", pady=(4, 0))

            right = tk.Frame(row, bg=light)
            right.pack(side="right")

            if already_issued:
                make_button(right, "📄 View", lambda p=earned_types[key]: open_file(p), cfg.NAVY2, padx=14, pady=8).pack()
            else:
                def claim(m=mid):
                    ok, result = issue_module_certificate_if_eligible(user, m)
                    refresh()
                make_button(
                    right, "🎓 Claim Certificate", claim, color, padx=14, pady=8
                ).pack()

        # ---------- Final Assessment (gate before certificate #8) ----------

        assess_card = make_card(wrap)
        assess_card.configure(padx=20, pady=16, bg=cfg.PURPLE_LIGHT)
        assess_card.pack(fill="x", pady=(20, 6))

        row = tk.Frame(assess_card, bg=cfg.PURPLE_LIGHT)
        row.pack(fill="x")

        left = tk.Frame(row, bg=cfg.PURPLE_LIGHT)
        left.pack(side="left", fill="x", expand=True)

        tk.Label(left, text="📝 Final Assessment — All Modules", bg=cfg.PURPLE_LIGHT, fg=cfg.TEXT, font=cfg.FONT_BODY_BOLD).pack(anchor="w")

        assessment_best = get_best_quiz_score(user["id"], FINAL_ASSESSMENT_MODULE_ID)
        assessment_passed = is_final_assessment_passed(user["id"])
        unlocked = is_final_assessment_unlocked(user["id"])

        if assessment_passed:
            score, total, _ = assessment_best
            tk.Label(left, text=f"✅ Passed — {score}/{total} ({percent(score, total)}%)", bg=cfg.PURPLE_LIGHT, fg=cfg.GREEN, font=cfg.FONT_SMALL).pack(anchor="w", pady=(4, 0))
        elif not unlocked:
            tk.Label(left, text="🔒 Complete and pass all 7 modules to unlock", bg=cfg.PURPLE_LIGHT, fg=cfg.MUTED, font=cfg.FONT_SMALL).pack(anchor="w", pady=(4, 0))
        elif assessment_best:
            score, total, _ = assessment_best
            tk.Label(left, text=f"🔓 Unlocked — last attempt {score}/{total} ({percent(score, total)}%), try again to pass", bg=cfg.PURPLE_LIGHT, fg=cfg.PURPLE, font=cfg.FONT_SMALL).pack(anchor="w", pady=(4, 0))
        else:
            tk.Label(left, text="🔓 Unlocked — a cumulative quiz covering every module", bg=cfg.PURPLE_LIGHT, fg=cfg.PURPLE, font=cfg.FONT_SMALL).pack(anchor="w", pady=(4, 0))

        right = tk.Frame(row, bg=cfg.PURPLE_LIGHT)
        right.pack(side="right")

        if unlocked and not assessment_passed and on_take_final_assessment:
            btn_text = "🔁 Retake Assessment" if assessment_best else "📝 Take Final Assessment"
            make_button(right, btn_text, on_take_final_assessment, cfg.PURPLE, padx=14, pady=8).pack()

        # ---------- Final certificate (#8) ----------

        final_card = make_card(wrap)
        final_card.configure(padx=20, pady=20, bg=cfg.GOLD_LIGHT)
        final_card.pack(fill="x", pady=(14, 10))

        final_key = ("final", None)
        already_final = final_key in earned_types

        row = tk.Frame(final_card, bg=cfg.GOLD_LIGHT)
        row.pack(fill="x")

        badge_col = tk.Frame(row, bg=cfg.GOLD_LIGHT)
        badge_col.pack(side="left")
        cert_number_badge(badge_col, 8, cfg.GOLD)

        left = tk.Frame(row, bg=cfg.GOLD_LIGHT)
        left.pack(side="left", fill="x", expand=True)

        tk.Label(left, text="🎓 Final Python Certificate  (Certificate 8 of 8)", bg=cfg.GOLD_LIGHT, fg=cfg.TEXT, font=cfg.FONT_H3).pack(anchor="w")

        if already_final:
            tk.Label(left, text="✅ Awarded — you completed the whole course!", bg=cfg.GOLD_LIGHT, fg=cfg.GREEN, font=cfg.FONT_SMALL).pack(anchor="w", pady=(4, 0))
        elif is_final_eligible(user["id"]):
            tk.Label(left, text="🔓 All modules + Final Assessment passed — claim it!", bg=cfg.GOLD_LIGHT, fg=cfg.GOLD, font=cfg.FONT_SMALL).pack(anchor="w", pady=(4, 0))
        elif not unlocked:
            tk.Label(left, text="🔒 Complete and pass every module to unlock", bg=cfg.GOLD_LIGHT, fg=cfg.MUTED, font=cfg.FONT_SMALL).pack(anchor="w", pady=(4, 0))
        else:
            tk.Label(left, text="🔒 Pass the Final Assessment above to unlock", bg=cfg.GOLD_LIGHT, fg=cfg.MUTED, font=cfg.FONT_SMALL).pack(anchor="w", pady=(4, 0))

        right = tk.Frame(row, bg=cfg.GOLD_LIGHT)
        right.pack(side="right")

        if already_final:
            make_button(right, "📄 View", lambda: open_file(earned_types[final_key]), cfg.NAVY2, padx=14, pady=8).pack()
        else:
            def claim_final():
                issue_final_certificate_if_eligible(user)
                refresh()
            make_button(right, "🎓 Claim Final Certificate", claim_final, cfg.GOLD, padx=14, pady=8).pack()

        # Bottom spacer so the last card isn't flush against the window edge
        tk.Frame(wrap, bg=cfg.BG, height=20).pack()

    refresh()

