from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from external_services.supported_languages import SUPPORTED_LANGUAGES

from lexicon.lexicon import LEXICON_ENG

# This keyboard will show all available languages to choose for target or native (it doesnt matter)
def choose_lang_kb(page_pageination: int = 1) -> InlineKeyboardMarkup:
    
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # buttons for pagination languages
    pagination_buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text=LEXICON_ENG["back"], callback_data="back"),
        InlineKeyboardButton(text=LEXICON_ENG["next"], callback_data="next")
    ]

    # our languages
    languages_buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text=language.title(), callback_data=language_code) for language_code, language in SUPPORTED_LANGUAGES.items()
    ]

    # adding pagination signs to keyboard
    kb_builder.row(*pagination_buttons, width=2)

    # adding the languages
    first_page: list[InlineKeyboardButton] = languages_buttons[:30]
    second_page: list[InlineKeyboardButton] = languages_buttons[30:]
    
    kb_builder.row(*(first_page if page_pageination == 1 else second_page), width=5)

    return kb_builder.as_markup()




















