import asyncio
from config import LOG_GROUP_ID
from database import users, group_settings, stats
from plugins.stats_tracker import get_uptime


async def daily_report(client):
    while True:
        await asyncio.sleep(86400)  # 24 hours

        s = stats.find_one({"_id": "global"}) or {}
        await client.send_message(
            LOG_GROUP_ID,
            "📊 **Daily Bot Report**\n\n"
            f"⏱ Uptime: {get_uptime()}\n"
            f"👤 Total Users: {users.count_documents({})}\n"
            f"👥 Active Groups: {group_settings.count_documents({})}\n"
            f"💬 Messages Checked: {s.get('messages_checked', 0)}\n"
            f"📢 Force Actions: {s.get('force_actions', 0)}"
        )
