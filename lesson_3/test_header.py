import requests

def test_headers():
    response = requests.get('https://playground.learnqa.ru/api/homework_header')
    headers = response.headers
    print(headers)
    assert response.headers == headers, "The headers doesn't match"