import requests

playload = {"name" : "User"}
response = requests.get('https://playground.learnqa.ru/api/hello', params = playload)
print(response.text)