import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect')

count_redirect = len(response.history)
final_redirect = response
print(count_redirect)
print(final_redirect.url)