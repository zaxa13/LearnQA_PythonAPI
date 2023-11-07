import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest
import allure
from allure_commons.types import Severity
from allure_commons.types import LabelType

@allure.epic("user_register_cases")
class TestUserRegister(BaseCase):
    # СОЗДАНИЕ НОВОГО ПОЛЬЗОВАТЕЛЯ
    @allure.id(1)
    @allure.severity(Severity.NORMAL)
    def test_create_user_successfully(self):
        data = self.prepared_data()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")



    # Попытка создания пользователя с уже созданным email ранее
    @allure.id(2)
    @allure.severity(Severity.BLOCKER)
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepared_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content, {response.content}"



    # Попытка регистрации с адресом почты без символа @
    @allure.id(3)
    @allure.severity(Severity.BLOCKER)
    def test_create_user_without_symbol_dog(self):
        email = "vinkotovexample.com"
        data = self.prepared_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == "Invalid email format", f"Unexpected response content, {response.content}"



    # Попытка регистрации без использования одного из параметров
    @pytest.mark.parametrize("condition", ["username", "firstName", "lastName", "email", "password"])
    @allure.id(4)
    @allure.severity(Severity.BLOCKER)
    def test_create_user_without_one_parameter(self, condition):
        data = self.prepared_data()
        data.pop(condition)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {condition}", \
            f"The user should not register without the parameter - '{condition}'"



    # Регистрация пользователя с коротким именем (1 символ)
    @allure.id(5)
    @allure.severity(Severity.CRITICAL)
    def test_create_user_short_name(self):
        data = self.prepared_data()
        user_name = "a"
        data["username"] = user_name

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f"The user should not register with this name - '{user_name}'"



    # Регистрация пользователя с длинным именем (> 250 символов)
    @allure.id(6)
    @allure.severity(Severity.NORMAL)
    def test_create_user_long_name(self):
        data = self.prepared_data()
        user_name = ("testtesttesttesttesttesttesttesttesttesttesttesttesttesttestte"
                     "sttesttesttesttesttesttesttesttesttesttesttesttesttesttesttestt"
                     "esttesttesttesttesttesttesttesttesttesttesttesttesttesttesttestt"
                     "esttesttesttesttesttesttesttesttesttesttesttesttestvtesttestte")
        data["username"] = user_name

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long", \
            f"The user should not register with this name - '{user_name}'"

