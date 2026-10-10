import allure
import requests
from PageApiKinopoisk import KinopoiskApi
import os
from dotenv import load_dotenv
load_dotenv()

# Считываем ключ из секретных переменных окружения
API_KEY = os.getenv('KINOPOISK_API_KEY')
BASE_URL = 'https://kinopoiskapiunofficial.tech/'

# Инициализируем наш API-клиент
api = KinopoiskApi(base_url=BASE_URL, api_key=API_KEY)


@allure.story('Запрос без API-ключа (Проверка авторизации). Негативный тест')
@allure.epic('API тесты')
@allure.title('Запрос без API-ключа')
@allure.description('Негативный тест')
def test_api_key_unauthorized():
    with allure.step(
            'Используем f-строку, чтобы подставить переменную с ключом в URL'):
        url = f'{BASE_URL}api/v1/api_keys/'

    with allure.step('Отправляем GET-запрос совсем без параметра headers'):
        resp = requests.get(url)

    with allure.step(
            'Печатаем в консоль реальный статус и ответ сервера, '
            'чтобы увидеть ошибку'):
        print("Реальный статус-код:", resp.status_code)
        print("Ответ сервера:", resp.text)

    with allure.step(
            'Проверяем статус-код (сервер должен вернуть 401) '
            'и заголовки ответа'):
        assert resp.status_code == 401
        assert "application/json" in resp.headers["content-type"]


@allure.story('Запрос несуществующей страницы (невалидные параметры)')
@allure.epic('API тесты')
@allure.title('Запрос несуществующей страницы')
@allure.description('Негативный тест')
def test_film_list_invalid_page():
    with allure.step('Очищаем URL от дублирования параметров'):
        url = f'{BASE_URL}api/v2.2/films/collections'

    params = {
        'type': 'TOP_POPULAR_ALL',
        'page': 'fa'  # Невалидное значение
    }

    resp = api.send_get_request(url, params=params)

    with allure.step(
            'Печатаем в консоль реальный статус и ответ сервера, '
            'чтобы увидеть ошибку'):
        print("Реальный статус-код:", resp.status_code)
        print("Ответ сервера:", resp.text)

    with allure.step('Проверяем статус-код (сервер должен вернуть 400)'):
        assert resp.status_code == 400
