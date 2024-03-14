from translate import Translator
import re

eng_letters = re.compile("[a-zA-Z]+")



def post_process(text: str):
    if has_eng_letters(text):
        text = translate(text, from_lang='en', to_lang='ru')
    return text

def double_translate(text: str):
    en_text = translate(text, from_lang='ru', to_lang='en')
    return translate(en_text, from_lang='en', to_lang='ru')


def translate(text: str, from_lang: str, to_lang: str) -> str:
    translate_to_ru = Translator(to_lang=to_lang, from_lang=from_lang)
    return translate_to_ru.translate(text)

def has_eng_letters(text: str) -> bool:
    words_arr = text.split()
    for el in filter(eng_letters.match, words_arr):
        return True
    return False
