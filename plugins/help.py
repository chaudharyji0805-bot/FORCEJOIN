from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType


HELP_TEXT_PRIVATE = """
🤖 **Force Join Bot – Help**

👤 **User Commands**
/start – Bot start karo
/help – Ye help message

ℹ️ Agar bot kisi group me laga hai to
group ke rules follow karna zaroori hai.
"""

HELP_TEXT_GROUP = """
🤖 **Force Join Bot – Help (Group)**

👤 **Users**
• Message bhejne se pehle required channels join karna zaroori ho sakta hai
• "✅ I Joined" button se dubara check kar sakte ho

👮 **Admins (Group me hi use kare)**
/addchannel @channel [invite]
/removechannel @channel
/listchannels
/forceon
/forceoff

⚠️ Rules:
• 3 warning → auto mute
• Join ke baad auto unmute
"""


def start_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📖 Help", callback_data="help"),
                InlineKeyboardButton("ℹ️ About", callback_data="about")
            ]
        ]
    )


def close_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("❌ Close", callback_data="close")]]
    )


async def help_command(client, message):
    if message.chat.type == ChatType.PRIVATE:
        await message.reply(HELP_TEXT_PRIVATE, reply_markup=close_button())
    else:
        await message.reply(HELP_TEXT_GROUP, reply_markup=close_button())
