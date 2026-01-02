from database import group_settings
from pyrogram import filters

async def enable_force(client, message):
    group_settings.update_one(
        {"group_id": message.chat.id},
        {"$set": {"enabled": True}},
        upsert=True
    )
    await message.reply("✅ Force Join enabled for this group.")

async def disable_force(client, message):
    group_settings.update_one(
        {"group_id": message.chat.id},
        {"$set": {"enabled": False}},
        upsert=True
    )
    await message.reply("❌ Force Join disabled for this group.")
