from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):

    # Попытка получить данные пользователя будучи не авторизованным
    def test_get_user_info_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")
        Assertions.assert_json_has_not_key(response, "email")

    def test_get_user_details_auth_as_same_User(self):
        data = {"email": "vinkotov@example.com",
                "password": "1234"}

        # Вход пользователя в систему ( авторизация)
        response1 = MyRequests.post('/user/login', data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

        # Получить информацию о пользователе по идентификатору (авторизован)
        response2 = MyRequests.get(f"/user/{self.user_id_from_auth_method}",
                                   cookies={"auth_sid": self.auth_sid},
                                   headers={"x-csrf-token": self.token})

        params = [
            "username",
            "firstName",
            "lastName",
            "email"
        ]
        Assertions.assert_json_has_keys(response2, params)




    #Просмотр данных пользователя с чужим user_ID
    def test_get_user_info_another_data(self):
        #REGISTER
        data = self.prepared_data()
        response = MyRequests.post("/user/", data=data)
        user_id = response.json()["id"]

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")


        #LOGIN
        data2 = {"email": "vinkotov@example.com",
                "password": "1234"}

        response1 = MyRequests.post('/user/login', data=data2)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")



        #Получение данных с чужим user_ID
        response2 = MyRequests.get(f"/user/{user_id}",
                                   cookies={"auth_sid": self.auth_sid},
                                   headers={"x-csrf-token": self.token})

        Assertions.assert_status_code(response2,200)
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")
        Assertions.assert_json_has_not_key(response, "email")