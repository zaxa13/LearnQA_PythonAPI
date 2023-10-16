import requests
import time

response = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job')

pars_response = response.json()
token = pars_response['token']
times = int(pars_response['seconds'])

response2 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params= {'token': token})
print(response2.text)

time.sleep(times)
response3 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params= {'token': token})
print(response3.text)
