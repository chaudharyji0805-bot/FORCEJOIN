from database import group_settings


def is_group_admin(data, user_id):
    if not data:
        return False
    return user_id in data.get("admins", [])


async def add_admin(client, message):
    if not message.chat or not message.from_user:
        return

    if len(message.command) < 2:
        return await message.reply("Usage: /addadmin <user_id>")

    try:
        uid = int(message.command[1])
    except ValueError:
        return await message.reply("❌ Invalid user ID")

    gid = message.chat.id

    try:
        await group_settings.update_one(
            {"group_id": gid},
            {"$addToSet": {"admins": uid}},
            upsert=True,
        )
    except Exception:
        return await message.reply("❌ Failed to add admin")

    await message.reply(f"✅ `{uid}` added as group admin")


async def remove_admin(client, message):
    if not message.chat or not message.from_user:
        return

    if len(message.command) < 2:
        return await message.reply("Usage: /removeadmin <user_id>")

    try:
        uid = int(message.command[1])
    except ValueError:
        return await message.reply("❌ Invalid user ID")

    gid = message.chat.id

    try:
        await group_settings.update_one(
            {"group_id": gid},
            {"$pull": {"admins": uid}},
        )
    except Exception:
        return await message.reply("❌ Failed to remove admin")

    await message.reply(f"❌ `{uid}` removed from group admin list")
