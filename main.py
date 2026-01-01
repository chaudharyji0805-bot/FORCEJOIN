import os


from pyrogram import Client, filters
from config import *
from database import users
from plugins.start import start
from plugins.broadcast import broadcast, cancel_broadcast
from plugins.stats import inline_stats
from plugins.admin_panel import admin_panel
from plugins.scheduler import scheduled_broadcast

app = Client(
    "forcejoinbot",
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")
OWNER_ID = int(os.environ.get("OWNER_ID", 0))

)

app.on_message(filters.command("start"))(start)
app.on_message(filters.command("panel"))(admin_panel)
app.on_message(filters.command("broadcast"))(broadcast)
app.on_message(filters.command("schedule"))(scheduled_broadcast)

app.on_callback_query(filters.regex("stats"))(inline_stats)
app.on_callback_query(filters.regex("cancel"))(cancel_broadcast)

app.run()
