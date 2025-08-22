import json

import pytest
from requests import RequestException


# Тесты инициализации
def test_initialization(hh_api):
    """Проверка корректной инициализации объекта"""
    assert hh_api._HeadHunterAPI__headers == {"User-Agent": "HH-User-Agent"}
    assert hh_api._HeadHunterAPI__params == {"text": "", "page": 0, "per_page": 10}
    assert hh_api._HeadHunterAPI__vacancies == []


# Параметризованные тесты для get_vacancies_by_api
@pytest.mark.parametrize(
    "status_code, response_data, expected, exception",
    [
        # Успешный запрос
        (200, {"items": [{"id": 1}, {"id": 2}]}, [{"id": 1}, {"id": 2}], None),
        # Ошибка HTTP
        (404, None, [], None),
        # Ошибка сети
        (200, None, [], RequestException),
        # Ошибка JSON
        (200, "invalid_json", [], json.JSONDecodeError),
        # Отсутствие ключа items
        (200, {"data": []}, [], KeyError),
    ],
)
def test_get_vacancies_by_api(hh_api, mock_requests_get_hhapi, status_code, response_data, expected, exception):
    """Тестирование различных сценариев get_vacancies_by_api"""
    # Настройка мока
    mock_response = mock_requests_get_hhapi.return_value
    mock_response.status_code = status_code

    if exception == RequestException:
        mock_requests_get_hhapi.side_effect = RequestException("Connection error")
    elif exception == json.JSONDecodeError:
        mock_response.json.side_effect = json.JSONDecodeError("Error", "doc", 0)
    elif exception == KeyError:
        mock_response.json.return_value = response_data
    else:
        mock_response.json.return_value = response_data

    # Вызов тестируемого метода
    result = hh_api.get_vacancies_by_api()

    # Проверка результата
    assert result == expected


# Тест установки ключевого слова
def test_keyword_setting(hh_api):
    """Проверка установки ключевого слова"""
    hh_api.get_vacancies("python")
    assert hh_api._HeadHunterAPI__params["text"] == "python"
