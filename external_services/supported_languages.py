from bs4 import BeautifulSoup

import asyncio 

import aiohttp



SUPPORTED_LANGUAGES: dict[str, str] = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'be': 'belarusian',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'haw': 'hawaiian',
    'hi': 'hindi',
    'hu': 'hungarian',
    'is': 'icelandic',
    'id': 'indonesian',
    'it': 'italian',
    'ja': 'japanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'ko': 'korean',
    'ky': 'kyrgyz',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mn': 'mongolian',
    'ne': 'nepali',
    'no': 'norwegian',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'ro': 'romanian',
    'ru': 'russian',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'sk': 'slovak',
    'sl': 'slovenian',
    'es': 'spanish',
    'sv': 'swedish',
    'tg': 'tajik',
    'tt': 'tatar',
    'th': 'thai',
    'tr': 'turkish',
    'tk': 'turkmen',
    'uk': 'ukrainian',
    'uz': 'uzbek',
    'vi': 'vietnamese',
}





"""Code for parcing the page with languages."""

""" 
async def parse_page(page: str) -> None:
    soup = BeautifulSoup(page, "lxml")
    langs = soup.find("table", class_="table").find("tbody").findAll("td")
    temp_dict_str = "{"

    for index, lang in enumerate(langs, 0):
        if index % 2:
            temp_dict_str += f"\'{lang.text}\': \'{langs[index-1].text.lower()}\',\n"
        print(index, lang.text)
    temp_dict_str += "}"
    print(temp_dict_str)


async def get_page():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://rapidapi.com/dickyagustin/api/text-translator2/details") as response:
            
            if response.status == 200:
                res_page = await response.text()
                await parse_page(res_page)
                return "Function worked correctly"

            
async def main():
    res = await get_page()

    print("Sorry, we couldnt make a request." if res is None else res)

asyncio.run(main())
"""