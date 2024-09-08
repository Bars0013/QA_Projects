import random
import allure
import string
import requests
import data

from data import Url


@allure.step('Генерируем рандомную строку')
def generate_random_string(length=10):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


@allure.step('Генерируем рандомный email')
def generate_random_email():
    return f'{generate_random_string()}@gmail.com'


@allure.step('Создаем заказ')
def create_order(user):
    payload = {
        'ingredients': [data.TestData.INGREDIENTS]
    }
    headers = {'Authorization': user['json']['accessToken']}
    response = requests.post(Url.ORDERS_HANDLE, data=payload, headers=headers)
    return response
