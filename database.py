from pymongo import MongoClient
from config import MONGO_URI

# ─────────────────────────────
# MONGODB CONNECTION
# ─────────────────────────────
mongo = MongoClient(MONGO_URI)
db = mongo.forcejoinbot


# ─────────────────────────────
# COLLECTIONS
# ─────────────────────────────

# Users who interacted with bot (DM / Group)
# Used for: broadcast, user stats
users = db.users


# Per-group force join configuration
# Stores:
# group_id, enabled, channels, admins, warnings etc.
group_settings = db.group_settings


# Global bot statistics
# Stores:
# messages_checked, force_actions
stats = db.stats


# Per-group activity statistics
# Stores:
# group_id, messages, actions
group_stats = db.group_stats
