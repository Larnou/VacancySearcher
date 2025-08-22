from unittest.mock import patch

from src.utils import followup_actions, filtration_by_experience, filtration_by_min_salary, filtration_by_keywords


def test_followup_actions_save_to_file(mock_manager, mock_vacancies, capsys):
    """Тестирование сохранения результатов в файл"""
    # Мокируем пользовательский ввод
    with patch('builtins.input', side_effect=['1', 'test_vacancies.json']):
        followup_actions(mock_manager, mock_vacancies)

    # Проверяем, что метод save_to_json был вызван с правильными параметрами
    mock_manager.save_to_json.assert_called_once_with(mock_vacancies, 'test_vacancies.json')

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "Выберите дальнейшие действие:" in captured.out
    assert "1. Сохранить результат в файл" in captured.out
    assert "2. Вывести результат в консоль" in captured.out


def test_followup_actions_print_to_console(mock_manager, mock_vacancies, capsys):
    """Тестирование вывода результатов в консоль"""
    # Мокируем пользовательский ввод
    with patch('builtins.input', return_value='2'):
        followup_actions(mock_manager, mock_vacancies)

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "Всего вакансий: 3" in captured.out
    # Проверяем, что каждая вакансия была напечатана
    for i in range(3):
        assert f"Вакансия {i + 1}" in captured.out

def test_filtration_by_experience(mock_manager, mock_vacancies, capsys):
    """Тестирование фильтрации по опыту работы"""
    # Настраиваем мок менеджера
    mock_manager.filter_by_experience.return_value = mock_vacancies

    # Мокируем пользовательский ввод и вызов followup_actions
    with patch('builtins.input', side_effect=['2']), \
            patch('src.utils.followup_actions') as mock_followup:
        filtration_by_experience(mock_manager)

    # Проверяем, что метод фильтрации был вызван с правильными параметрами
    mock_manager.filter_by_experience.assert_called_once_with('От 1 года до 3 лет')

    # Проверяем, что followup_actions была вызвана с отфильтрованными вакансиями
    mock_followup.assert_called_once_with(mock_manager, mock_vacancies)

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "Выберите соотвествующий опыт:" in captured.out
    assert "1. Нет опыта" in captured.out
    assert "2. От 1 года до 3 лет" in captured.out
    assert "3. От 3 до 6 лет" in captured.out
    assert "4. Более 6 лет" in captured.out