from database import group_stats


async def group_stats_cmd(client, message):
    data = group_stats.find_one({"group_id": message.chat.id})

    if not data:
        return await message.reply("📊 No stats available yet.")

    await message.reply(
        "📊 **Group Activity Stats**\n\n"
        f"💬 Messages Checked: {data.get('messages', 0)}\n"
        f"📢 Force Actions: {data.get('actions', 0)}"
    )
