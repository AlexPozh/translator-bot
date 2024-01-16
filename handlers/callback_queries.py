from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, default_state, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import StateFilter

from redis import Redis

from lexicon.lexicon import LEXICON_ENG

from keyboards.choose_lang import choose_lang_kb

from sqlalchemy.ext.asyncio import AsyncSession

from db.queries import insert_user, get_user, update_lang_code

from external_services.supported_languages import SUPPORTED_LANGUAGES

import json



# init storage for FSM
storage: MemoryStorage = MemoryStorage()


# creating the class ChooseLangFSM to work with FSM states
class ChooseLangFSM(StatesGroup):
    # these states use for register a user
    choose_native = State()
    choose_target = State()
    

class ChangeLangFSM(StatesGroup):
    # these states use for changing user's languages
    change_target = State()
    change_native = State()

router: Router = Router()


# callbacks for answers. Callbacks 'yes' and 'no'
@router.callback_query(F.data == "answer_yes", StateFilter(default_state))
async def choose_targ_lang(callback: CallbackQuery, state: FSMContext, async_session: AsyncSession):
    # add new user to db
    print(await get_user(async_session, callback.from_user.id))
    if await get_user(async_session, callback.from_user.id) is None:
        await insert_user(async_session, callback.from_user.id, callback.message.from_user.language_code)

    await callback.message.edit_text(
        text = LEXICON_ENG["choose_targ"],
        reply_markup = choose_lang_kb()
    )

    # if bot dected the native lang right, we will set the "state" to get target language
    await state.set_state(ChooseLangFSM.choose_target)

@router.callback_query(F.data == "answer_no", StateFilter(default_state))
async def choose_native_lang(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text = LEXICON_ENG["choose_nat"],
        reply_markup = choose_lang_kb()
    )

    # if bot dected the native lang NOT right, we will set the "state" to get native language
    await state.set_state(ChooseLangFSM.choose_native)

#-------------------------------------------------------

# callbacks for pagination. Callbacks 'next' and 'back'
@router.callback_query(F.data == "next")
async def next_pagination(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            text = LEXICON_ENG["choose_targ"],
            reply_markup = choose_lang_kb(2)
        )
    except(TelegramBadRequest):
        await callback.answer(text=LEXICON_ENG["end_list"], show_alert=True)
        pass


@router.callback_query(F.data == "back")
async def back_pagination(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            text = LEXICON_ENG["choose_targ"],
            reply_markup = choose_lang_kb()
        )
    except(TelegramBadRequest):
        await callback.answer()
        pass
#--------------------------------------------------------------------------------

@router.callback_query(F.data.in_(SUPPORTED_LANGUAGES.keys()), StateFilter(ChooseLangFSM.choose_target))
async def get_targ_language(callback: CallbackQuery, state: FSMContext, async_session: AsyncSession, redis_instance: Redis):

    await update_lang_code(async_session, callback.from_user.id, callback.data, is_targ_lang=True)

    await callback.message.delete()

    await callback.message.answer(
        text=LEXICON_ENG["write_text"] + SUPPORTED_LANGUAGES[callback.data].title()
    )

    await state.clear()


@router.callback_query(F.data.in_(SUPPORTED_LANGUAGES.keys()), StateFilter(ChooseLangFSM.choose_native))
async def get_native_language(callback: CallbackQuery, state: FSMContext, async_session: AsyncSession):
    
    print("Native language ", SUPPORTED_LANGUAGES[callback.data])
    if await get_user(async_session, callback.from_user.id) is None:
        await insert_user(async_session, callback.from_user.id, callback.data)

    await callback.message.edit_text(
        text = LEXICON_ENG["choose_targ"],
        reply_markup = choose_lang_kb()
    )
    # now we need to get TARGET lang
    await state.set_state(ChooseLangFSM.choose_target)


#------------------------------------------------------------------------------------------------------------
# here will be code duplication, unfortunately, because idk how to solve it differently (for now)
@router.callback_query(F.data.in_(SUPPORTED_LANGUAGES.keys()), StateFilter(ChangeLangFSM.change_native))
async def change_native_lang(callback: CallbackQuery, state: FSMContext, async_session: AsyncSession):

    await update_lang_code(async_session, callback.from_user.id, callback.data)

    await state.clear()

    await callback.message.delete()

    await callback.message.answer(
        text=LEXICON_ENG["native_changed"] 
    )

@router.callback_query(F.data.in_(SUPPORTED_LANGUAGES.keys()), StateFilter(ChangeLangFSM.change_target))
async def change_target_lang(callback: CallbackQuery, state: FSMContext, async_session: AsyncSession):

    await update_lang_code(async_session, callback.from_user.id, callback.data, is_targ_lang=True)

    await state.clear()

    await callback.message.delete()
    
    await callback.message.answer(
        text=LEXICON_ENG["target_changed"]
    )

#------------------------------------------------------------------------------------------------------------
