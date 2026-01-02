from database import group_settings

async def list_channels(client, message):
    s = group_settings.find_one({"group_id": message.chat.id}) or {}
    channels = s.get("channels", [])

    if not channels:
        return await message.reply("ℹ️ No channels set for this group.")

    lines = []
    for i, ch in enumerate(channels, start=1):
        invite = ch.get("invite") or ""
        lines.append(f"{i}. @{ch['username']} {invite}")

    await message.reply("📌 **Channels for this group:**\n\n" + "\n".join(lines))
