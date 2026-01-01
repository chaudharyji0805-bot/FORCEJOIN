from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import channels

# Store last warning message per user per chat
FORCE_WARNINGS = {}


async def force_join_check(client, message):
    user = message.from_user
    chat = message.chat

    if not user:
        return True

    not_joined = []

    # check all force join channels
    for ch in channels.find({}):
        try:
            await client.get_chat_member(ch["username"], user.id)
        except Exception:
            not_joined.append(ch)

    # ❌ user has NOT joined required channels
    if not_joined:
        # delete user's message (GROUP MODE)
        try:
            await message.delete()
        except Exception:
            pass

        buttons = []
        for ch in not_joined:
            url = ch.get("invite") or f"https://t.me/{ch['username']}"
            buttons.append(
                [InlineKeyboardButton(f"Join @{ch['username']}", url=url)]
            )

        warn_text = (
            f"🚫 **Access Denied**\n\n"
            f"👤 {user.mention}\n\n"
            f"➡️ Pehle niche diye gaye **ALL channels** join karo, "
            f"phir group me message bhejo."
        )

        warn_msg = await client.send_message(
            chat.id,
            warn_text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        # save warning msg id
        FORCE_WARNINGS[(chat.id, user.id)] = warn_msg.id
        return False

    # ✅ user joined all channels → delete old warning
    old_warn = FORCE_WARNINGS.get((chat.id, user.id))
    if old_warn:
        try:
            await client.delete_messages(chat.id, old_warn)
        except Exception:
            pass
        FORCE_WARNINGS.pop((chat.id, user.id), None)

    return True
