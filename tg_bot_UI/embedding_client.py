import os

import requests
from dotenv import load_dotenv

load_dotenv()


class Embedding:
    def __init__(self):
        self.session = requests.Session()
        self.session.auth = (os.getenv('EMBEDDING_USER'), os.getenv('EMBEDDING_PASS'))
        self.url = f"http://{os.getenv('EMBEDDING_HOST')}:{os.getenv('EMBEDDING_PORT')}/embedding"

    def embedding_request(self, data: str, max_length):
        res = self.session.post(self.url, json={'input_text': data, 'max_length': max_length})
        return res.json()
