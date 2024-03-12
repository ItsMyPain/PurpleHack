import requests

session = requests.Session()
session.auth = ('doctor23', 'acfab71e-7700-46c7-959d-1776436d2167')

auth = session.post('http://81.94.156.185:8889/embedding', json={'input_text': 'Привет, как дела?'})
print(auth)
print(auth.json())
