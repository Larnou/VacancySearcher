import pytest

from src.classes.vacancy import Vacancy


def test_vacancy_initialization_validation():
    """Тестирование валидации при инициализации"""
    with pytest.raises(ValueError, match="Название вакансии не может быть пустым"):
        Vacancy(
            name="",
            salary=None,
            employer="Company",
            requirement="Desc",
            experience="Exp",
            has_test=True,
            alternate_url="https://example.com",
            rates_dict={},
        )

    with pytest.raises(ValueError, match="Описание вакансии не может быть пустым"):
        Vacancy(
            name="Developer",
            salary=None,
            employer="Company",
            requirement="",
            experience="Exp",
            has_test=True,
            alternate_url="https://example.com",
            rates_dict={},
        )

    with pytest.raises(ValueError, match="Некорректный URL вакансии"):
        Vacancy(
            name="Developer",
            salary=None,
            employer="Company",
            requirement="Desc",
            experience="Exp",
            has_test=True,
            alternate_url="invalid-url",
            rates_dict={},
        )


def test_set_salary_conversion(base_vacancy_data, sample_rates_dict):
    """Тестирование конвертации зарплаты в рубли"""
    # Тест конвертации USD
    vacancy = Vacancy(**base_vacancy_data)
    assert vacancy.salary == {"from": 75000, "to": 150000, "currency": "RUB"}

    # Тест конвертации EUR
    data = base_vacancy_data.copy()
    data["salary"]["currency"] = "EUR"
    vacancy_eur = Vacancy(**data)
    assert vacancy_eur.salary == {"from": 85000, "to": 170000, "currency": "RUB"}

    # Тест конвертации JPY (номинал 100)
    data = base_vacancy_data.copy()
    data["salary"] = {"from": 100000, "to": 200000, "currency": "JPY"}
    vacancy_jpy = Vacancy(**data)
    assert vacancy_jpy.salary == {"from": 650, "to": 1300, "currency": "RUB"}


def test_set_salary_no_conversion(base_vacancy_data):
    """Тестирование зарплаты без конвертации (RUB)"""
    data = base_vacancy_data.copy()
    data["salary"]["currency"] = "RUB"
    vacancy = Vacancy(**data)
    assert vacancy.salary == {"from": 1000, "to": 2000, "currency": "RUB"}


def test_set_salary_no_salary(base_vacancy_data):
    """Тестирование обработки отсутствия зарплаты"""
    data = base_vacancy_data.copy()
    data["salary"] = None
    vacancy = Vacancy(**data)
    assert vacancy.salary == {"from": 0, "to": 0, "currency": "RUB"}
    assert vacancy.avg_salary == 0


def test_remove_html_tags(base_vacancy_data):
    """Тестирование очистки HTML тегов из требований"""
    vacancy = Vacancy(**base_vacancy_data)
    assert vacancy.requirement == "Python experience required"


def test_calculate_avg_salary():
    """Тестирование расчета средней зарплаты"""
    # Зарплата указана "от" и "до"
    vacancy1 = Vacancy(
        name="Dev",
        salary={"from": 100000, "to": 200000, "currency": "RUB"},
        employer="Company",
        requirement="Desc",
        experience="Exp",
        has_test=True,
        alternate_url="https://example.com",
        rates_dict={},
    )
    assert vacancy1.avg_salary == 150000

    # Указана только зарплата "от"
    vacancy2 = Vacancy(
        name="Dev",
        salary={"from": 100000, "to": 0, "currency": "RUB"},
        employer="Company",
        requirement="Desc",
        experience="Exp",
        has_test=True,
        alternate_url="https://example.com",
        rates_dict={},
    )
    assert vacancy2.avg_salary == 100000

    # Указана только зарплата "до"
    vacancy3 = Vacancy(
        name="Dev",
        salary={"from": 0, "to": 200000, "currency": "RUB"},
        employer="Company",
        requirement="Desc",
        experience="Exp",
        has_test=True,
        alternate_url="https://example.com",
        rates_dict={},
    )
    assert vacancy3.avg_salary == 200000

    # Зарплата не указана
    vacancy4 = Vacancy(
        name="Dev",
        salary=None,
        employer="Company",
        requirement="Desc",
        experience="Exp",
        has_test=True,
        alternate_url="https://example.com",
        rates_dict={},
    )
    assert vacancy4.avg_salary == 0


