from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import channels

# Store last force join message id per user (memory-based)
FORCE_JOIN_MESSAGES = {}


async def force_join_check(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    not_joined = []

    for ch in channels.find({}):
        try:
            await client.get_chat_member(ch["username"], user_id)
        except Exception:
            not_joined.append(ch)

    # If user has NOT joined all channels
    if not_joined:
        buttons = []
        for ch in not_joined:
            url = ch.get("invite") or f"https://t.me/{ch['username']}"
            buttons.append(
                [InlineKeyboardButton(f"Join @{ch['username']}", url=url)]
            )

        msg = await message.reply(
            "❌ **Pehle niche diye gaye channels join karo:**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        # Save force join message id
        FORCE_JOIN_MESSAGES[user_id] = msg.id
        return False

    # ✅ User joined all channels → delete old force join message
    old_msg_id = FORCE_JOIN_MESSAGES.get(user_id)
    if old_msg_id:
        try:
            await client.delete_messages(chat_id, old_msg_id)
        except Exception:
            pass
        FORCE_JOIN_MESSAGES.pop(user_id, None)

    return True
