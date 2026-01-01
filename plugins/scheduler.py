import asyncio
from database import users

async def scheduled_broadcast(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /schedule 10 (minutes)")

    delay = int(message.command[1]) * 60
    reply = message.reply_to_message

    await message.reply("⏳ Broadcast scheduled")

    await asyncio.sleep(delay)

    for u in users.find({}):
        try:
            await reply.copy(u["user_id"])
        except:
            pass
