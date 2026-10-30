import tkinter as tk

import config as cfg
from utils.helpers import make_card, make_button, percent, score_remark
from ui.dashboard import build_app_shell
from database import save_quiz_score
from modules.registry import get_module, get_final_assessment_quiz, FINAL_ASSESSMENT_MODULE_ID


def _render_quiz(root, user, callbacks, title_text, subtitle_extra, quiz, save_module_id, color, on_finish):
    """Shared renderer used by both a single module's quiz and the cumulative
    Final Assessment — identical look and grading logic either way."""

    content = build_app_shell(root, user, "modules", callbacks)

    if not quiz:
        empty = tk.Frame(content, bg=cfg.BG)
        empty.pack(fill="both", expand=True)
        tk.Label(
            empty, text="Quiz coming soon.", bg=cfg.BG, fg=cfg.MUTED, font=cfg.FONT_H3
        ).pack(expand=True)
        return

    wrap = tk.Frame(content, bg=cfg.BG, padx=40, pady=30)
    wrap.pack(fill="both", expand=True)

    tk.Label(
        wrap, text=title_text, bg=cfg.BG, fg=cfg.TEXT, font=cfg.FONT_H2
    ).pack(anchor="w", pady=(0, 6))
    tk.Label(
        wrap, text=f"{len(quiz)} questions · {cfg.PASS_THRESHOLD}% needed to pass{subtitle_extra}",
        bg=cfg.BG, fg=cfg.MUTED, font=cfg.FONT_BODY
    ).pack(anchor="w", pady=(0, 20))

    selected_answers = {}  # question_index -> option_index

    scroll_canvas = tk.Canvas(wrap, bg=cfg.BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(wrap, orient="vertical", command=scroll_canvas.yview)
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

    for q_index, question in enumerate(quiz):
        card = make_card(inner)
        card.configure(padx=22, pady=18)
        card.pack(fill="x", pady=8)

        label_text = f"{q_index + 1}. {question['question']}"
        if "source_module" in question:
            label_text += f"   (Module {question['source_module']})"

        tk.Label(
            card, text=label_text, bg=cfg.WHITE, fg=cfg.TEXT,
            font=cfg.FONT_BODY_BOLD, wraplength=780, justify="left"
        ).pack(anchor="w", pady=(0, 10))

        choice_var = tk.IntVar(value=-1)

        for opt_index, option_text in enumerate(question["options"]):
            tk.Radiobutton(
                card, text=option_text, variable=choice_var, value=opt_index,
                bg=cfg.WHITE, fg=cfg.TEXT, font=cfg.FONT_BODY, anchor="w",
                selectcolor=cfg.BLUE_LIGHT, activebackground=cfg.WHITE,
                command=lambda qi=q_index, cv=choice_var: selected_answers.__setitem__(qi, cv.get())
            ).pack(anchor="w", pady=2)

    result_label = tk.Label(wrap, text="", bg=cfg.BG, font=cfg.FONT_H3)
    result_label.pack(pady=(10, 0))

    def submit_quiz():
        unanswered = [i for i in range(len(quiz)) if i not in selected_answers]
        if unanswered:
            result_label.configure(
                text=f"Please answer all questions — {len(unanswered)} remaining.", fg=cfg.RED
            )
            return

        score = sum(
            1 for i, q in enumerate(quiz) if selected_answers[i] == q["answer_index"]
        )
        total = len(quiz)
        pct = percent(score, total)

        save_quiz_score(user["id"], save_module_id, score, total)

        remark, remark_color = score_remark(pct)
        result_label.configure(text=f"You scored {score}/{total} ({pct}%) — {remark}", fg=remark_color)

        submit_btn.configure(state="disabled")
        make_button(
            wrap, "Continue →", on_finish, color
        ).pack(pady=15, ipadx=10, ipady=4)

    submit_btn = make_button(wrap, "Submit Quiz", submit_quiz, color)
    submit_btn.pack(pady=15, ipadx=15, ipady=6)


def show_quiz_page(root, user, module_id, callbacks, on_finish):
    """A single module's own quiz — unchanged behavior from before."""
    module = get_module(module_id)
    _render_quiz(
        root, user, callbacks,
        title_text=f"🧠 Module {module_id} Quiz — {module['title']}",
        subtitle_extra="",
        quiz=module["quiz"],
        save_module_id=module_id,
        color=cfg.MODULE_COLORS[module_id],
        on_finish=on_finish,
    )


def show_final_assessment_page(root, user, callbacks, on_finish):
    """The cumulative Final Assessment, covering all 7 modules — passing this
    (on top of completing every module) unlocks the Final Python Certificate."""
    quiz = get_final_assessment_quiz()
    _render_quiz(
        root, user, callbacks,
        title_text="🎓 Final Assessment — All Modules",
        subtitle_extra="  ·  covers every module, needed for the Final Python Certificate",
        quiz=quiz,
        save_module_id=FINAL_ASSESSMENT_MODULE_ID,
        color=cfg.GOLD,
        on_finish=on_finish,
    )
