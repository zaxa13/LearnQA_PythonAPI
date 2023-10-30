import requests

def test_cookie():
    response = requests.get('https://playground.learnqa.ru/api/homework_cookie')
    cookies = response.cookies
    print(cookies)
    assert response.cookies == cookies, "The cookies doesn't match"


