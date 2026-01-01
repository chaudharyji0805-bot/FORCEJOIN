from config import OWNER_ID

async def notify_start(client, user):
    await client.send_message(
        OWNER_ID,
        f"👤 New User Started Bot\n\n"
        f"Name: {user.first_name}\n"
        f"ID: `{user.id}`"
    )


async def notify_group_add(client, chat):
    await client.send_message(
        OWNER_ID,
        f"➕ Bot Added to Group\n\n"
        f"Title: {chat.title}\n"
        f"ID: `{chat.id}`"
    )


async def notify_force_set(client, chat):
    await client.send_message(
        OWNER_ID,
        f"⚙️ Force Join Set\n\n"
        f"Group: {chat.title}\n"
        f"ID: `{chat.id}`"
    )
