from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import channels


async def force_join_check(client, message):
    user_id = message.from_user.id

    not_joined = []

    for ch in channels.find({}):
        try:
            await client.get_chat_member(ch["username"], user_id)
        except UserNotParticipant:
            not_joined.append(ch)
        except Exception:
            not_joined.append(ch)

    if not_joined:
        buttons = []
        for ch in not_joined:
            url = ch.get("invite") or f"https://t.me/{ch['username']}"
            buttons.append(
                [InlineKeyboardButton(f"Join @{ch['username']}", url=url)]
            )

        await message.reply(
            "❌ **Pehle niche diye gaye channels join karo:**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return False

    return True
