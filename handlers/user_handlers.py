from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types.message_entity import MessageEntity
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON_ENG, LEXICON_COMMANDS

from handlers.callback_queries import ChangeLangFSM

from redis import Redis

import json

from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.answers import answer_keyboard

from external_services.supported_languages import SUPPORTED_LANGUAGES
from external_services.translate import get_translation

from db.queries import get_user, update_lang_code
from db.models import TelegramUser

from keyboards.choose_lang import choose_lang_kb


# init the router
router: Router = Router()

# handler for /start command
@router.message(CommandStart())
async def start_command(message: Message, async_session: AsyncSession):
    
    if await get_user(async_session, message.from_user.id) is None:
        await message.answer(text=LEXICON_ENG[message.text]) # message.text == /start
        await message.answer(text=LEXICON_ENG["nat_lang"] + f"<b>{SUPPORTED_LANGUAGES.get(message.from_user.language_code,'en').title()}</b>?", 
                         reply_markup=answer_keyboard())
    else:
        await message.reply(
                text=LEXICON_ENG["has_account"]
            )


# handler for /profile command
@router.message(Command(commands="profile"))
async def profile_command(message: Message, async_session: AsyncSession):
    user: TelegramUser | None = await get_user(async_session, message.from_user.id)

    if user is None:
        await message.reply(
            text=LEXICON_ENG["without_profile"]
        )
    else:
        await message.answer(
            text=f"""
🔶<b>{message.from_user.first_name}'s</b> profile🔶:
Name: {message.from_user.first_name}
Telegram ID: {user.tg_user}
Native language: {SUPPORTED_LANGUAGES[user.lang_code].lower()}
Target language: {SUPPORTED_LANGUAGES[user.targ_lang_code].lower()}
""",
            parse_mode="HTML"
    )


# handler for /help command
@router.message(Command(commands="help"))
async def help_command(message: Message):
    await message.answer(
        text=LEXICON_ENG["/help"]
    )


# handler for /change_native command
@router.message(Command(commands="change_native"))
async def change_native_lang_command(message: Message, async_session: AsyncSession, state: FSMContext):
    
    if await get_user(async_session, message.from_user.id) is None:
        await message.answer(
            text=LEXICON_ENG["without_profile"],
            show_alert=True
        )
        await message.answer(
            text="Write \help"
        )
    else:
        await message.answer(
            text = LEXICON_ENG["choose_nat"],
            reply_markup = choose_lang_kb()
        )
        await state.set_state(ChangeLangFSM.change_native)


# handler for /change_target command
@router.message(Command(commands="change_target"))
async def change_target_lang_command(message: Message, async_session: AsyncSession, state: FSMContext):
    
    if await get_user(async_session, message.from_user.id) is None:
        await message.answer(
            text=LEXICON_ENG["without_profile"],
            show_alert=True
        )
        await message.answer(
            text="Write \help"
        )
    else:
        await message.answer(
            text = LEXICON_ENG["choose_targ"],
            reply_markup = choose_lang_kb()
        )
        await state.set_state(ChangeLangFSM.change_target)


@router.message(F.content_type == ContentType.TEXT, ~F.text.in_(LEXICON_COMMANDS.keys()))
async def send_translated_text(message: Message, async_session: AsyncSession):
   
    user: TelegramUser | None = await get_user(async_session, message.from_user.id)

    if user is None:
        await message.answer(
            text=LEXICON_ENG['without_profile']
        )
    native_lang: str = user.lang_code

    targ_lang: str = user.targ_lang_code

    if native_lang == targ_lang:
        await message.reply(
            text=LEXICON_ENG["same_targ_native"]
        )
    else:
        await message.reply(
            text = await get_translation(message.text, native_lang, targ_lang)
        )


    