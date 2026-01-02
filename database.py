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

        # create indexes (non-blocking)
        async def _ensure_indexes():
            try:
                await users.create_index("user_id", unique=True)
                await group_settings.create_index("group_id", unique=True)
                await group_stats.create_index("group_id", unique=True)
            except Exception:
                pass

    except Exception as e:
        print("❌ Mongo connection error:", e)
else:
    print("⚠️ MONGO_URI not set, database disabled")
