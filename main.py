from pyrogram import Client, filters

from config import API_ID, API_HASH, BOT_TOKEN
from plugins.start import start
from plugins.broadcast import broadcast
from plugins.broadcast import broadcast

app = Client(
    "forcejoinbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await start(client, message)

@app.on_message(filters.command("broadcast"))
async def broadcast_handler(client, message):
    await broadcast(client, message)

print("🚀 Bot starting...")

app.run()
