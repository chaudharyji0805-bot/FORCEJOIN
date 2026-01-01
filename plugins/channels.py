from config import OWNER_ID
from database import group_channels


def _get_group(chat):
    return chat.id if chat.type in ("group", "supergroup") else None


async def add_channel(client, message):
    if message.from_user.id != OWNER_ID:
        return

    group_id = _get_group(message.chat)
    if not group_id:
        return await message.reply("❌ Use this command in a group")

    if len(message.command) < 2:
        return await message.reply(
            "Usage:\n/addchannel @channel [invite_link]"
        )

    username = message.command[1].replace("@", "")
    invite = message.command[2] if len(message.command) > 2 else None

    data = group_channels.find_one({"group_id": group_id}) or {
        "group_id": group_id,
        "channels": []
    }

    for ch in data["channels"]:
        if ch["username"] == username:
            return await message.reply("⚠️ Channel already added for this group")

    data["channels"].append({
        "username": username,
        "invite": invite
    })

    group_channels.update_one(
        {"group_id": group_id},
        {"$set": data},
        upsert=True
    )

    await message.reply(f"✅ @{username} added for this group")


async def remove_channel(client, message):
    if message.from_user.id != OWNER_ID:
        return

    group_id = _get_group(message.chat)
    if not group_id:
        return

    if len(message.command) < 2:
        return await message.reply("Usage:\n/removechannel @channel")

    username = message.command[1].replace("@", "")

    group_channels.update_one(
        {"group_id": group_id},
        {"$pull": {"channels": {"username": username}}}
    )

    await message.reply(f"❌ @{username} removed from this group")
