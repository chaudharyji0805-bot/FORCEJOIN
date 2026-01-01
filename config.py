import os

# =========================
# Telegram Credentials
# =========================

API_ID = int(os.environ.get("API_ID", "25266584"))
API_HASH = os.environ.get("API_HASH", "051c368565939ecdbd8d5b37c26cc68e")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# =========================
# Database
# =========================

MONGO_URI = os.environ.get("MONGO_URI", "")

# =========================
# Admin / Owner
# =========================

OWNER_ID = int(os.environ.get("OWNER_ID", "7538572906"))

# =========================
# Optional Settings
# =========================

# Flood wait safety (seconds)
BROADCAST_DELAY = float(os.environ.get("BROADCAST_DELAY", "0.05"))

# Debug mode
DEBUG = bool(int(os.environ.get("DEBUG", "0")))
