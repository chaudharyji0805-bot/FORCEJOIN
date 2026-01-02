from config import LOG_GROUP_ID
from pyrogram.enums import ParseMode
from pyrogram.utils import escape_markdown


async def notify_bot_start(client):
    if not LOG_GROUP_ID:
        return
    try:
        await client.send_message(
            LOG_GROUP_ID,
            "🚀 **Bot Started Successfully**\n\n✅ Status: Online",
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception:
        pass


async def notify_group_add(client, chat):
    if not LOG_GROUP_ID or not chat:
        return
    try:
        title = escape_markdown(chat.title or "Unknown Group", version=2)
        await client.send_message(
            LOG_GROUP_ID,
            f"➕ **Bot Added to Group**\n\n"
            f"📛 Group: {title}\n"
            f"🆔 ID: `{chat.id}`",
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception:
        pass


async def notify_user_start(client, user):
    if not LOG_GROUP_ID or not user:
        return
    try:
        name = escape_markdown(user.first_name or "Unknown", version=2)
        await client.send_message(
            LOG_GROUP_ID,
            f"👤 **User Started Bot (DM)**\n\n"
            f"👤 Name: {name}\n"
            f"🆔 ID: `{user.id}`",
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception:
        pass


async def notify_force_set(client, chat, channel):
    if not LOG_GROUP_ID or not chat:
        return
    try:
        title = escape_markdown(chat.title or "Unknown Group", version=2)
        channel = escape_markdown(str(channel), version=2)
        await client.send_message(
            LOG_GROUP_ID,
            f"⚙️ **Force Join Updated**\n\n"
            f"📛 Group: {title}\n"
            f"🆔 Group ID: `{chat.id}`\n"
            f"📢 Channel: `{channel}`",
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception:
        pass
