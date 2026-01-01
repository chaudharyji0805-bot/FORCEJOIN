from plugins.help import start_buttons
from database import users


async def start(client, message):
    user = message.from_user

    users.update_one(
        {"user_id": user.id},
        {"$set": {"user_id": user.id}},
        upsert=True
    )

    await message.reply(
        f"👋 **Welcome {user.first_name}!**\n\n"
        f"Is bot ka use groups me force join manage karne ke liye hota hai.\n\n"
        f"Neeche buttons se help dekho 👇",
        reply_markup=start_buttons()
    )
