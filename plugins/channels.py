from config import OWNER_ID
from database import group_settings


def ensure_group(message):
    if message.chat.type not in ("group", "supergroup"):
        return False
    return True


async def add_channel(client, message):
    # only owner
    if message.from_user.id != OWNER_ID:
        return

    # only group
    if not ensure_group(message):
        return await message.reply("❌ Ye command sirf GROUP me use hogi")

    group_id = message.chat.id

    if len(message.command) < 2:
        return await message.reply(
            "Usage:\n/addchannel @channel [invite_link]\n\n"
            "⚠️ Is command ko usi group me use karo jahan force join chahiye"
        )

    username = message.command[1].replace("@", "")
    invite = message.command[2] if len(message.command) > 2 else None

    doc = group_channels.find_one({"group_id": group_id})
    if not doc:
        doc = {"group_id": group_id, "channels": []}

    for ch in doc["channels"]:
        if ch["username"] == username:
            return await message.reply("⚠️ Ye channel is group ke liye pehle se set hai")

    doc["channels"].append({
        "username": username,
        "invite": invite
    })

    group_channels.update_one(
        {"group_id": group_id},
        {"$set": doc},
        upsert=True
    )

    await message.reply(
        f"✅ **Force join set ho gaya**\n\n"
        f"Group: `{group_id}`\n"
        f"Channel: @{username}"
    )


async def remove_channel(client, message):
    if message.from_user.id != OWNER_ID:
        return

    if not ensure_group(message):
        return await message.reply("❌ Ye command sirf GROUP me use hogi")

    group_id = message.chat.id

    if len(message.command) < 2:
        return await message.reply("Usage:\n/removechannel @channel")

    username = message.command[1].replace("@", "")

    group_channels.update_one(
        {"group_id": group_id},
        {"$pull": {"channels": {"username": username}}}
    )

    await message.reply(
        f"❌ Channel @{username} **is group se remove** kar diya gaya"
    )
