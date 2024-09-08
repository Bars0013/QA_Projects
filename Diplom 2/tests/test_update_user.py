import allure
import requests
import pytest

from conftest import create_new_user, generate_user_credentials
from data import ExistentUserCredentials, GenerateUserCredentials
from urls import Urls


class TestUpdateUser:

    @allure.title('Проверка что данные любого поля можно изменить авторизованным пользователем')
    @allure.description('При запросе передается каждое из полей авторизованным пользователем')
    @pytest.mark.parametrize('update_data', [({"email": GenerateUserCredentials.email}),
                                             ({"password": GenerateUserCredentials.password}),
                                             ({"name": GenerateUserCredentials.name})])
    def test_update_user_authorized_user_update_fields_success(self, update_data, create_new_user):
        access_token = create_new_user[1]["accessToken"]
        headers = {"Authorization": f"{access_token}"}
        payload = update_data
        response = requests.patch(f'{Urls.UPDATE_USER}', data=payload, headers=headers)
        data = response.json()

        assert response.status_code == 200 and data["success"] == True

    @allure.title('Проверка невозможности изменения любого поля не авторизованным пользователем')
    @allure.description('При запросе передается каждое из полей не авторизованным пользователем')
    @pytest.mark.parametrize('update_data', [({"email": GenerateUserCredentials.email}),
                                             ({"password": GenerateUserCredentials.password}),
                                             ({"name": GenerateUserCredentials.name})])
    def test_update_user_unauthorized_user_update_fields_error(self, update_data):
        payload = update_data
        response = requests.patch(f'{Urls.UPDATE_USER}', data=payload)
        data = response.json()

        assert response.status_code == 401 and data["success"] == False and data[
            "message"] == "You should be authorised"

    @allure.title('Проверка передачи почты, которая уже используется ')
    @allure.description('При запросе передается уже существующая почта')
    def test_update_user_authorized_user_existent_email_error(self, create_new_user):
        access_token = create_new_user[1]["accessToken"]
        headers = {"Authorization": f"{access_token}"}
        email = ExistentUserCredentials.email
        password = GenerateUserCredentials.password
        name = GenerateUserCredentials.name
        payload = {'email': email, 'password': password, 'name': name}
        response = requests.patch(f'{Urls.UPDATE_USER}', data=payload, headers=headers)
        data = response.json()

        assert response.status_code == 403 and data["success"] == False and data[
            "message"] == "User with such email already exists"
