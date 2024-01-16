from aiogram import Bot

from aiogram.types import BotCommand

from lexicon.lexicon import LEXICON_COMMANDS


async def set_main_menu(bot: Bot):
    """Function sets the bot's main menu"""

    # create the list of BotCommand()
    main_menu_commands: list[BotCommand] = [
        BotCommand(command=comm, description=desc) for comm, desc in LEXICON_COMMANDS.items()
    ]

    # call the bot method .set_my_commands()
    await bot.set_my_commands(main_menu_commands)