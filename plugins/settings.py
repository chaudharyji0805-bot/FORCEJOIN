from database import group_settings
from config import OWNER_ID

async def _is_admin(client, message) -> bool:
    if OWNER_ID and message.from_user.id == OWNER_ID:
        return True
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ("administrator", "creator")

async def enable_force(client, message):
    if not await _is_admin(client, message):
        return await message.reply("❌ Only admins can use this command.")

    await group_settings.update_one(
        {"group_id": message.chat.id},
        {"$set": {"enabled": True}},
        upsert=True
    )
    await message.reply("✅ Force Join enabled for this group.")

async def disable_force(client, message):
    if not await _is_admin(client, message):
        return await message.reply("❌ Only admins can use this command.")

    await group_settings.update_one(
        {"group_id": message.chat.id},
        {"$set": {"enabled": False}},
        upsert=True
    )
    await message.reply("❌ Force Join disabled for this group.")
