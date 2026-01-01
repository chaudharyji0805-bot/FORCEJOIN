from pymongo import MongoClient
from config import MONGO_URI

# Mongo connection
mongo = MongoClient(MONGO_URI)
db = mongo.forcejoinbot

# Collections
users = db.users
channels = db.channels     # ✅ FORCE JOIN CHANNELS
banned = db.banned         # (future use)
premium = db.premium       # (future use)
