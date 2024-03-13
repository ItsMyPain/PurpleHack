import aiohttp
import requests
from config import get_backend_url

BACKEND_URL = get_backend_url()


async def get_answer_from_bd(prompt: str) -> str:
    return 'Здесь будет ответ из бд вопрос ответов. Или ответ, что не нашли'

async def get_RAG(prompt: str) -> str:
    return 'Тут вернем новые сформированные вопросы'

async def get_paragraps_from_documents(prompt: str) -> str:
    return 'Тут вернем топики, которые нашли из бд, мб косинусные расстояния, по которым сортировали'

async def get_final_result(prompt: str) -> str:
    return 'Тут будет суммарный ответ от модели'