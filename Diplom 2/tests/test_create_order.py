import allure
import requests

from conftest import create_new_user, generate_user_credentials
from data import IngredientsData
from urls import Urls


class TestCreateOrder:

    @allure.title('Проверка создания заказа с ингредиентами авторизованным пользователем')
    @allure.description('При создании заказа передаются существующие ингредиенты'
                        'авторизованным созданным пользователем')
    def test_create_order_authorized_user_actual_ingredients_success(self, create_new_user):
        access_token = create_new_user[1]["accessToken"]
        headers = {"Authorization": f"{access_token}"}
        payload = {
            'ingredients': [IngredientsData.BUN, IngredientsData.SAUCE, IngredientsData.FILLER]
        }
        response = requests.post(f'{Urls.GET_USER_ORDERS}', data=payload, headers=headers)
        data = response.json()
        assert response.status_code == 200
        assert data["success"] == True


    @allure.title('Проверка создания заказа с ингредиентами  не авторизованным пользователем')
    @allure.description('При создании заказа передаются существующие ингредиенты не авторизованным пользователем')
    def test_create_order_unauthorized_user_actual_ingredients_success(self):
        payload = {
            'ingredients': ['61c0c5a71d1f82001bdaaa6d', '61c0c5a71d1f82001bdaaa75', '61c0c5a71d1f82001bdaaa78']
        }
        response = requests.post(f'{Urls.GET_USER_ORDERS}', data=payload)
        data = response.json()
        assert response.status_code == 200
        assert data["success"] == True


    @allure.title('Проверка создания заказа без ингредиентов авторизованным пользователем')
    @allure.description('При создании заказа авторизованным созданным пользователем не передаются ингредиенты ')
    def test_create_order_authorized_user_no_ingredients_error(self, create_new_user):
        access_token = create_new_user[1]["accessToken"]
        headers = {"Authorization": f"{access_token}"}
        payload = {'ingredients': ['']}
        response = requests.post(f'{Urls.GET_USER_ORDERS}', data=payload, headers=headers)
        data = response.json()
        assert response.status_code == 400
        assert data["success"] == False
        assert response.json()['message'] == 'Ingredient ids must be provided'


    @allure.title('Проверка создания заказа без ингредиентов не авторизованным пользователем')
    @allure.description('При создании заказа не авторизованным пользователем не передаются ингредиенты ')
    def test_create_order_unauthorized_user_no_ingredients_error(self):
        payload = {'ingredients': ['']}
        response = requests.post(f'{Urls.GET_USER_ORDERS}', data=payload)
        data = response.json()
        assert response.status_code == 400
        assert data["success"] == False
        assert response.json()['message'] == 'Ingredient ids must be provided'


    @allure.title('Проверка создания заказа с неверным хешем ингредиентов авторизованным пользователем')
    @allure.description('При создании заказа авторизованным  пользователем не передаются ингредиенты с неверным хешем')
    def test_create_order_authorized_user_bad_ingredients_hash_error(self, create_new_user):
        access_token = create_new_user[1]["accessToken"]
        headers = {"Authorization": f"{access_token}"}
        payload = {'ingredients': ['51c0c5a71d1f82001bdaaa6']}
        response = requests.post(f'{Urls.GET_USER_ORDERS}', data=payload, headers=headers)
        assert response.status_code == 500

