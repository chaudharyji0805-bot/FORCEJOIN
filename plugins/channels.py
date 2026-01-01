from config import OWNER_ID
from database import group_settings


def ensure_group(message):
    return message.chat.type in ("group", "supergroup")


async def add_channel(client, message):
    if message.from_user.id != OWNER_ID:
        return

    if not ensure_group(message):
        return await message.reply("❌ Ye command sirf GROUP me use hogi")

    group_id = message.chat.id

    if len(message.command) < 2:
        return await message.reply(
            "Usage:\n/addchannel @channel [invite_link]"
        )

    username = message.command[1].replace("@", "")
    invite = message.command[2] if len(message.command) > 2 else None

    data = group_settings.find_one({"group_id": group_id}) or {
        "group_id": group_id,
        "enabled": True,
        "admins": [OWNER_ID],
        "channels": []
    }

    for ch in data["channels"]:
        if ch["username"] == username:
            return await message.reply("⚠️ Ye channel is group ke liye already set hai")

    data["channels"].append({
        "username": username,
        "invite": invite
    })

    group_settings.update_one(
        {"group_id": group_id},
        {"$set": data},
        upsert=True
    )

    await message.reply(f"✅ @{username} is group ke liye add ho gaya")


async def remove_channel(client, message):
    if message.from_user.id != OWNER_ID:
        return

    if not ensure_group(message):
        return await message.reply("❌ Ye command sirf GROUP me use hogi")

    group_id = message.chat.id

    if len(message.command) < 2:
        return await message.reply("Usage:\n/removechannel @channel")

    username = message.command[1].replace("@", "")

    group_settings.update_one(
        {"group_id": group_id},
        {"$pull": {"channels": {"username": username}}}
    )

    await message.reply(f"❌ @{username} is group se remove ho gaya")
