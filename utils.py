
import asyncio
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def __reply(message, bot_username, copied):
    msg_id = copied.id
    if copied.video:
        unique_idx = copied.video.file_unique_id
    elif copied.photo:
        unique_idx = copied.photo.file_unique_id
    elif copied.audio:
        unique_idx = copied.audio.file_unique_id
    elif copied.document:
        unique_idx = copied.document.file_unique_id
    elif copied.sticker:
        unique_idx = copied.sticker.file_unique_id
    elif copied.animation:
        unique_idx = copied.animation.file_unique_id
    elif copied.voice:
        unique_idx = copied.voice.file_unique_id
    elif copied.video_note:
        unique_idx = copied.video_note.file_unique_id
    else:
        await copied.delete()
        return

    Url = f"https://t.me/{bot_username}?start={unique_idx.lower()}-{str(msg_id)}"
    await message.reply_text(
        f"""
**Here is Your Sharing Link:**

`{Url}`
        """,
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Sharing Link",
                        url=Url
                    )
                ]
            ]
        )
    )
    await asyncio.sleep(0.5)
