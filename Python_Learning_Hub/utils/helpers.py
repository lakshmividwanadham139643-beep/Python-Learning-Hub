import tkinter as tk
from datetime import datetime

import config as cfg


# ==========================================
# WINDOW / LAYOUT HELPERS
# ==========================================

def clear_window(root):
    """Destroys every widget currently in root, ready for a new screen."""
    # Any scrollable canvas on the outgoing screen bound its mousewheel
    # handler globally with bind_all(). If we don't remove that binding
    # here, it keeps firing after the canvas is destroyed below and
    # raises "invalid command name ... canvas" errors on every scroll.
    root.unbind_all("<MouseWheel>")
    for widget in root.winfo_children():
        widget.destroy()


def center_window(win, width, height):
    """Centers a Tk window (or Toplevel) on the screen."""
    win.update_idletasks()
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")


# ==========================================
# FORMATTING HELPERS
# ==========================================

def now_iso():
    return datetime.now().isoformat()


def friendly_date(iso_string):
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%d %b %Y, %I:%M %p")
    except (ValueError, TypeError):
        return iso_string or "—"


def percent(part, whole):
    if not whole:
        return 0
    return round((part / whole) * 100)


def score_remark(pct):
    """Returns a short encouraging remark + badge emoji based on a score %."""
    if pct >= 90:
        return "Outstanding! 🏆", cfg.GOLD
    if pct >= cfg.PASS_THRESHOLD:
        return "Nice work — passed! 🎉", cfg.GREEN
    if pct >= 40:
        return "Getting there — review and retry. 💪", cfg.ORANGE
    return "Keep practicing — you'll get it. 📘", cfg.RED


# ==========================================
# SHARED WIDGET BUILDERS
# ==========================================

def build_header(root, subtitle=None, on_logo_click=None):
    """Standard navy header bar used on every screen."""

    header = tk.Frame(root, bg=cfg.NAVY, height=76)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)

    title_frame = tk.Frame(header, bg=cfg.NAVY)
    title_frame.pack(side="left", padx=28)

    logo = tk.Label(
        title_frame,
        text="🐍 " + cfg.APP_NAME,
        bg=cfg.NAVY,
        fg=cfg.WHITE,
        font=cfg.FONT_H3,
        cursor="hand2" if on_logo_click else "arrow"
    )
    logo.pack(anchor="w", pady=(14, 0))

    if on_logo_click:
        logo.bind("<Button-1>", lambda e: on_logo_click())

    if subtitle:
        tk.Label(
            title_frame,
            text=subtitle,
            bg=cfg.NAVY,
            fg="#94A3B8",
            font=cfg.FONT_SMALL
        ).pack(anchor="w")

    return header


def build_progress_bar(parent, pct, color, width=220, height=10, bg=cfg.BORDER):
    """Draws a simple horizontal progress bar using a Canvas. Returns the Canvas."""

    canvas = tk.Canvas(
        parent,
        width=width,
        height=height,
        bg=bg,
        highlightthickness=0
    )
    canvas.pack(anchor="w")

    fill_width = max(0, min(width, int(width * pct / 100)))

    canvas.create_rectangle(0, 0, width, height, fill=bg, outline="")
    if fill_width > 0:
        canvas.create_rectangle(0, 0, fill_width, height, fill=color, outline="")

    return canvas


def make_button(parent, text, command, bg, fg=None, font=None, padx=20, pady=10):
    fg = fg or cfg.WHITE
    font = font or cfg.FONT_BODY_BOLD

    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=bg,
        activeforeground=fg,
        font=font,
        bd=0,
        padx=padx,
        pady=pady,
        cursor="hand2"
    )


def make_card(parent, bg=None):
    bg = bg or cfg.WHITE
    return tk.Frame(
        parent,
        bg=bg,
        highlightbackground=cfg.BORDER,
        highlightthickness=1
    )


class ScrollableFrame(tk.Frame):
    """A vertically scrollable frame. Put widgets inside self.inner."""

    def __init__(self, parent, bg=None):
        bg = bg or cfg.BG
        super().__init__(parent, bg=bg)

        canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)

        self.inner = tk.Frame(canvas, bg=bg)

        self.inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _resize_inner(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", _resize_inner)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
