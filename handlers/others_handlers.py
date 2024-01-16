from aiogram import Router, F

from aiogram.types import Message, ContentType

from lexicon.lexicon import LEXICON_ENG

router: Router = Router()

@router.message(F.content_type.in_(['audio', "sticker", "photo", "voice", "video", "animation"]))
async def echo_message(message: Message):
    await message.reply(
        text=LEXICON_ENG["others"]
    )