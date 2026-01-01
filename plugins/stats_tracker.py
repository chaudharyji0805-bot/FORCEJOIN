import time
from database import stats

BOT_START_TIME = int(time.time())


def init_stats():
    if not stats.find_one({"_id": "global"}):
        stats.insert_one({
            "_id": "global",
            "messages_checked": 0,
            "force_actions": 0
        })


def inc_message():
    stats.update_one(
        {"_id": "global"},
        {"$inc": {"messages_checked": 1}},
        upsert=True
    )


def inc_force_action():
    stats.update_one(
        {"_id": "global"},
        {"$inc": {"force_actions": 1}},
        upsert=True
    )


def get_uptime():
    seconds = int(time.time()) - BOT_START_TIME
    h = seconds // 3600
    m = (seconds % 3600) // 60
    return f"{h}h {m}m"
