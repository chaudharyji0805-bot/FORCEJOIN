from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from collections import defaultdict
import time

from database import group_settings, users, group_stats
from plugins.stats_tracker import inc_message, inc_force_action


# ─────────────────────────────
# WARNINGS TRACKING
# ─────────────────────────────
WARN_COUNT = defaultdict(int)        # (chat_id, user_id) -> warnings
FORCE_WARNINGS = {}                  # (chat_id, user_id) -> message_id

MAX_WARNINGS = 3


# ─────────────────────────────
# HELPERS
# ─────────────────────────────
def valid_url(url: str) -> bool:
    return bool(url) and url.startswith("https://t.me/")


# ─────────────────────────────
# MAIN FORCE JOIN CHECK
# ─────────────────────────────
async def force_join_check(client, message):
    user = message.from_user
    chat = message.chat

    # basic safety
    if not user or chat.type not in ("group", "supergroup"):
        return True

    # global stats
    inc_message()

    # per-group stats
    group_stats.update_one(
        {"group_id": chat.id},
        {"$inc": {"messages": 1}},
        upsert=True
    )

    # store user globally (for broadcast)
    users.update_one(
        {"user_id": user.id},
        {"$set": {"user_id": user.id}},
        upsert=True
    )

    # load group force join settings
    settings = group_settings.find_one({"group_id": chat.id})

    if not settings or not settings.get("enabled", True):
        return True

    channels = settings.get("channels", [])
    if not channels:
        return True

    not_joined = []

    # check membership
    for ch in channels:
        try:
            await client.get_chat_member(ch["username"], user.id)
        except UserNotParticipant:
            not_joined.append(ch)
        except Exception:
            # private channel / bot not admin / inaccessible
            continue

    # ─────────────────────────────
    # USER NOT JOINED REQUIRED CHANNELS
    # ─────────────────────────────
    if not_joined:
        # delete user's message
        try:
            await message.delete()
        except Exception:
            pass

        key = (chat.id, user.id)
        WARN_COUNT[key] += 1

        # count force action
        inc_force_action()
        group_stats.update_one(
            {"group_id": chat.id},
            {"$inc": {"actions": 1}},
            upsert=True
        )

        # auto mute after MAX_WARNINGS
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

        # build join buttons
        buttons = []
        for ch in not_joined:
            invite = ch.get("invite")
            url = invite if valid_url(invite) else f"https://t.me/{ch['username']}"
            if valid_url(url):
                buttons.append(
                    [InlineKeyboardButton(f"Join @{ch['username']}", url=url)]
                )

        # recheck button
        buttons.append(
            [InlineKeyboardButton("✅ I Joined", callback_data=f"recheck:{chat.id}")]
        )

        text = (
            f"🚫 **Force Join Required**\n\n"
            f"👤 {user.mention}\n"
            f"⚠️ Warning: {WARN_COUNT[key]}/{MAX_WARNINGS}\n\n"
            f"➡️ Sab channels join karo, phir **I Joined** dabao."
        )

        # delete previous warning message
        old_msg = FORCE_WARNINGS.get(key)
        if old_msg:
            try:
                await client.delete_messages(chat.id, old_msg)
            except Exception:
                pass

        warn = await client.send_message(
            chat.id,
            text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        FORCE_WARNINGS[key] = warn.id
        return False

    # ─────────────────────────────
    # USER JOINED ALL CHANNELS
    # ─────────────────────────────
    key = (chat.id, user.id)

    WARN_COUNT.pop(key, None)

    old_msg = FORCE_WARNINGS.pop(key, None)
    if old_msg:
        try:
            await client.delete_messages(chat.id, old_msg)
        except Exception:
            pass

    # unmute user (if muted)
    try:
        await client.restrict_chat_member(
            chat.id,
            user.id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
    except Exception:
        pass

    return True
