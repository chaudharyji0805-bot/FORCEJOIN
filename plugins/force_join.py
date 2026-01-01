from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from database import group_settings, users
from collections import defaultdict
import time

# warning counter: (chat_id, user_id) -> count
WARN_COUNT = defaultdict(int)

# last warning message id: (chat_id, user_id) -> msg_id
FORCE_WARNINGS = {}

MAX_WARNINGS = 3


def valid_url(url: str) -> bool:
    return bool(url) and url.startswith("https://t.me/")


async def force_join_check(client, message):
    user = message.from_user
    chat = message.chat

    # safety checks
    if not user or chat.type not in ("group", "supergroup"):
        return True

    # store user globally
    users.update_one(
        {"user_id": user.id},
        {"$set": {"user_id": user.id}},
        upsert=True
    )

    # get group settings
    settings = group_settings.find_one({"group_id": chat.id})

    # if no force join set OR disabled → allow
    if not settings or not settings.get("enabled", True):
        return True

    channels = settings.get("channels", [])
    if not channels:
        return True

    not_joined = []

    # check all channels for this group
    for ch in channels:
        try:
            await client.get_chat_member(ch["username"], user.id)
        except UserNotParticipant:
            not_joined.append(ch)
        except Exception:
            # private channel / bot not member → skip
            continue

    # ❌ user NOT joined all channels
    if not_joined:
        # delete user's message
        try:
            await message.delete()
        except Exception:
            pass

        key = (chat.id, user.id)
        WARN_COUNT[key] += 1

        # auto mute after 3 warnings
        if WARN_COUNT[key] > MAX_WARNINGS:
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

        # delete old warning message
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

    # ✅ user joined all channels successfully
    key = (chat.id, user.id)

    # reset warning count
    WARN_COUNT.pop(key, None)

    # delete old warning message
    old_msg = FORCE_WARNINGS.get(key)
    if old_msg:
        try:
            await client.delete_messages(chat.id, old_msg)
        except Exception:
            pass
        FORCE_WARNINGS.pop(key, None)

    # unmute user if muted
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
