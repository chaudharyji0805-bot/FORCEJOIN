from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import users, channels, premium

async def inline_stats(client, callback):
    text = (
        "📊 **Bot Statistics**\n\n"
        f"👤 Users: {users.count_documents({})}\n"
        f"💎 Premium: {premium.count_documents({})}\n"
        f"📣 Channels: {channels.count_documents({})}"
    )
    await callback.message.edit(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="panel")]
        ])
    )
