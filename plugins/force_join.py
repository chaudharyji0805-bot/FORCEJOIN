from collections import defaultdict
import time

from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions

from database import group_settings, users, group_stats
from plugins.stats_tracker import inc_message, inc_force_action

WARN_COUNT = defaultdict(int)
FORCE_WARNINGS = {}
MAX_WARNINGS = 3


def valid_url(url: str) -> bool:
    return bool(url) and url.startswith("https://t.me/")


async def force_join_check(client, message):
    user = message.from_user
    chat = message.chat

    if not user or not chat or chat.type not in ("group", "supergroup"):
        return True

    # global stats
    try:
        await inc_message()
    except Exception:
        pass

    # group stats
    try:
        await group_stats.update_one(
            {"group_id": chat.id},
            {"$inc": {"messages": 1}},
            upsert=True
        )
    except Exception:
        pass

    # save user
    try:
        await users.update_one(
            {"user_id": user.id},
            {"$set": {"user_id": user.id}},
            upsert=True
        )
    except Exception:
        pass

    # get settings
    settings = await group_settings.find_one({"group_id": chat.id})
    if not settings:
        return True

    channels = settings.get("channels", [])
    if not channels:
        return True

    not_joined = []

    for ch in channels:
        try:
            await client.get_chat_member(ch["username"], user.id)
        except UserNotParticipant:
            not_joined.append(ch)
        except Exception:
            continue

    # user joined all channels
    if not not_joined:
        key = (chat.id, user.id)
        WARN_COUNT.pop(key, None)

        old = FORCE_WARNINGS.pop(key, None)
        if old:
            try:
                await client.delete_messages(chat.id, old)
            except Exception:
                pass
        return True

    # user not joined → enforce
    try:
        await message.delete()
    except Exception:
        pass

    key = (chat.id, user.id)
    WARN_COUNT[key] += 1

    try:
        await inc_force_action()
        await group_stats.update_one(
            {"group_id": chat.id},
            {"$inc": {"actions": 1}},
            upsert=True
        )
    except Exception:
        pass

    # mute after 3 warnings
    if WARN_COUNT[key] >= MAX_WARNINGS:
        try:
            await client.restrict_chat_member(
                chat.id,
                user.id,
                ChatPermissions(can_send_messages=False),
                until_date=int(time.time()) + 3600
            )
        except Exception:
            pass
        return False

    # build buttons
    buttons = []
    for ch in not_joined:
        invite = ch.get("invite")
        url = invite if valid_url(invite) else f"https://t.me/{ch['username']}"
        if valid_url(url):
            buttons.append(
                [InlineKeyboardButton(f"Join @{ch['username']}", url=url)]
            )

    buttons.append(
        [InlineKeyboardButton("✅ I Joined", callback_data=f"recheck:{chat.id}")]
    )

    text = (
        f"🚫 **Force Join Required**\n\n"
        f"👤 {user.mention}\n"
        f"⚠️ Warning: {WARN_COUNT[key]}/{MAX_WARNINGS}\n\n"
        f"➡️ Channels join karo, phir **I Joined** dabao."
    )

    old = FORCE_WARNINGS.get(key)
    if old:
        try:
            await client.delete_messages(chat.id, old)
        except Exception:
            pass

    warn = await client.send_message(
        chat.id,
        text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    FORCE_WARNINGS[key] = warn.id

    return False
