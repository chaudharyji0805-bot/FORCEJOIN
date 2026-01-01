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

👤 **User Info**
• Group me message bhejne se pehle
  required channels join karna zaroori ho sakta hai.
• "✅ I Joined" button dabakar dubara check kara sakte ho.

👮 **Admin Commands (Group me hi use kare)**
/addchannel @channel [invite_link]
➜ Is group ke liye force join channel add kare

/removechannel @channel
➜ Is group se force join channel remove kare

/listchannels
➜ Is group ke sab force join channels dekhe

/forceon
➜ Is group me force join ENABLE kare

/forceoff
➜ Is group me force join DISABLE kare

⚠️ **Rules**
• 3 warning ke baad auto mute
• Join karne ke baad auto unmute
"""


async def help_command(client, message):
    if message.chat.type == ChatType.PRIVATE:
        await message.reply(HELP_TEXT_PRIVATE)
    else:
        await message.reply(HELP_TEXT_GROUP)
