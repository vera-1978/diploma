import requests


class KinopoiskApi:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {
            'X-API-KEY': api_key
        }

    def send_get_request(self, url, params=None):
        # Просто отправляем пришедший URL, добавив параметры и заголовки
        return requests.get(url, params=params, headers=self.headers)
