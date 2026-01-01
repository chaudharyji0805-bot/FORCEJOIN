from database import users

async def start(client, message):
    user = message.from_user

    # save user in database (if not exists)
    if not users.find_one({"user_id": user.id}):
        users.insert_one({"user_id": user.id})

    await message.reply(
        "✅ Welcome!\n\n"
        "Bot successfully started."
    )
