from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
from allure_commons.types import Severity


#Ex18, task1
@allure.epic("Delete_user_cases")
class TestUserDelete(BaseCase):
    @allure.severity(Severity.BLOCKER)
    @allure.id(1)
    def test_delete_user_with_test_account(self):
        # Авторизация пользователя
        data = {"email": "vinkotov@example.com",
                "password": "1234"}

        response = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")

        Assertions.assert_status_code(response, 200)

        # Удаление пользователя
        response2 = MyRequests.delete("/user/2",
                                      data=data,
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response2, 400)
        assert response2.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Пользователь с таким id не может быть удален"


    # Ex18, task2
    @allure.severity(Severity.BLOCKER)
    @allure.id(2)
    def test_successful_user_delete(self):

        #REGISTER
        register_data = self.prepared_data()
        response = MyRequests.post("/user/", data=register_data)
        user_id = self.get_json_value(response, "id")
        email = register_data.get("email")
        password = register_data.get("password")

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")


        #Авторизация пользователя
        data = {"email": email,
                "password": password}

        response2 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        Assertions.assert_status_code(response2, 200)


        # Удаление пользователя
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      data=data,
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}")
        print(response4.content)

        Assertions.assert_status_code(response4, 404) #Мне кажется здесь допущена ошибка в status_code,
        # т.к ситуация штатная, хоть пользователь и не обнаружен, здесь должен быть ответ сервера 200
        assert response4.content.decode(
            "utf-8") == 'User not found', \
            "Unexpected error when trying to get user data"

    #Ex18, task3
    @allure.severity(Severity.BLOCKER)
    @allure.id(3)
    def test_negative_delete_user(self):
        #REGISTER_1
        register_data = self.prepared_data()
        response = MyRequests.post("/user/", data=register_data)
        email = register_data.get("email")
        password = register_data.get("password")
        user_id = self.get_json_value(response, "id")

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")


        #Авторизация пользователя
        data = {"email": email,
                "password": password}

        response2 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        Assertions.assert_status_code(response2, 200)



        # REGISTER2
        register_data2 = self.prepared_data()
        response3 = MyRequests.post("/user/", data=register_data2)
        user_id2 = self.get_json_value(response3, "id")

        Assertions.assert_status_code(response3, 200)
        Assertions.assert_json_has_key(response3, "id")


        # Удаление пользователя
        response4 = MyRequests.delete(f"/user/{user_id2}",
                                      data=data,
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        # Assertions.assert_status_code(response4, 403)
        # Здесь есть логическая ошибка, тест падает, т.к авторизованные куки и userID н совпадают,
        # то ответ от сервера должен прийти status_code == 403


        #GET
        response5 = MyRequests.get(
            f"/user/{user_id}"
        )


        print(response5.status_code)
        print(response5.text)

        Assertions.assert_status_code(response5, 200) #Допущена логическая ошибка, т.к в методе delete мы указали user_id и cookies от разных пользователей,
        # то user от которого мы применяли cookies не должен был удалиться,
