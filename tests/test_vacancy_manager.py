from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.classes.vacancy import Vacancy


def test_vacancy_manager_initialization(vacancy_manager):
    """Тестирование инициализации менеджера вакансий"""
    assert vacancy_manager.vacancies == {}
    assert isinstance(vacancy_manager.vacancies, dict)


def test_add_vacancy_success(vacancy_manager, mock_vacancy):
    """Тестирование успешного добавления вакансии"""
    vacancy_manager.add_vacancy(mock_vacancy)
    assert len(vacancy_manager.vacancies) == 1
    assert mock_vacancy.alternate_url in vacancy_manager.vacancies
    assert vacancy_manager.vacancies[mock_vacancy.alternate_url] == mock_vacancy


def test_add_duplicate_vacancy(vacancy_manager, mock_vacancy):
    """Тестирование попытки добавления дубликата вакансии"""
    vacancy_manager.add_vacancy(mock_vacancy)

    with pytest.raises(ValueError, match="Эта вакансия уже добавлена в список!"):
        vacancy_manager.add_vacancy(mock_vacancy)

    assert len(vacancy_manager.vacancies) == 1


def test_add_list_of_vacancies(vacancy_manager, mock_vacancy, mock_vacancy2):
    """Тестирование добавления списка вакансий"""
    vacancies_list = [mock_vacancy, mock_vacancy2]

    vacancy_manager.add_list_of_vacancies(vacancies_list)

    assert len(vacancy_manager.vacancies) == 2
    assert mock_vacancy.alternate_url in vacancy_manager.vacancies
    assert mock_vacancy2.alternate_url in vacancy_manager.vacancies


def test_get_vacancies_without_printing(vacancy_manager, mock_vacancy, mock_vacancy2):
    """Тестирование получения вакансий без вывода в консоль"""
    vacancy_manager.add_vacancy(mock_vacancy)
    vacancy_manager.add_vacancy(mock_vacancy2)

    vacancies = vacancy_manager.get_vacancies(print_vacancies=False)

    assert len(list(vacancies)) == 2
    assert mock_vacancy in vacancies
    assert mock_vacancy2 in vacancies


def test_delete_vacancy_success(vacancy_manager, mock_vacancy):
    """Тестирование успешного удаления вакансии"""
    vacancy_manager.add_vacancy(mock_vacancy)
    assert len(vacancy_manager.vacancies) == 1

    result = vacancy_manager.delete_vacancy(mock_vacancy)

    assert result is True
    assert len(vacancy_manager.vacancies) == 0


def test_delete_nonexistent_vacancy(vacancy_manager, mock_vacancy):
    """Тестирование удаления несуществующей вакансии"""
    result = vacancy_manager.delete_vacancy(mock_vacancy)

    assert result is False
    assert len(vacancy_manager.vacancies) == 0


@patch("builtins.open")
def test_load_from_json_file_not_found(mock_open, vacancy_manager, capsys):
    """Тестирование загрузки из несуществующего JSON-файла"""
    mock_open.side_effect = FileNotFoundError("File not found")

    result = vacancy_manager.load_from_json("nonexistent.json")

    assert result == []

    # Проверяем, что ошибка была выведена
    captured = capsys.readouterr()
    assert "File not found" in captured.out


def test_filter_by_keywords(vacancy_manager, mock_vacancy, mock_vacancy2):
    """Тестирование фильтрации по ключевым словам"""
    vacancy_manager.add_vacancy(mock_vacancy)
    vacancy_manager.add_vacancy(mock_vacancy2)

    # Фильтрация по слову "Python" (должны найтись обе вакансии)
    result = vacancy_manager.filter_by_keywords("Python")
    assert len(result) == 2

    # Фильтрация по слову "Django" (должна найтись только первая вакансия)
    result = vacancy_manager.filter_by_keywords("Django")
    assert len(result) == 1
    assert result[0] == mock_vacancy

    # Фильтрация по слову "Machine" (должна найтись только вторая вакансия)
    result = vacancy_manager.filter_by_keywords("Machine")
    assert len(result) == 1
    assert result[0] == mock_vacancy2

    # Фильтрация по нескольким словам
    result = vacancy_manager.filter_by_keywords("Python Data")
    assert len(result) == 1
    assert result[0] == mock_vacancy2


def test_filter_by_min_salary(vacancy_manager, mock_vacancy, mock_vacancy2):
    """Тестирование фильтрации по минимальной зарплате"""
    vacancy_manager.add_vacancy(mock_vacancy)  # avg_salary = 150000
    vacancy_manager.add_vacancy(mock_vacancy2)  # avg_salary = 200000

    # Фильтрация по минимальной зарплате 100000 (обе вакансии)
    result = vacancy_manager.filter_by_min_salary(100000)
    assert len(result) == 2

    # Фильтрация по минимальной зарплате 160000 (только вторая вакансия)
    result = vacancy_manager.filter_by_min_salary(160000)
    assert len(result) == 1
    assert result[0] == mock_vacancy2

    # Фильтрация по минимальной зарплате 250000 (нет вакансий)
    result = vacancy_manager.filter_by_min_salary(250000)
    assert len(result) == 0


def test_filter_by_experience(vacancy_manager, mock_vacancy, mock_vacancy2):
    """Тестирование фильтрации по опыту работы"""
    vacancy_manager.add_vacancy(mock_vacancy)  # experience = "1-3 years"
    vacancy_manager.add_vacancy(mock_vacancy2)  # experience = "3+ years"

    # Фильтрация по опыту "1-3 years"
    result = vacancy_manager.filter_by_experience("1-3 years")
    assert len(result) == 1
    assert result[0] == mock_vacancy

    # Фильтрация по опыту "3+ years"
    result = vacancy_manager.filter_by_experience("3+ years")
    assert len(result) == 1
    assert result[0] == mock_vacancy2

    # Фильтрация по несуществующему опыту
    result = vacancy_manager.filter_by_experience("5+ years")
    assert len(result) == 0


def test_filter_by_salary(vacancy_manager, mock_vacancy, mock_vacancy2):
    """Тестирование фильтрации по зарплате (только с указанной зарплатой)"""
    # Создаем вакансию без зарплаты
    vacancy_no_salary = Mock(spec=Vacancy)
    vacancy_no_salary.alternate_url = "https://example.com/vacancy/3"
    vacancy_no_salary.name = "Intern"
    vacancy_no_salary.avg_salary = 0

    vacancy_manager.add_vacancy(mock_vacancy)  # avg_salary = 150000
    vacancy_manager.add_vacancy(mock_vacancy2)  # avg_salary = 200000
    vacancy_manager.add_vacancy(vacancy_no_salary)  # avg_salary = 0

    # Фильтрация по зарплате 100000 (обе вакансии с зарплатой)
    result = vacancy_manager.filter_by_salary(100000)
    assert len(result) == 2

    # Фильтрация по зарплате 160000 (только вторая вакансия)
    result = vacancy_manager.filter_by_salary(160000)
    assert len(result) == 1
    assert result[0] == mock_vacancy2

    # Фильтрация по зарплате 250000 (нет вакансий)
    result = vacancy_manager.filter_by_salary(250000)
    assert len(result) == 0