def test_get_salary_info():
    """Тестирование форматирования информации о зарплате"""
    # Полный диапазон
    vacancy1 = Vacancy(
        name="Dev",
        salary={"from": 100000, "to": 200000, "currency": "RUB"},
        employer="Company",
        requirement="Desc",
        experience="Exp",
        has_test=True,
        alternate_url="https://example.com",
        rates_dict={},
    )
    assert vacancy1.get_salary_info() == "100000 - 200000 RUB"

    # Только "от"
    vacancy2 = Vacancy(
        name="Dev",
        salary={"from": 100000, "to": 0, "currency": "RUB"},
        employer="Company",
        requirement="Desc",
        experience="Exp",
        has_test=True,
        alternate_url="https://example.com",
        rates_dict={},
    )
    assert vacancy2.get_salary_info() == "от 100000 RUB"

    # Только "до"
    vacancy3 = Vacancy(
        name="Dev",
        salary={"from": 0, "to": 200000, "currency": "RUB"},
        employer="Company",
        requirement="Desc",
        experience="Exp",
        has_test=True,
        alternate_url="https://example.com",
        rates_dict={},
    )
    assert vacancy3.get_salary_info() == "до 200000 RUB"

    # Зарплата не указана
    vacancy4 = Vacancy(
        name="Dev",
        salary=None,
        employer="Company",
        requirement="Desc",
        experience="Exp",
        has_test=True,
        alternate_url="https://example.com",
        rates_dict={},
    )
    assert vacancy4.get_salary_info() == "Не указана"


def test_vacancy_str_representation(base_vacancy_data):
    """Тестирование строкового представления вакансии"""
    vacancy = Vacancy(**base_vacancy_data)
    result = str(vacancy)

    assert "Вакансия: Python Developer" in result
    assert "Зарплата: 75000 - 150000 RUB" in result
    assert "Компания: TechCorp" in result
    assert "Требования: Python experience required" in result
    assert "Опыт работы: 1-3 years" in result
    assert "Тестовое задание: Есть" in result
    assert "Ссылка: https://example.com/vacancy/123" in result


def test_vacancy_comparison():
    """Тестирование сравнения вакансий по зарплате"""
    vacancy_low = Vacancy(
        name="Junior",
        salary={"from": 50000, "to": 80000, "currency": "RUB"},
        employer="Company",
        requirement="Desc",
        experience="No exp",
        has_test=False,
        alternate_url="https://example.com/junior",
        rates_dict={},
    )

    vacancy_medium = Vacancy(
        name="Middle",
        salary={"from": 100000, "to": 150000, "currency": "RUB"},
        employer="Company",
        requirement="Desc",
        experience="1-3 years",
        has_test=True,
        alternate_url="https://example.com/middle",
        rates_dict={},
    )

    vacancy_high = Vacancy(
        name="Senior",
        salary={"from": 200000, "to": 300000, "currency": "RUB"},
        employer="Company",
        requirement="Desc",
        experience="3+ years",
        has_test=True,
        alternate_url="https://example.com/senior",
        rates_dict={},
    )

    # Проверка сравнения
    assert vacancy_low < vacancy_medium
    assert vacancy_medium < vacancy_high
    assert vacancy_high > vacancy_medium
    assert vacancy_medium > vacancy_low
    assert vacancy_medium <= vacancy_medium
    assert vacancy_medium >= vacancy_medium

    # Проверка равенства
    vacancy_same = Vacancy(
        name="Similar",
        salary={"from": 100000, "to": 150000, "currency": "RUB"},
        employer="Company",
        requirement="Desc",
        experience="1-3 years",
        has_test=True,
        alternate_url="https://example.com/similar",
        rates_dict={},
    )
    assert vacancy_medium == vacancy_same


def test_vacancy_comparison_with_missing_salary():
    """Тестирование сравнения вакансий без зарплаты"""
    vacancy_with_salary = Vacancy(
        name="With Salary",
        salary={"from": 100000, "to": 150000, "currency": "RUB"},
        employer="Company",
        requirement="Desc",
        experience="Exp",
        has_test=True,
        alternate_url="https://example.com/with",
        rates_dict={},
    )

    vacancy_no_salary = Vacancy(
        name="No Salary",
        salary=None,
        employer="Company",
        requirement="Desc",
        experience="Exp",
        has_test=True,
        alternate_url="https://example.com/without",
        rates_dict={},
    )

    print(vacancy_no_salary.avg_salary)

    # Попытка сравнения должна вызывать TypeError
    with pytest.raises(TypeError, match="Эти вакансии нельзя сравнить..."):
        vacancy_with_salary > vacancy_no_salary

    with pytest.raises(TypeError, match="Эти вакансии нельзя сравнить..."):
        vacancy_no_salary < vacancy_with_salary

    with pytest.raises(TypeError, match="Эти вакансии нельзя сравнить..."):
        vacancy_with_salary == vacancy_no_salary


def test_vacancy_comparison_with_non_vacancy():
    """Тестирование сравнения с объектами другого типа"""
    vacancy = Vacancy(
        name="Dev",
        salary={"from": 100000, "to": 150000, "currency": "RUB"},
        employer="Company",
        requirement="Desc",
        experience="Exp",
        has_test=True,
        alternate_url="https://example.com",
        rates_dict={},
    )

    with pytest.raises(TypeError, match="Можно сравнивать только объекты Vacancy"):
        vacancy > 100000

    with pytest.raises(TypeError, match="Можно сравнивать только объекты Vacancy"):
        vacancy == "developer"
