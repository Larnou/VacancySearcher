import pytest
import requests

from src.classes.headhunter_api import HeadHunterAPI
from src.classes.ratesapi import RatesAPI
from src.classes.vacancy import Vacancy


# Фикстура для создания экземпляра API
@pytest.fixture
def hh_api():
    return HeadHunterAPI()


# Фикстура для мока requests.get
@pytest.fixture
def mock_requests_get_hhapi(mocker):
    return mocker.patch("src.classes.headhunterapi.requests.get")


# Фикстура для создания экземпляра API
@pytest.fixture
def rates_api():
    return RatesAPI()


# Фикстуры для создания тестовых объектов
@pytest.fixture
def sample_rates_dict():
    """Фикстура с тестовыми курсами валют"""
    return {
        "USD": {"Value": 75.0, "Nominal": 1},
        "EUR": {"Value": 85.0, "Nominal": 1},
        "JPY": {"Value": 0.65, "Nominal": 100},
    }


@pytest.fixture
def base_vacancy_data(sample_rates_dict):
    """Базовые данные для создания вакансии"""
    return {
        "name": "Python Developer",
        "salary": {"from": 1000, "to": 2000, "currency": "USD"},
        "employer": "TechCorp",
        "requirement": "<highlighttext>Python</highlighttext> experience required",
        "experience": "1-3 years",
        "has_test": True,
        "alternate_url": "https://example.com/vacancy/123",
        "rates_dict": sample_rates_dict,
    }


@pytest.fixture
def vacancy_no_salary(sample_rates_dict):
    """Вакансия без указания зарплаты"""
    return Vacancy(
        name="Python Developer",
        salary=None,
        employer="TechCorp",
        requirement="Python experience",
        experience="1-3 years",
        has_test=True,
        alternate_url="https://example.com/vacancy/123",
        rates_dict=sample_rates_dict,
    )
