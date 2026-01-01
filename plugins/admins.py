from database import group_settings

def is_group_admin(data, user_id):
    return user_id in data.get("admins", [])


async def add_admin(client, message):
    gid = message.chat.id
    uid = int(message.command[1])

    group_settings.update_one(
        {"group_id": gid},
        {"$addToSet": {"admins": uid}},
        upsert=True
    )

    await message.reply(f"✅ `{uid}` added as group admin")


async def remove_admin(client, message):
    gid = message.chat.id
    uid = int(message.command[1])

    group_settings.update_one(
        {"group_id": gid},
        {"$pull": {"admins": uid}}
    )

    await message.reply(f"❌ `{uid}` removed from group admin list")
