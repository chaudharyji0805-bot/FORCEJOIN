from pymongo import MongoClient
from config import MONGO_URI

if not MONGO_URI:
    raise ValueError("MONGO_URI is missing! Set it in environment variables.")

mongo = MongoClient(MONGO_URI)
db = mongo.forcejoinbot

users = db.users
group_settings = db.group_settings
stats = db.stats
group_stats = db.group_stats

try:
    users.create_index("user_id", unique=True)
    group_settings.create_index("group_id", unique=True)
    group_stats.create_index("group_id", unique=True)
except Exception:
    pass
