

LEXICON_ENG: dict[str, str] = {
    "/start":               "Hi👋\nI'm a translator bot🤖. If you wanna get a translation, call me😊",
    "/help":                """Here are the commands to use this bot:
/start - run a bot.
/help - get information about using the bot.
/change_native - change your native language.
/change_target - change your target language.
""",
    "/change_native":       "Please, choose the language below ⬇⬇⬇",
    "/change_target":       "Please, choose the language below ⬇⬇⬇",
    "leave_last":           "Leave the last❎",
    "back":                 "<<",
    "next":                 ">>",
    "option_yes":           "Yes✅",
    "option_no":            "No❌",
    "end_list":             "You have reached the end.", # alert в боте, что-то было такое. Будем использовать всплывающее предупреждение, если человек дошел до конца или начало списка с языками
    "choose_lang_warn":     "You didn't choose the language❗❗❗\nPlease, choose the language", # alert в боте, что-то было такое. Будем использовать, если человек нажал "leave_last", но при этом только зарегался, то есть в базе его родного языка нет.
    "others":               "Sorry, but i can't interact with this type of message😐\nTry again, please!",
    "save":                 "save translation🔸",
    "nat_lang":             "Is your native language ",
    "choose_targ":          "Please, choose the target language below ⬇⬇⬇",
    "choose_nat":           "Please, choose your native language below ⬇⬇⬇",
    "write_text":           "Now, you can write any text in your native and i will translate that to ",
    "without_profile":      "Sorry, you have to register your profile🔴! Write /start",
    "has_account":          "You already have an account✌, so just write a text😊",
    "native_changed":       "Native language has changed successfully✅",
    "target_changed":       "Target language has changed successfully✅",
    "same_targ_native":     "Your native can't be your target language😞😞\nWrite /change_native or /change_target to change one of your language",
}





LEXICON_COMMANDS: dict[str, str] = {
    "/start": "run a bot",
    "/help": "get information about using the bot.",
    "/change_native": "change your native language.",
    "/change_target": "change your target language.",
    "/profile": "get info about your profile"
}