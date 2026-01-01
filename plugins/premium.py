from database import premium
from config import OWNER_ID

async def add_premium(client, message):
    if message.from_user.id != OWNER_ID:
        return

    user_id = int(message.command[1])
    premium.insert_one({"user_id": user_id})
    await message.reply("💎 Premium Added")

async def is_premium(user_id):
    return premium.find_one({"user_id": user_id}) is not None
