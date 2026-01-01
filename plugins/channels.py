from config import OWNER_ID
from database import channels


async def add_channel(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ You are not allowed")

    if len(message.command) < 2:
        return await message.reply(
            "Usage:\n"
            "/addchannel @channelusername [invite_link]"
        )

    username = message.command[1].replace("@", "")
    invite = message.command[2] if len(message.command) > 2 else None

    if channels.find_one({"username": username}):
        return await message.reply("⚠️ Channel already added")

    channels.insert_one({
        "username": username,
        "invite": invite
    })

    await message.reply(f"✅ Channel @{username} added successfully")


async def remove_channel(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ You are not allowed")

    if len(message.command) < 2:
        return await message.reply(
            "Usage:\n/removechannel @channelusername"
        )

    username = message.command[1].replace("@", "")
    channels.delete_one({"username": username})

    await message.reply(f"❌ Channel @{username} removed")
