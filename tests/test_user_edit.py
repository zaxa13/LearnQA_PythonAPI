from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
from allure_commons.types import Severity

@allure.epic("Edit_user_cases")
class TestUserEdit(BaseCase):

    # REGISTER
    @allure.id(1)
    @allure.severity(Severity.BLOCKER)
    def test_edit_just_created_user(self):
        register_data = self.prepared_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)
        Assertions.assert_status_code(response2, 200)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed name"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token},
            data={"firstName": new_name})

        Assertions.assert_status_code(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        Assertions.assert_status_code(response4, 200)
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Неверное имя после редактирования"
        )

    # Попытка изменить данные пользователя, будучи неавторизованными
    @allure.id(2)
    @allure.severity(Severity.BLOCKER)
    def test_user_edit_not_auth(self):  # EX17task1
        data = self.prepared_data()
        response = MyRequests.post("/user/", data=data)
        user_id = response.json()["id"]

        new_name = "Changed name"
        response2 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name})

        Assertions.assert_status_code(response2, 400)
        assert response2.content.decode("utf-8") == "Auth token not supplied", \
            f"Unexpected response content - '{response2.content}'"

    #
    @allure.id(3)
    @allure.severity(Severity.BLOCKER)
    def test_user_edit_auth_other_auth_data(self):  # EX17task2
        # REGISTER1
        register_data = self.prepared_data()
        response1 = MyRequests.post("/user/", data=register_data)
        user_id = self.get_json_value(response1, "id")
        email = register_data["email"]
        password = register_data["password"]

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")


        # REGISTER2
        register_data2 = self.prepared_data()
        response2 = MyRequests.post("/user/", data=register_data2)
        user_id2 = self.get_json_value(response2, "id")

        Assertions.assert_status_code(response2, 200)
        Assertions.assert_json_has_key(response2, "id")


        #LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response3 = MyRequests.post("/user/login", data=login_data)
        Assertions.assert_status_code(response2, 200)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # EDIT
        new_name = "Changed name"
        response4 = MyRequests.put(
            f"/user/{user_id2}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token},
            data={"firstName": new_name})

        Assertions.assert_status_code(response4, 403,)
        #Здесь есть логическая ошибка, тест падает, т.к авторизованные куки и userID не совпадают,
        # то ответ от сервера должен прийти status_code == 403, вместо status_code ==200

    @allure.id(4)
    @allure.severity(Severity.BLOCKER)
    def test_user_edit_auth_incorrect_email(self):  # EX17task3
        # REGISTER
        data = self.prepared_data()
        response = MyRequests.post("/user/", data=data)
        user_id = response.json()["id"]
        email = data.get("email")

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

        # LOGIN
        user_data = {"email": email,
                     "password": "1234"}

        response1 = MyRequests.post('/user/login', data=user_data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")

        # EDIT
        new_email = "testtest.com"
        response2 = MyRequests.put(
            f"/user/{user_id}",
            cookies={"auth_sid": self.auth_sid},
            headers={"x-csrf-token": self.token},
            data={"email": new_email})

        print(response2.status_code)
        print(response2.content)
        Assertions.assert_status_code(response2, 400)
        assert response2.content.decode(
            "utf-8") == "Invalid email format", "Недопустимое значение email для редактирования"

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            cookies={"auth_sid": self.auth_sid},
            headers={"x-csrf-token": self.token}
        )

        Assertions.assert_status_code(response4, 200)
        Assertions.assert_json_value_by_name(
            response4,
            "email",
            email,
            "Неверный email после редактирования")

    @allure.id(5)
    @allure.severity(Severity.BLOCKER)
    def test_user_name_edit_with_auth(self):  # EX17task4
        # REGISTER
        data = self.prepared_data()
        response = MyRequests.post("/user/", data=data)
        user_id = response.json()["id"]
        email = data.get("email")
        user_name = data.get("firstName")

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

        # LOGIN
        user_data = {"email": email,
                     "password": "1234"}

        response1 = MyRequests.post('/user/login', data=user_data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")

        # EDIT
        new_email = "t"
        response2 = MyRequests.put(
            f"/user/{user_id}",
            cookies={"auth_sid": self.auth_sid},
            headers={"x-csrf-token": self.token},
            data={"firstName": new_email})

        print(response2.status_code)
        print(response2.content)
        Assertions.assert_status_code(response2, 400)
        assert response2.content.decode(
            "utf-8") == '{"error":"Too short value for field firstName"}', \
            "Unexpected error when trying to edit data"
