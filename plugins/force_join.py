from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from database import group_channels, users
from collections import defaultdict
from database import group_settings
import time

WARN_COUNT = defaultdict(int)
FORCE_WARNINGS = {}
MAX_WARNINGS = 3


def valid_url(url):
    return bool(url) and url.startswith("https://t.me/")


async def force_join_check(client, message):
    user = message.from_user
    chat = message.chat

    if not user or chat.type not in ("group", "supergroup"):
        return True

    # store user globally
    users.update_one(
        {"user_id": user.id},
        {"$set": {"user_id": user.id}},
        upsert=True
    )

    config = group_channels.find_one({"group_id": chat.id})
    if not config or not config.get("channels"):
        return True  # no force join for this group

    not_joined = []

    for ch in config["channels"]:
        try:
            await client.get_chat_member(ch["username"], user.id)
        except UserNotParticipant:
            not_joined.append(ch)
        except Exception:
            continue

    if not_joined:
        try:
            await message.delete()
        except Exception:
            pass

        key = (chat.id, user.id)
        WARN_COUNT[key] += 1

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

        buttons = []
        for ch in not_joined:
            url = ch.get("invite") if valid_url(ch.get("invite")) else f"https://t.me/{ch['username']}"
            if valid_url(url):
                buttons.append([InlineKeyboardButton(f"Join @{ch['username']}", url=url)])

        buttons.append(
            [InlineKeyboardButton("✅ I Joined", callback_data=f"recheck:{chat.id}")]
        )

        text = (
            f"🚫 **Force Join Required**\n\n"
            f"👤 {user.mention}\n"
            f"⚠️ Warning: {WARN_COUNT[key]}/{MAX_WARNINGS}"
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

    # success
    key = (chat.id, user.id)
    WARN_COUNT.pop(key, None)

    old = FORCE_WARNINGS.get(key)
    if old:
        try:
            await client.delete_messages(chat.id, old)
        except Exception:
            pass
        FORCE_WARNINGS.pop(key, None)

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
settings = group_settings.find_one({"group_id": chat.id})
if not settings or not settings.get("enabled", True):
    return True
