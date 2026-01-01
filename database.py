from pymongo import MongoClient
from config import MONGO_URI

mongo = MongoClient(MONGO_URI)
db = mongo.forcejoinbot

# users who interacted (DM or group)
users = db.users

# per-group force join settings
group_settings = db.group_settings

stats = db.stats

group_stats = db.group_stats
