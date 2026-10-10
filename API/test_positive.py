import allure
import os
from dotenv import load_dotenv
from PageApiKinopoisk import KinopoiskApi

load_dotenv()

API_KEY = os.getenv('KINOPOISK_API_KEY')
BASE_URL = 'https://kinopoiskapiunofficial.tech/'

# Инициализируем наш API-клиент
api = KinopoiskApi(base_url=BASE_URL, api_key=API_KEY)

pytestmark = allure.epic('API тесты')


@allure.story('Получить данные об api key')
@allure.title('Проверка валидности API ключа')
def test_api_key():
    # Объявление URL перенесли внутрь логического шага
    with allure.step('Отправить GET-запрос для проверки API ключа'):
        url = f'{BASE_URL}api/v1/api_keys/{API_KEY}'
        resp = api.send_get_request(url)

    with allure.step('Проверить, что сервер вернул статус-код 200'):
        assert resp.status_code == 200


@allure.story('Получить список фильмов')
@allure.title('Получение списка популярных фильмов')
def test_film_list():
    with allure.step(
            'Отправить GET-запрос на получение коллекции фильмов'):
        url = BASE_URL + 'api/v2.2/films/collections'
        params = {'type': 'TOP_POPULAR_ALL', 'page': 1}
        resp = api.send_get_request(url, params=params)

        print("Реальный статус-код:", resp.status_code)
        print("Ответ сервера:", resp.text)

    with allure.step(
            'Проверяем статус-код и заголовки ответа сервера'):
        assert resp.status_code == 200


@allure.story('Получить данные о фильме по kinopoisk id')
@allure.epic('API тесты')
@allure.title('Получение данных о фильме по id')
def test_get_movie_by_id():
    with allure.step('Отправить GET-запрос для фильма'):
        url = f'{BASE_URL}api/v2.2/films/7036356'
        resp = api.send_get_request(url)

    with allure.step('Проверить успешность запроса (Статус 200)'):
        assert resp.status_code == 200

    with allure.step('Извлекаем JSON-данные и выводим их в консоль'):
        movie_data = resp.json()
        print("Данные о фильме:", movie_data)


@allure.story('Получить список премьер')
@allure.title('Получение списка премьер')
def test_premieres_films():
    with allure.step(
            'Отправить GET-запрос на получение премьер за январь 2025'):
        url = f'{BASE_URL}api/v2.2/films/premieres?year=2025&month=JANUARY'
        resp = api.send_get_request(url)

    with allure.step('Проверяем статус-код и заголовки ответа сервера'):
        assert resp.status_code == 200

    with allure.step('Извлекаем JSON-данные и выводим их в консоль'):
        movie_data = resp.json()
        print("Список премьер:", movie_data)
