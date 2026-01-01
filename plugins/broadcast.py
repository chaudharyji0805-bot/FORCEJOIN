import asyncio
from database import users
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BROADCAST_RUNNING = False


async def broadcast(client, message):
    global BROADCAST_RUNNING

    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast")

    BROADCAST_RUNNING = True

    msg = await message.reply(
        "📢 Broadcasting...",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("❌ Cancel Broadcast", callback_data="cancel")]]
        )
    )

    total = users.count_documents({})
    sent = 0

    for u in users.find({}):
        if not BROADCAST_RUNNING:
            await msg.edit("❌ Broadcast Cancelled")
            return

        try:
            await message.reply_to_message.copy(u["user_id"])
            sent += 1
        except Exception:
            pass

        if total > 0 and sent % 10 == 0:
            percent = int((sent / total) * 100)
            await msg.edit(
                f"📢 Broadcasting...\nProgress: {percent}%",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("❌ Cancel Broadcast", callback_data="cancel")]]
                )
            )

        await asyncio.sleep(0.05)

    await msg.edit(f"✅ Broadcast Done\nSent: {sent}")


async def cancel_broadcast(client, callback):
    global BROADCAST_RUNNING
    BROADCAST_RUNNING = False
    await callback.answer("Broadcast cancelled", show_alert=True)
