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

# help
from plugins.help import help_command

# logging (log group)
from plugins.notify import notify_group_add, notify_user_start, notify_force_set


app = Client(
    "forcejoinbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ─────────────────────────────
# HELP (PRIVATE + GROUP)
# ─────────────────────────────
@app.on_message(filters.command("help"))
async def help_handler(client, message):
    await help_command(client, message)

# ─────────────────────────────
# GROUP FORCE JOIN (AUTO CHECK)
# ─────────────────────────────
# ⚠️ commands excluded so /help etc. are not deleted
@app.on_message(filters.group & filters.text & ~filters.command)
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
# ADMIN: ADD / REMOVE CHANNEL (GROUP ONLY)
# ─────────────────────────────
@app.on_message(filters.group & filters.command("addchannel"))
async def add_channel_handler(client, message):
    await add_channel(client, message)
    if len(message.command) >= 2:
        await notify_force_set(client, message.chat, message.command[1])

@app.on_message(filters.group & filters.command("removechannel"))
async def remove_channel_handler(client, message):
    await remove_channel(client, message)

# ─────────────────────────────
# FORCE JOIN ON / OFF (PER GROUP)
# ─────────────────────────────
@app.on_message(filters.group & filters.command("forceon"))
async def force_on_handler(client, message):
    await enable_force(client, message)

@app.on_message(filters.group & filters.command("forceoff"))
async def force_off_handler(client, message):
    await disable_force(client, messag_
