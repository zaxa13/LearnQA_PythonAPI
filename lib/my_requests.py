import requests


class MyRequests:
    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "GET")

    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "POST")

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "PUT")

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "DELETE")

    @staticmethod
    def _send(url: str, data: dict, heades: dict, cookies: dict, method: str):
        url = f"https://playground.learnqa.ru/api{url}"

        if heades is None:
            heades = {}
        if cookies is None:
            cookies = {}

        if method == "GET":
            response = requests.get(url, params=data, headers=heades, cookies=cookies)
        elif method == "POST":
            response = requests.post(url, data=data, headers=heades, cookies=cookies)
        elif method == "PUT":
            response = requests.put(url, data=data, headers=heades, cookies=cookies)
        elif method == "DELETE":
            response = requests.delete(url, data=data, headers=heades, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")
        return response
