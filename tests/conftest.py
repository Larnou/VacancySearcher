from unittest.mock import Mock

import pytest

from src.classes.headhunter_api import HeadHunterAPI
from src.classes.rates_api import RatesAPI
from src.classes.vacancy import Vacancy
from src.classes.vacancy_manager import VacancyManager


# Фикстура для создания экземпляра API
@pytest.fixture
def hh_api():
    return HeadHunterAPI()


# Фикстура для мока requests.get
@pytest.fixture
def mock_requests_get_hhapi(mocker):
    return mocker.patch("src.classes.headhunter_api.requests.get")


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

@pytest.fixture
def vacancy_manager():
    return VacancyManager()

@pytest.fixture
def mock_vacancy():
    """Создает мок-объект вакансии"""
    vacancy = Mock(spec=Vacancy)
    vacancy.alternate_url = "https://example.com/vacancy/1"
    vacancy.name = "Python Developer"
    vacancy.requirement = "Python, Django, Flask"
    vacancy.employer = "TechCorp"
    vacancy.experience = "1-3 years"
    vacancy.avg_salary = 150000
    vacancy.to_dict.return_value = {
        "name": "Python Developer",
        "salary": {"from": 100000, "to": 200000, "currency": "RUB"},
        "has_test": True,
        "experience": "1-3 years",
        "requirement": "Python, Django, Flask",
        "employer": "TechCorp",
        "alternate_url": "https://example.com/vacancy/1"
    }
    return vacancy

@pytest.fixture
def mock_vacancy2():
    """Создает второй мок-объект вакансии"""
    vacancy = Mock(spec=Vacancy)
    vacancy.alternate_url = "https://example.com/vacancy/2"
    vacancy.name = "Data Scientist"
    vacancy.requirement = "Python, Machine Learning"
    vacancy.employer = "DataPro"
    vacancy.experience = "3+ years"
    vacancy.avg_salary = 200000
    vacancy.to_dict.return_value = {
        "name": "Data Scientist",
        "salary": {"from": 150000, "to": 250000, "currency": "RUB"},
        "has_test": False,
        "experience": "3+ years",
        "requirement": "Python, Machine Learning",
        "employer": "DataPro",
        "alternate_url": "https://example.com/vacancy/2"
    }
    return vacancy


@pytest.fixture
def mock_manager():
    """Создает мок-объект менеджера вакансий"""
    manager = Mock(spec=VacancyManager)
    return manager

@pytest.fixture
def mock_vacancies():
    """Создает список мок-объектов вакансий"""
    vacancies = []
    for i in range(3):
        vacancy = Mock(spec=Vacancy)
        vacancy.__str__ = Mock(return_value=f"Вакансия {i+1}")
        vacancies.append(vacancy)
    return vacancies


@pytest.fixture
def mock_apis():
    """Создает мок-объекты API"""
    hh_api = Mock(spec=HeadHunterAPI)
    rates_api = Mock(spec=RatesAPI)
    return hh_api, rates_api