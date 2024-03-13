import os

import requests
from dotenv import load_dotenv

load_dotenv()


class Llama:
    def __init__(self):
        self.session = requests.Session()
        self.session.auth = (os.getenv('LLAMA_USER'), os.getenv('LLAMA_PASS'))
        self.url = f"http://{os.getenv('LLAMA_HOST')}:{os.getenv('LLAMA_PORT')}/model"

    def llama_request(self, data: str):
        auth = self.session.post(self.url, json={'user_prompt': data})
        return auth.json()
