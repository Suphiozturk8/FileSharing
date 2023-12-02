
from pyrogram import Client, filters
from pyrogram.types import Message

from config import APP_ID, API_HASH, BOT_TOKEN, TRACK_CHANNEL, OWNER_ID, START_MESSAGE, HELP_MESSAGE

from utils import __reply

bot = Client("FileSharing", api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

with bot:
    bot_username = bot.get_me().username
    print("Bot started!")
    bot.send_message(int(OWNER_ID), "Bot started!")


@bot.on_message(filters.command("help") & filters.private)
async def _help(bot, message: Message):
    await message.reply_text(
        HELP_MESSAGE.format(OWNER_ID),
        quote=True
    )


@bot.on_message(filters.command("start") & filters.private)
async def _startfile(bot, message: Message):
    if message.text == "/start":
        return await message.reply_text(
            START_MESSAGE.format(message.from_user.first_name),
            quote=True
        )

    if len(message.command) != 2:
        return
    code = message.command[1]
    if "-" in code:
        msg_id = code.split("-")[-1]
        unique_id = "-".join(code.split("-")[0:-1])

        if not msg_id.isdigit():
            return
        try:
            check_media_group = await bot.get_media_group(TRACK_CHANNEL, int(msg_id))
            check = check_media_group[0]
        except Exception:
            check = await bot.get_messages(TRACK_CHANNEL, int(msg_id))

        if check.empty:
            return await message.reply_text(
                "**Error:** `[Message does not exist]`\n**/help for more details...**"
            )

        if check.video:
            unique_idx = check.video.file_unique_id
        elif check.photo:
            unique_idx = check.photo.file_unique_id
        elif check.audio:
            unique_idx = check.audio.file_unique_id
        elif check.document:
            unique_idx = check.document.file_unique_id
        elif check.sticker:
            unique_idx = check.sticker.file_unique_id
        elif check.animation:
            unique_idx = check.animation.file_unique_id
        elif check.voice:
            unique_idx = check.voice.file_unique_id
        elif check.video_note:
            unique_idx = check.video_note.file_unique_id
        if unique_id != unique_idx.lower():
            return
        try:
            await bot.copy_media_group(message.from_user.id, TRACK_CHANNEL, int(msg_id))
        except Exception:
            await check.copy(message.from_user.id)
    else:
        return


media_group_id = 0
@bot.on_message(
    filters.media &
    filters.private)
async def _main_grop(bot, message: Message):
    global media_group_id

    if message.media_group_id:
        if int(media_group_id) != int(message.media_group_id):
            media_group_id = message.media_group_id
            copied = (await bot.copy_media_group(TRACK_CHANNEL, message.from_user.id, message.id))[0]
            await __reply(message, bot_username, copied)
        else:
            return
    else:
        copied = await message.copy(TRACK_CHANNEL)
        await __reply(message, bot_username, copied)


bot.run()
