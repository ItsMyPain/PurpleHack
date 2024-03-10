import os
from pathlib import Path
import requests
from dotenv import load_dotenv
import json

load_dotenv()


def ocr_space_file(filename):
    payload = {
        'apikey': os.getenv('OCR_API_KEY'),
        'language': 'rus',
        'isOverlayRequired': False,
        'filetype': 'PDF',
        'detectOrientation': False,
        'isCreateSearchablePdf': False,
        'isSearchablePdfHideTextLayer': False,
        'scale': False,
        'isTable': False,
        'OCREngine': 1
    }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return json.loads(r.content.decode())

def save_result(text: str, file_name: str = 'result.txt'):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(text.replace('\n', ''))

def get_text_from_pdf(folder: Path, pdf_id: int = 0, part: int = 0):
    file_path = folder / f'id_{pdf_id}' / f'id_{pdf_id}_{part}.pdf'
    test_file = ocr_space_file(filename=str(file_path))
    text = ''
    for el in test_file['ParsedResults']:
        text += el['ParsedText']
    return text


if __name__ == '__main__':
    pdf_folder = Path(r'C:\Users\maxxx\VSprojects\hacks\purple\download')
    text = get_text_from_pdf(pdf_folder, pdf_id=0, part=0)
    print(text)
    save_result(text)

