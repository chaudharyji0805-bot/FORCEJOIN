from pymongo import MongoClient
from config import MONGO_URI

# ─────────────────────────────
# MONGODB CONNECTION
# ─────────────────────────────
if not MONGO_URI:
    raise ValueError("MONGO_URI is missing! Set it in environment variables.")

mongo = MongoClient(MONGO_URI)
db = mongo.forcejoinbot

# ─────────────────────────────
# COLLECTIONS
# ─────────────────────────────

# Users who interacted with bot (DM / Group)
# Used for: broadcast, user stats
users = db.users

# Per-group force join configuration
# Stores: group_id, enabled, channels, admins, warnings etc.
group_settings = db.group_settings

# Global bot statistics
# Stores: messages_checked, force_actions
stats = db.stats

# Per-group activity statistics
# Stores: group_id, messages, actions
group_stats = db.group_stats

# ─────────────────────────────
# INDEXES (performance + duplicates safety)
# ─────────────────────────────
try:
    users.create_index("user_id", unique=True)
    group_settings.create_index("group_id", unique=True)
    group_stats.create_index("group_id", unique=True)
except Exception:
    # Index creation can fail on limited permissions or during cold start; ignore safely
    pass
