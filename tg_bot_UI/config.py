from dotenv import load_dotenv
import os

START_MSG = 'Стартовое сообщение!'
MODE_MSG = 'Выберите режим'
INFO_MSG = 'Инструкция по использованию бота'
FEEDBACK_MSG = 'Сообщение с контактами разработчиков'

def get_tg_token():
    load_dotenv()
    return os.getenv('TG_TOKEN')


def get_backend_url():
    BACKEND_URL = ''
    return BACKEND_URL