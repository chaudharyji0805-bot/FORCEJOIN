from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from plugins.force_join import force_join_check
from plugins.start import start
from plugins.broadcast import broadcast, cancel_broadcast
from plugins.channels import add_channel, remove_channel
from plugins.force_join import force_join_check
app = Client(
    "forcejoinbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Group force join (AUTO)
@app.on_message(filters.group & filters.text)
async def group_force_join(client, message):
    await force_join_check(client, message)

# Start (private)
@app.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):
    await start(client, message)

# Admin commands
@app.on_message(filters.command("addchannel"))
async def add_channel_handler(client, message):
    await add_channel(client, message)

@app.on_message(filters.command("removechannel"))
async def remove_channel_handler(client, message):
    await remove_channel(client, message)

@app.on_message(filters.group & filters.text)
async def group_force_join(client, message):
    await force_join_check(client, message)


@app.on_callback_query(filters.regex("^recheck:"))
async def recheck_handler(client, callback):
    await callback.answer("Checking...")
    fake = callback.message
    fake.from_user = callback.from_user
    await force_join_check(client, fake)

    
# Broadcast
@app.on_message(filters.command("broadcast"))
async def broadcast_handler(client, message):
    await broadcast(client, message)

@app.on_callback_query(filters.regex("^cancel$"))
async def cancel_handler(client, callback):
    await cancel_broadcast(client, callback)

print("🚀 Bot starting...")
app.run()
