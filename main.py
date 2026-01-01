# ─────────────────────────────
# IMPORTS
# ─────────────────────────────
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN

# core logic
from plugins.force_join import force_join_check
from plugins.start import start
from plugins.broadcast import broadcast, cancel_broadcast

# group management
from plugins.channels import add_channel, remove_channel
from plugins.settings import enable_force, disable_force
from plugins.listchannels import list_channels

# help & inline UI
from plugins.help import help_command, HELP_TEXT_PRIVATE, close_button

# logging & notifications
from plugins.notify import (
    notify_group_add,
    notify_user_start,
    notify_force_set,
    notify_bot_start
)

# stats & reports
from plugins.stats_tracker import init_stats
from plugins.daily_report import daily_report
from plugins.group_stats import group_stats_cmd


# ─────────────────────────────
# APP INITIALIZATION
# ─────────────────────────────
app = Client(
    "forcejoinbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# ─────────────────────────────
# STATS (PER GROUP)
# ─────────────────────────────
@app.on_message(filters.group & filters.command("stats"))
async def stats_handler(client, message):
    await group_stats_cmd(client, message)


# ─────────────────────────────
# HELP COMMAND
# ─────────────────────────────
@app.on_message(filters.command("help"))
async def help_handler(client, message):
    await help_command(client, message)


# ─────────────────────────────
# GROUP FORCE JOIN (AUTO CHECK)
# commands excluded so /help etc. not deleted
# ─────────────────────────────
@app.on_message(filters.group & filters.text & ~filters.regex(r"^/"))
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
# ADMIN COMMANDS (GROUP ONLY)
# ─────────────────────────────
@app.on_message(filters.group & filters.command("addchannel"))
async def add_channel_handler(client, message):
    await add_channel(client, message)
    if len(message.command) >= 2:
        await notify_force_set(client, message.chat, message.command[1])


@app.on_message(filters.group & filters.command("removechannel"))
async def remove_channel_handler(client, message):
    await remove_channel(client, message)


@app.on_message(filters.group & filters.command("forceon"))
async def force_on_handler(client, message):
    await enable_force(client, message)


@app.on_message(filters.group & filters.command("forceoff"))
async def force_off_handler(client, message):
    await disable_force(client, message)


@app.on_message(filters.group & filters.command("listchannels"))
async def list_channels_handler(client, message):
    await list_channels(client, message)


# ─────────────────────────────
# BOT ADDED TO GROUP
# ─────────────────────────────
@app.on_message(filters.new_chat_members)
async def bot_added_handler(client, message):
    for m in message.new_chat_members:
        if m.is_self:
            await notify_group_add(client, message.chat)


# ─────────────────────────────
# INLINE CALLBACKS
# ─────────────────────────────
@app.on_callback_query(filters.regex("^recheck:"))
async def recheck_handler(client, callback):
    await callback.answer("🔍 Checking...")
    fake_message = callback.message
    fake_message.from_user = callback.from_user
    await force_join_check(client, fake_message)


@app.on_callback_query(filters.regex("^help$"))
async def help_callback(client, callback):
    await callback.answer()
    await callback.message.edit_text(
        HELP_TEXT_PRIVATE,
        reply_markup=close_button()
    )


@app.on_callback_query(filters.regex("^about$"))
async def about_callback(client, callback):
    await callback.answer()
    await callback.message.edit_text(
        "ℹ️ **About Bot**\n\n"
        "Advanced Force Join Management Bot\n"
        "• Per-group force join\n"
        "• Auto mute after warnings\n"
        "• Inline recheck system\n"
        "• Log group notifications",
        reply_markup=close_button()
    )


@app.on_callback_query(filters.regex("^close$"))
async def close_callback(client, callback):
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass


# ─────────────────────────────
# BROADCAST
# ─────────────────────────────
@app.on_message(filters.command("broadcast"))
async def broadcast_handler(client, message):
    await broadcast(client, message)


@app.on_callback_query(filters.regex("^cancel$"))
async def cancel_handler(client, callback):
    await cancel_broadcast(client, callback)


# ─────────────────────────────
# STARTUP SEQUENCE
# ─────────────────────────────
print("🚀 Bot starting...")

init_stats()                          # init DB stats
app.start()                           # start bot
app.loop.create_task(daily_report(app))  # daily uptime report
app.loop.run_until_complete(
    notify_bot_start(app)
)                                    # log group start message
app.idle()                            # keep bot alive
app.stop()                            # graceful shutdown
