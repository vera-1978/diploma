import os
from dotenv import load_dotenv
from PageApiKinopoisk import KinopoiskApi

# Загружаем переменные из файла .env в систему
load_dotenv()

# Считываем ключ из секретных переменных окружения
API_KEY = os.getenv('KINOPOISK_API_KEY')
BASE_URL = 'https://kinopoiskapiunofficial.tech/'


# Инициализируем наш API-клиент
api = KinopoiskApi(base_url=BASE_URL, api_key=API_KEY)

# Получить данные об api key
def test_api_key():
    # Исользуем f-строку, чтобы подставить переменную с ключом в URL
    url = f'{BASE_URL }api/v1/api_keys/{API_KEY}'

    # Отправляем GET-запрос
    # Используем вспомогательный метод
    resp = api.send_get_request(url)

    # Проверяем статус-код и заголовки ответа
    assert resp.status_code == 200


    # Получить список фильмов
def test_film_list():
    # ИСПРАВЛЕНО: Убрали параметры из строки URL, оставили только чистый эндпоинт
    url = BASE_URL + 'api/v2.2/films/collections'

    # 2. Обязательные параметры для этого метода
    params = {
        'type': 'TOP_POPULAR_ALL',
        'page': 1
    }

    # Отправляем GET-запрос со всеми собранными данными
    # Используем вспомогательный метод
    resp = api.send_get_request(url, params=params)

    print("Реальный статус-код:", resp.status_code)
    print("Ответ сервера:", resp.text)

    # Проверяем статус-код и заголовки ответа сервера
    assert resp.status_code == 200


    # Получить данные о фильме по kinopoisk id
def test_get_movie_by_id():
    # Используем f-строку, чтобы подставить переменную с ключом в URL
    url = f'{BASE_URL}api/v2.2/films/7036356'

    # Отправляем GET-запрос со всеми собранными данными
    # Используем вспомогательный метод
    resp = api.send_get_request(url)

    # Проверяем статус-код и заголовки ответа сервера
    assert resp.status_code == 200

    # Извлекаем JSON-данные и выводим их в консоль
    movie_data = resp.json()
    print("Данные о фильме:", movie_data)


    # Получить список премьер
def test_premieres_films():
    # Используем f-строку, чтобы подставить переменную с ключом в URL
    url = f'{BASE_URL}api/v2.2/films/premieres?year=2025&month=JANUARY'

    # Отправляем GET-запрос со всеми собранными данными
    # Используем вспомогательный метод
    resp = api.send_get_request(url)

    # Проверяем статус-код и заголовки ответа сервера
    assert resp.status_code == 200

    # Извлекаем JSON-данные и выводим их в консоль
    movie_data = resp.json()
    print("Список премьер:", movie_data)
