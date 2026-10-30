# ==========================================
# PYTHON LEARNING HUB
# Configuration and Theme Settings
# ==========================================

import os

# ---------- Paths ----------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "data")
CERT_FOLDER = os.path.join(BASE_DIR, "certificates")
LOG_FOLDER = os.path.join(BASE_DIR, "logs")
ASSETS_FOLDER = os.path.join(BASE_DIR, "assets")
DB_FILE = os.path.join(DATA_FOLDER, "python_learning_hub.db")

for _folder in (DATA_FOLDER, CERT_FOLDER, LOG_FOLDER, ASSETS_FOLDER):
    os.makedirs(_folder, exist_ok=True)

# ---------- Certificate branding ----------
# Drop your own files at these paths to brand every certificate. If a file
# is missing, the certificate still generates fine — it just falls back to
# plain text instead of the image (see ui/certificate.py).
LOGO_PATH = os.path.join(ASSETS_FOLDER, "university_logo.png")
SIGNATURE_PATH = os.path.join(ASSETS_FOLDER, "authority_signature.png")
SIGNATORY_NAME = "Nilesh Kumar Jadav"
SIGNATORY_TITLE = "HOD, Programming with Python"


# ---------- Application Settings ----------

APP_NAME = "Python Learning Hub"
APP_TAGLINE = "Learn Python by building, practicing, and proving it."

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 820

MIN_WIDTH = 1100
MIN_HEIGHT = 720

# Score needed (%) on a module quiz before its certificate unlocks
PASS_THRESHOLD = 70


# ---------- Main Theme Colors ----------

NAVY = "#0F172A"
NAVY2 = "#1E293B"
NAVY3 = "#334155"

BLUE = "#2563EB"
BLUE_LIGHT = "#EFF6FF"
BLUE_DARK = "#1D4ED8"

GREEN = "#16A34A"
GREEN_LIGHT = "#F0FDF4"

PURPLE = "#7C3AED"
PURPLE_LIGHT = "#F5F3FF"

ORANGE = "#EA580C"
ORANGE_LIGHT = "#FFF7ED"

TEAL = "#0F766E"
TEAL_LIGHT = "#F0FDFA"

RED = "#DC2626"
RED_LIGHT = "#FEF2F2"

GOLD = "#CA8A04"
GOLD_LIGHT = "#FEFCE8"

WHITE = "#FFFFFF"
BG = "#F5F7FB"
TEXT = "#111827"
MUTED = "#64748B"
BORDER = "#E2E8F0"


# ---------- Module Colors (used across cards, badges, progress bars) ----------

MODULE_COLORS = {
    1: BLUE,
    2: GREEN,
    3: PURPLE,
    4: ORANGE,
    5: TEAL,
    6: "#0891B2",
    7: "#9333EA",
}

MODULE_LIGHT_COLORS = {
    1: BLUE_LIGHT,
    2: GREEN_LIGHT,
    3: PURPLE_LIGHT,
    4: ORANGE_LIGHT,
    5: TEAL_LIGHT,
    6: "#ECFEFF",
    7: "#FAF5FF",
}

MODULE_ICONS = {
    1: "🧩",
    2: "🔁",
    3: "🗂️",
    4: "📁",
    5: "🏛️",
    6: "🗄️",
    7: "🌐",
}

# Kept for backward compatibility with earlier drafts of this project
MODULE_1_COLOR = MODULE_COLORS[1]
MODULE_2_COLOR = MODULE_COLORS[2]
MODULE_3_COLOR = MODULE_COLORS[3]
MODULE_4_COLOR = MODULE_COLORS[4]
MODULE_5_COLOR = MODULE_COLORS[5]
MODULE_6_COLOR = MODULE_COLORS[6]
MODULE_7_COLOR = MODULE_COLORS[7]


# ---------- Fonts ----------

FONT_FAMILY = "Segoe UI"

FONT_H1 = (FONT_FAMILY, 28, "bold")
FONT_H2 = (FONT_FAMILY, 20, "bold")
FONT_H3 = (FONT_FAMILY, 15, "bold")
FONT_BODY = (FONT_FAMILY, 11)
FONT_BODY_BOLD = (FONT_FAMILY, 11, "bold")
FONT_SMALL = (FONT_FAMILY, 9)
FONT_MONO = ("Consolas", 11)
