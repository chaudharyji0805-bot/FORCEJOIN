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

# Log group (supergroup ID, negative number like -100xxxxxxxxxx)
LOG_GROUP_ID = int(os.environ.get("LOG_GROUP_ID", "0"))

# =========================
# Admin / Owner (Optional)
# =========================
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

# =========================
# Optional Settings
# =========================
# Flood wait safety (seconds)
BROADCAST_DELAY = float(os.environ.get("BROADCAST_DELAY", "0.05"))

# Debug mode (0/1)
DEBUG = bool(int(os.environ.get("DEBUG", "0")))
