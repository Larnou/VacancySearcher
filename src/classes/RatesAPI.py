import json

import requests


class RatesAPI:

    __API_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

    def __init__(self):
        pass

    def get_rates_by_api(self) -> dict:
        """
        Получает список курсов валют через подключение к ЦБРФ Api.

        Returns:
            Список курсов валют
        """
        try:
            response = requests.get(self.__API_URL)

            # Проверка статус-кода ответа
            if response.status_code != 200:
                print(f"Ошибка API: статус {response.status_code}")
                return {}
            else:
                rates = response.json()
                rates = rates.get('Valute')
                return rates

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API ЦБРФ: {e}")
            return {}
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Ошибка обработки ответа API ЦБРФ: {e}")
            return {}

    @staticmethod
    def get_currency_rate(curency_code, rate_dict) -> float:
        currency = rate_dict[curency_code]
        currency_value = currency['Value']
        currency_nominal = currency['Nominal']
        return currency_value / currency_nominal
