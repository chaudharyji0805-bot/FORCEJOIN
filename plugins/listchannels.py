from database import group_settings

async def list_channels(client, message):
    gid = message.chat.id
    data = group_settings.find_one({"group_id": gid})

    if not data or not data.get("channels"):
        return await message.reply("ℹ️ Is group me koi force join channel set nahi hai")

    text = "📢 **Force Join Channels (This Group)**\n\n"
    for i, ch in enumerate(data["channels"], start=1):
        text += f"{i}. @{ch['username']}\n"

    await message.reply(text)
