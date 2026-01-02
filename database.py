from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

mongo = None
db = None

users = None
group_settings = None
stats = None
group_stats = None

if MONGO_URI:
    try:
        mongo = AsyncIOMotorClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )
        db = mongo.forcejoinbot

        users = db.users
        group_settings = db.group_settings
        stats = db.stats
        group_stats = db.group_stats

    except Exception as e:
        print("Mongo connection error:", e)
else:
    print("⚠️ MONGO_URI not set")
