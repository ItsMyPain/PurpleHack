import requests

session = requests.Session()
session.auth = ('doctor22', '287aaeb9-6173-4183-8b88-b8182b6908d1')

auth = session.post('http://81.94.156.185:8888/model', json={'user_prompt': 'test'})
print(auth)
print(auth.text)
