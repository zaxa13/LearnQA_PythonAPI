import json

from requests import Response


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not forman JSON. Response text is {response.text}"

        assert name in response_as_dict, f"Response JSON doesn`t have key '{name}'"
        assert response_as_dict[name] == expected_value, error


    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not format JSON. Response text is {response.text}"

        assert name in response_as_dict, f"Response JSON doesn`t have key '{name}'"




    # Проверка приходящих параметров с информацией о пользователе
    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not forman JSON. Response text is {response.text}"
        for name in names:
            assert name in response_as_dict, f"Response JSON doesn`t have key '{name}'"



    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not forman JSON. Response text is {response.text}"

        assert name not in response_as_dict, f"Response JSON shouldn`t have key '{name}'.Buts it's present"




    @staticmethod
    def assert_status_code(response: Response, value):
        assert response.status_code == value, f"Unexpected status code! Expected {value}. Actual {response.status_code}"
