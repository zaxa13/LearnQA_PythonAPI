import requests
type_request = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']

print('First task')
response5 = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type')
print(response5.text)
print(response5.status_code)
# метод возвращает ошибку - Wrong method provided

print('\nSecond task')
response6 = requests.head('https://playground.learnqa.ru/ajax/api/compare_query_type', params= {'method': 'HEAD'})
print(response6.text)
print(response6.status_code)
print()
# Сервер возвращает 400 ошибку http запроса, указывая на то, что сервер не может обработать
# данный запрос как с передачей payload так и без него


for type in type_request:
    param = {"method" : type}
    response = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params= param)
    print(f'Тип передаваемого параметра: {type}, ответ requests.get - {response.text}, status_code = {response.status_code}')
    response1 = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type', data= param)
    print(f'Тип передаваемого параметра: {type}, ответ requests.post - {response1.text}, status_code = {response1.status_code}')
    response2 = requests.put('https://playground.learnqa.ru/ajax/api/compare_query_type', data=param)
    print(f'Тип передаваемого параметра: {type}, ответ requests.put - {response2.text}, status_code = {response2.status_code}')
    response3 = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type', data=param)
    print(f'Тип передаваемого параметра: {type}, ответ requests.delete - {response3.text}, status_code = {response3.status_code}')
    response4 = requests.head('https://playground.learnqa.ru/ajax/api/compare_query_type', data=param)
    print(f'Тип передаваемого параметра: {type}, ответ requests.head - {response4.text}, status_code = {response4.status_code}')
    print()





