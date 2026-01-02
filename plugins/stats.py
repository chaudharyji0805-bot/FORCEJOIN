from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import users, channels, premium


async def inline_stats(client, callback):
    try:
        total_users = await users.count_documents({})
    except Exception:
        total_users = 0

    try:
        total_premium = await premium.count_documents({})
    except Exception:
        total_premium = 0

    try:
        total_channels = await channels.count_documents({})
    except Exception:
        total_channels = 0

    text = (
        "📊 **Bot Statistics**\n\n"
        f"👤 Users: {total_users}\n"
        f"💎 Premium: {total_premium}\n"
        f"📣 Channels: {total_channels}"
    )

    try:
        await callback.message.edit(
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Back", callback_data="panel")]]
            )
        )
    except Exception:
        pass
