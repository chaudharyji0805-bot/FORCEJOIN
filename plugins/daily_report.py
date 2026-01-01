import asyncio
from datetime import datetime, timedelta, timezone

from config import LOG_GROUP_ID
from database import users, group_settings, stats
from plugins.stats_tracker import get_uptime

IST = timezone(timedelta(hours=5, minutes=30))

async def daily_report(client):
    if not LOG_GROUP_ID:
        return

    while True:
        now = datetime.now(IST)
        nxt = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        sleep_for = (nxt - now).total_seconds()
        await asyncio.sleep(sleep_for)

        s = stats.find_one({"_id": "global"}) or {}
        text = (
            "📊 **Daily Bot Report**\n\n"
            f"⏱ Uptime: {get_uptime()}\n"
            f"👤 Total Users: {users.count_documents({})}\n"
            f"👥 Active Groups: {group_settings.count_documents({})}\n"
            f"💬 Messages Checked: {s.get('messages_checked', 0)}\n"
            f"📢 Force Actions: {s.get('force_actions', 0)}"
        )
        try:
            await client.send_message(LOG_GROUP_ID, text)
        except Exception:
            pass
