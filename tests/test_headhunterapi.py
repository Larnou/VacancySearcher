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


# Тест пагинации в get_vacancies
def test_get_vacancies_pagination(hh_api, mocker):
    """Проверка правильной работы пагинации"""
    # Мокируем вызов API
    mock_api = mocker.patch.object(hh_api, "get_vacancies_by_api")
    mock_api.side_effect = [[{"id": 1}, {"id": 2}], [{"id": 3}, {"id": 4}]]

    # Вызов тестируемого метода
    result = hh_api.get_vacancies("python")

    # Проверки
    assert len(result) == 4
    assert mock_api.call_count == 2
    assert hh_api._HeadHunterAPI__params["page"] == 2


# Тест установки ключевого слова
def test_keyword_setting(hh_api):
    """Проверка установки ключевого слова"""
    hh_api.get_vacancies("python")
    assert hh_api._HeadHunterAPI__params["text"] == "python"


# Тест сохранения состояния при повторных вызовах
def test_state_persistence(hh_api, mocker):
    """Проверка сохранения состояния между вызовами"""
    # Мокируем вызов API
    mock_api = mocker.patch.object(hh_api, "get_vacancies_by_api")
    mock_api.return_value = [{"id": 1}]

    # Первый вызов
    hh_api.get_vacancies("python")
    # Второй вызов
    result = hh_api.get_vacancies("java")

    # Проверки
    assert len(result) == 2
    assert hh_api._HeadHunterAPI__params["page"] == 2
