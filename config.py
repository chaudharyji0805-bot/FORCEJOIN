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

# Log group (supergroup ID like -100xxxxxxxxxx) - optional
LOG_GROUP_ID = int(os.environ.get("LOG_GROUP_ID", "0"))

# =========================
# Owner / Admin (Optional)
# =========================
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))  # INT ✅

# =========================
# Support Links (Optional)
# =========================
# Examples:
# SUPPORT_CHAT = "https://t.me/YourSupportChat"
# SUPPORT_CHANNEL = "https://t.me/YourSupportChannel"
SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "https://t.me/Yaaro_kimehfill")
SUPPORT_CHANNEL = os.environ.get("SUPPORT_CHANNEL", "https://t.me/BotzEmpire")

# =========================
# Optional Settings
# =========================
BROADCAST_DELAY = float(os.environ.get("BROADCAST_DELAY", "0.05"))
DEBUG = bool(int(os.environ.get("DEBUG", "0")))
