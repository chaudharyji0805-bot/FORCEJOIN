import re
from database import group_settings
from pyrogram import filters

def _clean_username(s: str) -> str:
    s = s.strip()
    s = s.replace("https://t.me/", "").replace("http://t.me/", "")
    if s.startswith("@"):
        s = s[1:]
    return s

def _is_valid_invite(url: str) -> bool:
    if not url:
        return False
    return bool(re.match(r"^https://t\.me/(joinchat/|\+)[A-Za-z0-9_-]+$", url)) or url.startswith("https://t.me/")

async def add_channel(client, message):
    if not message.from_user:
        return

    # only group admins
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ("administrator", "owner"):
        return await message.reply("❌ Only admins can use this command.")

    if len(message.command) < 2:
        return await message.reply("Usage:\n/addchannel @channel [invite_link(optional)]")

    username = _clean_username(message.command[1])
    invite = message.command[2] if len(message.command) >= 3 else ""

    doc = group_settings.find_one({"group_id": message.chat.id}) or {"group_id": message.chat.id, "channels": [], "enabled": True}
    channels = doc.get("channels", [])

    # avoid duplicates
    if any(c.get("username") == username for c in channels):
        return await message.reply("ℹ️ This channel is already added.")

    ch_doc = {"username": username}
    if invite and _is_valid_invite(invite):
        ch_doc["invite"] = invite

    channels.append(ch_doc)

    group_settings.update_one(
        {"group_id": message.chat.id},
        {"$set": {"channels": channels, "enabled": doc.get("enabled", True)}},
        upsert=True
    )

    await message.reply(f"✅ Added: @{username}")

async def remove_channel(client, message):
    if not message.from_user:
        return

    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ("administrator", "owner"):
        return await message.reply("❌ Only admins can use this command.")

    if len(message.command) < 2:
        return await message.reply("Usage:\n/removechannel @channel")

    username = _clean_username(message.command[1])
    doc = group_settings.find_one({"group_id": message.chat.id}) or {}
    channels = doc.get("channels", [])

    new_channels = [c for c in channels if c.get("username") != username]

    group_settings.update_one(
        {"group_id": message.chat.id},
        {"$set": {"channels": new_channels}},
        upsert=True
    )
    await message.reply(f"✅ Removed: @{username}")
