import os

# =========================
# Telegram Credentials
# =========================

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# =========================
# Database
# =========================

MONGO_URI = os.environ.get("MONGO_URI", "")

# =========================
# Admin / Owner
# =========================

OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

# =========================
# Optional Settings
# =========================

# Flood wait safety (seconds)
BROADCAST_DELAY = float(os.environ.get("BROADCAST_DELAY", "0.05"))

# Debug mode
DEBUG = bool(int(os.environ.get("DEBUG", "0")))
