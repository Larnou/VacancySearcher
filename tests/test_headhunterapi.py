import json

import pytest
import requests


# Тесты инициализации
def test_initialization(hh_api):
    """Проверка корректной инициализации объекта"""
    assert hh_api._HeadHunterAPI__headers == {"User-Agent": "HH-User-Agent"}
    assert hh_api._HeadHunterAPI__params == {"text": "", "page": 0, "per_page": 10}
    assert hh_api._HeadHunterAPI__vacancies == []


@pytest.mark.parametrize(
    "status_code, response_data, expected, exception",
    [
        # Успешный запрос
        (200, {"items": [{"id": 1}, {"id": 2}]}, [{"id": 1}, {"id": 2}], None),
        # Ошибка HTTP
        (404, None, [], None),
        # Ошибка сети
        (200, None, [], requests.exceptions.RequestException),
        # Ошибка JSON
        (200, "invalid_json", [], json.JSONDecodeError),
        # Отсутствие ключа items
        (200, {"data": []}, [], KeyError),
    ],
)
def test_get_vacancies_by_api(hh_api, status_code, response_data, expected, exception, mocker, capsys):
    """Тестирование различных сценариев __get_vacancies_by_api"""
    mock_connect = mocker.patch.object(hh_api, "connect_to_api")

    if exception == requests.exceptions.RequestException:
        mock_connect.side_effect = exception("Connection error")
    else:
        mock_response = mocker.Mock()
        mock_response.status_code = status_code

        if status_code == 200:
            if exception == json.JSONDecodeError:
                mock_response.json.side_effect = json.JSONDecodeError("Error", "doc", 0)
            else:
                mock_response.json.return_value = response_data
        else:
            mock_response.json.side_effect = Exception("JSON should not be called for non-200 status")

        mock_connect.return_value = mock_response

    result = hh_api._HeadHunterAPI__get_vacancies_by_api()

    assert result == expected

    if status_code != 200 and status_code is not None:
        captured = capsys.readouterr()
        assert f"Ошибка API: статус {status_code}" in captured.out
    elif exception == requests.exceptions.RequestException:
        captured = capsys.readouterr()
        assert "Ошибка при запросе к API hh.ru" in captured.out
    elif exception in (json.JSONDecodeError, KeyError):
        captured = capsys.readouterr()
        assert "Ошибка обработки ответа API" in captured.out


def test_keyword_setting(hh_api):
    """Проверка установки ключевого слова"""
    hh_api.get_vacancies("python")
    assert hh_api._HeadHunterAPI__params["text"] == "python"
