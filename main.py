from pyrogram import Client, filters
from config import *
from plugins.start import start
from plugins.broadcast import broadcast, cancel_broadcast
from plugins.stats import inline_stats
from plugins.admin_panel import admin_panel
from plugins.scheduler import scheduled_broadcast

app = Client(
    "forcejoinbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

app.on_message(filters.command("start"))(start)
app.on_message(filters.command("panel"))(admin_panel)
app.on_message(filters.command("broadcast"))(broadcast)
app.on_message(filters.command("schedule"))(scheduled_broadcast)

app.on_callback_query(filters.regex("stats"))(inline_stats)
app.on_callback_query(filters.regex("cancel"))(cancel_broadcast)

app.run()
