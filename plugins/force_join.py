from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from database import channels
from collections import defaultdict
import time

# track warnings per user per chat
WARN_COUNT = defaultdict(int)

# store last warning message id
FORCE_WARNINGS = {}

MAX_WARNINGS = 3


def valid_url(url: str) -> bool:
    return bool(url) and url.startswith("https://t.me/")


async def force_join_check(client, message):
    user = message.from_user
    chat = message.chat

    if not user or chat.type not in ("group", "supergroup"):
        return True

    not_joined = []

    for ch in channels.find({}):
        try:
            await client.get_chat_member(ch["username"], user.id)
        except UserNotParticipant:
            not_joined.append(ch)
        except Exception:
            # private channel / bot not member → skip check
            continue

    # ❌ NOT JOINED CASE
    if not_joined:
        # delete user message
        try:
            await message.delete()
        except Exception:
            pass

        # increase warning count
        key = (chat.id, user.id)
        WARN_COUNT[key] += 1

        # AUTO MUTE after 3 warnings
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

        # build buttons
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
            f"👤 {user.mention}\n\n"
            f"⚠️ Warning: {WARN_COUNT[key]}/{MAX_WARNINGS}\n\n"
            f"➡️ Sab channels join karo, phir **I Joined** dabao."
        )

        # delete old warning (if exists)
        old = FORCE_WARNINGS.get(key)
        if old:
            try:
                await client.delete_messages(chat.id, old)
            except Exception:
                pass

        warn_msg = await client.send_message(
            chat.id,
            text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        FORCE_WARNINGS[key] = warn_msg.id
        return False

    # ✅ JOINED SUCCESS
    key = (chat.id, user.id)

    # reset warnings
    WARN_COUNT.pop(key, None)

    # delete old warning
    old = FORCE_WARNINGS.get(key)
    if old:
        try:
            await client.delete_messages(chat.id, old)
        except Exception:
            pass
        FORCE_WARNINGS.pop(key, None)

    # unmute if muted
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
