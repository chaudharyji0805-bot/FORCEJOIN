import os

# =========================
# Telegram Credentials
# =========================

def _get_int(name: str, default: int = 0) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


def _get_float(name: str, default: float = 0.0) -> float:
    try:
        return float(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


def _get_bool(name: str, default: bool = False) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.lower() in ("1", "true", "yes", "on")


API_ID = _get_int("API_ID", 0)
API_HASH = os.environ.get("API_HASH", "").strip()
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()

# =========================
# Database
# =========================
MONGO_URI = os.environ.get("MONGO_URI", "").strip()

# Log group (supergroup ID like -100xxxxxxxxxx) - optional
LOG_GROUP_ID = _get_int("LOG_GROUP_ID", 0)

# =========================
# Owner / Admin (Optional)
# =========================
OWNER_ID = _get_int("OWNER_ID", 0)  # INT ✅

# =========================
# Support Links (Optional)
# =========================
SUPPORT_CHAT = os.environ.get(
    "SUPPORT_CHAT",
    "https://t.me/Yaaro_kimehfill"
).strip()

SUPPORT_CHANNEL = os.environ.get(
    "SUPPORT_CHANNEL",
    "https://t.me/BotzEmpire"
).strip()

# =========================
# Optional Settings
# =========================
BROADCAST_DELAY = _get_float("BROADCAST_DELAY", 0.05)
DEBUG = _get_bool("DEBUG", False)

# =========================
# Basic Validation (NO CRASH)
# =========================
if DEBUG:
    print("⚙️ Config loaded")
    print("API_ID:", API_ID)
    print("OWNER_ID:", OWNER_ID)
    print("LOG_GROUP_ID:", LOG_GROUP_ID)
