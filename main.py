from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from plugins.start import start
from plugins.broadcast import broadcast, cancel_broadcast
from plugins.channels import add_channel, remove_channel

app = Client(
    "forcejoinbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# /start command
@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await start(client, message)

# /broadcast command (admin use)
@app.on_message(filters.command("broadcast"))
async def broadcast_handler(client, message):
    await broadcast(client, message)

# Cancel broadcast button
@app.on_callback_query(filters.regex("^cancel$"))
async def cancel_handler(client, callback):
    await cancel_broadcast(client, callback)
@app.on_message(filters.command("addchannel"))
async def add_channel_handler(client, message):
    await add_channel(client, message)


@app.on_message(filters.command("removechannel"))
async def remove_channel_handler(client, message):
    await remove_channel(client, message)

print("🚀 Bot starting...")
app.run()
