import aiohttp
import asyncio


MAX_TEXT_LEN = 5000


async def preprocess_input_prompt(prompt: str):
    corrected_words = await request_to_corrector(prompt)
    if corrected_words is not None:
        for error in corrected_words:
            s = error.get('s', [''])[0]
            if len(s) == 0:
                s = ['']
            if error['code'] in [1, 2, 3]:
                prompt = prompt.replace(error['word'], s)

    if len(prompt) > MAX_TEXT_LEN:
        prompt = prompt[:MAX_TEXT_LEN - 1]
    return prompt




async def request_to_corrector(words: str) -> dict:
    YANDEX_URL = 'http://speller.yandex.net/services/spellservice.json/checkText'
    
    if len(words) > MAX_TEXT_LEN:
        words = words[:MAX_TEXT_LEN - 1]

    async with aiohttp.ClientSession() as session:
        data = {
            'lang': 'ru',
            'format': 'plain',
            'text': words,
            'options': 16
        }
        async with session.post(YANDEX_URL, data=data) as response:
            json = await response.json()
            if response.status != 200:
                return None
            if json is not None:
                if len(json) != 0:
                    return json
            return None
        

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(preprocess_input_prompt())