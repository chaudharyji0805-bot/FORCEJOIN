from config import LOG_GROUP_ID
from pyrogram.enums import ParseMode


async def notify_bot_start(client):
    if not LOG_GROUP_ID:
        return
    try:
        await client.send_message(
            LOG_GROUP_ID,
            "🚀 **Bot Started Successfully**\n\n"
            "✅ Status: Online\n"
            "♻️ Reason: Restart / Deploy / Crash Recovery",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception:
        pass


async def notify_group_add(client, chat):
    if not LOG_GROUP_ID:
        return
    try:
        title = chat.title or "Unknown Group"
        await client.send_message(
            LOG_GROUP_ID,
            f"➕ **Bot Added to Group**\n\n"
            f"📛 Group: {title}\n"
            f"🆔 ID: `{chat.id}`",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception:
        pass


async def notify_user_start(client, user):
    if not LOG_GROUP_ID:
        return
    try:
        name = user.first_name or "Unknown User"
        await client.send_message(
            LOG_GROUP_ID,
            f"👤 **User Started Bot (DM)**\n\n"
            f"👤 Name: {name}\n"
            f"🆔 ID: `{user.id}`",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception:
        pass


async def notify_force_set(client, chat, channel):
    if not LOG_GROUP_ID:
        return
    try:
        title = chat.title or "Unknown Group"
        await client.send_message(
            LOG_GROUP_ID,
            f"⚙️ **Force Join Updated**\n\n"
            f"📛 Group: {title}\n"
            f"🆔 Group ID: `{chat.id}`\n"
            f"📢 Channel: @{channel}",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception:
        pass
