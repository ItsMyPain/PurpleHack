import aiohttp
import requests
from config import get_backend_url

BACKEND_URL = get_backend_url()



async def get_full_response(prompt: str) -> tuple:
    text = 'Здесь будет суммаризированный текст!'
    urls = 'https://cbr.ru/ https://cbr.ru/faq/'
    return text, urls
    """
    async with aiohttp.ClientSession() as session:
        json_request = {"prompt": prompt}
        async with session.post(BACKEND_URL, json=json_request) as response:
            json = await response.json()
            ...
    """