import tkinter as tk

import config as cfg
from database import initialize_database

from ui.landing import show_landing_page
from ui.login import show_login_page
from ui.register import show_register_page
from ui.dashboard import show_dashboard_page
from ui.course_home import show_course_home_page
from ui.module_page import show_module_page
from ui.quiz import show_quiz_page, show_final_assessment_page
from ui.progress import show_progress_page
from ui.certificate import show_certificates_page
from ui.admin import show_admin_dashboard_page


# ==========================================
# INITIALIZE DATABASE
# ==========================================

initialize_database()


# ==========================================
# CREATE MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title(cfg.APP_NAME)
root.geometry(f"{cfg.WINDOW_WIDTH}x{cfg.WINDOW_HEIGHT}")
root.minsize(cfg.MIN_WIDTH, cfg.MIN_HEIGHT)

current_user = None


# ==========================================
# NAVIGATION FUNCTIONS
# (each screen only needs to call one of these — no screen imports another
#  screen directly, so this is the single place that wires the whole app)
# ==========================================

def go_landing():
    show_landing_page(root, on_get_started=go_register, on_login=go_login)


def go_login():
    show_login_page(root, on_login_success=on_login_success, on_show_register=go_register, on_back_to_landing=go_landing)


def go_register():
    show_register_page(root, on_show_login=go_login)


def on_login_success(user_data):
    global current_user
    current_user = user_data
    if user_data["role"] == "Admin":
        go_admin_dashboard()
    else:
        go_dashboard()


def logout():
    global current_user
    current_user = None
    go_landing()


def shell_callbacks():
    """Callbacks passed to build_app_shell — same five actions from any screen."""
    return {
        "home": go_dashboard,
        "modules": go_course_home,
        "progress": go_progress,
        "certificates": go_certificates,
        "logout": logout,
    }


def go_dashboard():
    show_dashboard_page(root, current_user, shell_callbacks())


def go_admin_dashboard():
    show_admin_dashboard_page(root, current_user, shell_callbacks())


def go_course_home():
    show_course_home_page(root, current_user, shell_callbacks(), on_open_module=go_module_first_topic)


def go_module_first_topic(module_id):
    go_module(module_id, topic_id=1)


def go_module(module_id, topic_id):
    show_module_page(
        root, current_user, module_id, topic_id,
        callbacks=shell_callbacks(),
        on_open_topic=go_module,
        on_open_quiz=go_quiz,
        on_open_mini_app=launch_mini_app,
    )


def launch_mini_app(module_id):
    from modules.registry import get_module
    module = get_module(module_id)
    module["mini_app"]["launch"](root)


def go_quiz(module_id):
    show_quiz_page(root, current_user, module_id, shell_callbacks(), on_finish=go_course_home)


def go_progress():
    show_progress_page(root, current_user, shell_callbacks())


def go_certificates():
    show_certificates_page(root, current_user, shell_callbacks(), on_take_final_assessment=go_final_assessment)


def go_final_assessment():
    show_final_assessment_page(root, current_user, shell_callbacks(), on_finish=go_certificates)


# ==========================================
# START APPLICATION
# ==========================================

go_landing()
root.mainloop()
