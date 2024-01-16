from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon import LEXICON_ENG

def answer_keyboard() -> InlineKeyboardMarkup:
    """Function creates the answer keyboard with 'yes' and 'no' options."""

    # init InlineButtons builder
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(
        *[
            InlineKeyboardButton(text=LEXICON_ENG["option_yes"],
                                callback_data="answer_yes"),

            InlineKeyboardButton(text=LEXICON_ENG["option_no"],
                                callback_data="answer_no")
        ]
    )

    return kb_builder.as_markup()


