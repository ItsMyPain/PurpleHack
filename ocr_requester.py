import os

import requests
from dotenv import load_dotenv

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
    return r.content.decode()


test_file = ocr_space_file(filename='0_part_0.pdf')
print(test_file)
