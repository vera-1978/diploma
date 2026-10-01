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


    # Запрос без API-ключа (Проверка авторизации). Негативный тест
def test_api_key_unauthorized():
    # Используем f-строку, чтобы подставить переменную с ключом в URL
    url = f'{BASE_URL}api/v1/api_keys/{API_KEY}'

    # Отправляем GET-запрос совсем без параметра headers
    resp = requests.get(url)

    # Печатаем в консоль реальный статус и ответ сервера, чтобы увидеть ошибку
    print("Реальный статус-код:", resp.status_code)
    print("Ответ сервера:", resp.text)

    # Проверяем статус-код (сервер должен вернуть 401) и заголовки ответа
    assert resp.status_code == 401
    assert "application/json" in resp.headers["content-type"]


    # Запрос несуществующей страницы (невалидные параметры)
def test_film_list_invalid_page():
    # Очищаем URL от дублирования параметров
    url = f'{BASE_URL}api/v2.2/films/collections'

    params = {
        'type': 'TOP_POPULAR_ALL',
        'page': 'fa'  # Невалидное значение
    }

    resp = api.send_get_request(url, params=params)

    # Печатаем в консоль реальный статус и ответ сервера, чтобы увидеть ошибку
    print("Реальный статус-код:", resp.status_code)
    print("Ответ сервера:", resp.text)

    # Временно комментируем ассерт, чтобы тест не падал, пока мы смотрим лог
    assert resp.status_code == 400
