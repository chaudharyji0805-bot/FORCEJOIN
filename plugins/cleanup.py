from database import group_settings

async def cleanup_groups(client):
    dialogs = [d.chat.id async for d in client.get_dialogs() if d.chat.type in ("group", "supergroup")]

    for g in group_settings.find({}):
        if g["group_id"] not in dialogs:
            group_settings.delete_one({"group_id": g["group_id"]})
