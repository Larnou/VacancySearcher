import json

import requests

from src.classes.parser import Parser


class HeadHunterAPI(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """
    __API_URL = 'https://api.hh.ru/vacancies'

    def __init__(self):
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 10}
        self.__vacancies = []


    def get_vacancies_by_api(self):
        try:
            response = requests.get(self.__API_URL, headers=self.__headers, params=self.__params)

            # Проверка статус-кода ответа
            if response.status_code != 200:
                print(f"Ошибка API: статус {response.status_code}")
                return []
            else:
                vacancies = response.json()['items']
                return vacancies

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API hh.ru: {e}")
            return []
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Ошибка обработки ответа API: {e}")
            return []


    def get_vacancies(self, keyword):
        self.__params['text'] = keyword
        while self.__params.get('page') != 1:
            vacancies = self.get_vacancies_by_api()
            self.__vacancies.extend(vacancies)
            self.__params['page'] += 1

        return self.__vacancies
