import json

import pytest
import requests
from requests import RequestException


@pytest.mark.parametrize(
    "status_code, response_data, expected, exception",
    [
        # Успешный запрос
        (
            200,
            {"Valute": {"USD": {"Value": 75.5, "Nominal": 1}, "EUR": {"Value": 90.0, "Nominal": 1}}},
            {"USD": {"Value": 75.5, "Nominal": 1}, "EUR": {"Value": 90.0, "Nominal": 1}},
            None,
        ),
        # Ошибка HTTP
        (404, None, {}, None),
        # Ошибка сети
        (200, None, {}, RequestException),
        # Ошибка JSON
        (200, "invalid_json", {}, json.JSONDecodeError),
    ],
)
def test_get_rates_by_api(rates_api, mocker, status_code, response_data, expected, exception):
    """Тестирование различных сценариев получения курсов валют"""
    # Мокаем requests.get
    mock_get = mocker.patch("src.classes.rates_api.requests.get")

    if exception == RequestException:
        mock_get.side_effect = RequestException("Connection error")
    else:
        mock_response = mock_get.return_value
        mock_response.status_code = status_code

        if exception == json.JSONDecodeError:
            mock_response.json.side_effect = json.JSONDecodeError("Error", "doc", 0)
        else:
            mock_response.json.return_value = response_data

    # Вызов тестируемого метода
    result = rates_api.get_rates_by_api()

    # Проверка результата
    assert result == expected


@pytest.mark.parametrize(
    "currency_code, rate_dict, expected",
    [
        # Стандартный курс (1 единица)
        ("USD", {"USD": {"Value": 75.5, "Nominal": 1}}, 75.5),
        # Курс для номинала 10 единиц
        ("JPY", {"JPY": {"Value": 50.0, "Nominal": 10}}, 5.0),
        # Курс для номинала 100 единиц
        ("HUF", {"HUF": {"Value": 20.0, "Nominal": 100}}, 0.2),
        # Дробный курс
        ("EUR", {"EUR": {"Value": 89.99, "Nominal": 1}}, 89.99),
    ],
)
def test_get_currency_rate_success(rates_api, currency_code, rate_dict, expected):
    """Тестирование корректного расчета курса валют"""
    result = rates_api.get_currency_rate(currency_code, rate_dict)
    assert result == pytest.approx(expected)


def test_get_currency_rate_missing_currency(rates_api):
    """Тестирование обработки отсутствующей валюты"""
    rate_dict = {"USD": {"Value": 75.5, "Nominal": 1}}

    with pytest.raises(KeyError):
        rates_api.get_currency_rate("EUR", rate_dict)


# Проверка доступности API
def is_api_available():
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=5)
        return response.status_code == 200
    except RequestException:
        return False


# Интеграционный тест (реальный API вызов) с проверкой доступности
def test_real_api_response(rates_api):
    """Тестирование структуры реального ответа API"""
    if not is_api_available():
        pytest.skip("API is not available, skipping integration test")

    rates = rates_api.get_rates_by_api()

    assert "USD" in rates
    assert "EUR" in rates

    # Проверка структуры данных
    usd = rates["USD"]
    assert "Value" in usd
    assert "Nominal" in usd

    # Проверка расчета курса
    usd_rate = rates_api.get_currency_rate("USD", rates)
    assert isinstance(usd_rate, float)
    assert usd_rate > 0


def test_api_url(rates_api, mocker):
    """Проверка URL API вызова"""
    mock_get = mocker.patch("src.classes.rates_api.requests.get")
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"Valute": {}}

    rates_api.get_rates_by_api()

    # Проверка URL вызова
    mock_get.assert_called_once_with("https://www.cbr-xml-daily.ru/daily_json.js")
