from environs import Env

import aiohttp

import asyncio

from config_data.config import get_api_config, ApiConfig

# create the instance of Env()
env: Env = Env()

# read the variable environment
env.read_env()


async def request_api(text: str, src: str, targ: str) -> any:
    """Fucntion sends the request to API to get translation.
    :text - source text to translate.
    :src - source language for previous parameter 'text'.
    :targ - language to translate input text."""

    # get config
    api_config: ApiConfig = get_api_config()

    # url's API
    url: str = "https://text-translator2.p.rapidapi.com/translate"

    # parameters for POST request
    payload: dict[str, str] = {
        "text": text, # text which need to translate
        "target_language": targ, # the language in which need to translate text from 'q' key
        "source_language": src # the language in which the text is written in 'q'. If it wrote wrong lang-code, the API will detect by itself
    }

    # headers for API translator
    headers: dict[str, str] = {
        "content-type": api_config.content_type,
        "X-RapidAPI-Key": api_config.x_rapidAPI_key,
        "X-RapidAPI-Host": api_config.x_rapidAPI_host
    }

    # asynchronous request by aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            
            # get the response from API and parse with .json()
            res = await response.json()
            
            # checking that request and response were successfully
            if res['status'] != 'success':
                return "Sorry, we could not make a request. Repeat the request."

            return res


async def get_translation(input_text: str, origin_lang: str, translate_lang: str) -> str:
    """Function returns the translated text.\n
    :input_text - the text which need to translate.
    :origin_lang - the language in which the text is written.
    :translate_lang - the language in which need to translate the input text
    """

    # get JSON from API
    translated_text = await request_api(input_text, origin_lang, translate_lang)
    
    return translated_text['data']['translatedText']
