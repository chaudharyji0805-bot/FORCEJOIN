from database import group_settings

async def enable_force(client, message):
    gid = message.chat.id
    group_settings.update_one(
        {"group_id": gid},
        {"$set": {"enabled": True}},
        upsert=True
    )
    await message.reply("✅ Force Join ENABLED for this group")


async def disable_force(client, message):
    gid = message.chat.id
    group_settings.update_one(
        {"group_id": gid},
        {"$set": {"enabled": False}},
        upsert=True
    )
    await message.reply("❌ Force Join DISABLED for this group")
