from plugins.help import help_command
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN

# core features
from plugins.force_join import force_join_check
from plugins.start import start
from plugins.broadcast import broadcast, cancel_broadcast

# group force-join management
from plugins.channels import add_channel, remove_channel
from plugins.settings import enable_force, disable_force
from plugins.listchannels import list_channels

# logging
from plugins.notify import notify_group_add, notify_user_start, notify_force_set

app = Client(
    "forcejoinbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


@app.on_message(filters.command("help"))
async def help_handler(client, message):
    await help_command(client, message)

# ─────────────────────────────
# GROUP FORCE JOIN (AUTO CHECK)
# ─────────────────────────────
@app.on_message(filters.group & filters.text)
async def group_force_join(client, message):
    await force_join_check(client, message)

# ─────────────────────────────
# PRIVATE START
# ─────────────────────────────
@app.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):
    await notify_user_start(client, message.from_user)
    await start(client, message)

# ─────────────────────────────
# ADMIN: ADD / REMOVE CHANNEL
# ─────────────────────────────
@app.on_message(filters.command("addchannel") & filters.group)
async def add_channel_handler(client, message):
    await add_channel(client, message)
    if len(message.command) >= 2:
        await notify_force_set(client, message.chat, message.command[1])

@app.on_message(filters.command("removechannel") & filters.group)
async def remove_channel_handler(client, message):
    await remove_channel(client, message)

# ─────────────────────────────
# FORCE JOIN ON / OFF
# ─────────────────────────────
@app.on_message(filters.command("forceon") & filters.group)
async def force_on_handler(client, message):
    await enable_force(client, message)

@app.on_message(filters.command("forceoff") & filters.group)
async def force_off_handler(client, message):
    await disable_force(client, message)

# ─────────────────────────────
# LIST CHANNELS (CURRENT GROUP)
# ─────────────────────────────
@app.on_message(filters.command("listchannels") & filters.group)
async def list_channels_handler(client, message):
    await list_channels(client, message)

# ─────────────────────────────
# BOT ADDED TO GROUP → LOG
# ─────────────────────────────
@app.on_message(filters.new_chat_members)
async def bot_added_handler(client, message):
    for m in message.new_chat_members:
        if m.is_self:
            await notify_group_add(client, message.chat)

# ─────────────────────────────
# FORCE JOIN RECHECK BUTTON
# ─────────────────────────────
@app.on_callback_query(filters.regex("^recheck:"))
async def recheck_handler(client, callback):
    await callback.answer("🔍 Checking...")
    fake = callback.message
    fake.from_user = callback.from_user
    await force_join_check(client, fake)

# ─────────────────────────────
# BROADCAST
# ─────────────────────────────
@app.on_message(filters.command("broadcast"))
async def broadcast_handler(client, message):
    await broadcast(client, message)

@app.on_callback_query(filters.regex("^cancel$"))
async def cancel_handler(client, callback):
    await cancel_broadcast(client, callback)

print("🚀 Bot starting...")
app.run()
