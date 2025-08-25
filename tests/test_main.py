from unittest.mock import patch

from src.main import user_interaction


def test_user_interaction_keywords(mock_manager, capsys):
    """Тестирование выбора фильтрации по ключевым словам"""
    with patch("builtins.input", return_value="1"), patch("src.main.filtration_by_keywords") as mock_filter:
        user_interaction(mock_manager)

        # Проверяем, что функция фильтрации была вызвана
        mock_filter.assert_called_once_with(mock_manager)

        # Проверяем вывод меню
        captured = capsys.readouterr()
        assert "Доступные команды фильтрации:" in captured.out
        assert "1. По ключевым словам" in captured.out


def test_user_interaction_min_salary(mock_manager, capsys):
    """Тестирование выбора фильтрации по минимальной зарплате"""
    with patch("builtins.input", return_value="2"), patch("src.main.filtration_by_min_salary") as mock_filter:
        user_interaction(mock_manager)

        # Проверяем, что функция фильтрации была вызвана
        mock_filter.assert_called_once_with(mock_manager)


def test_user_interaction_experience(mock_manager, capsys):
    """Тестирование выбора фильтрации по опыту работы"""
    with patch("builtins.input", return_value="3"), patch("src.main.filtration_by_experience") as mock_filter:
        user_interaction(mock_manager)

        # Проверяем, что функция фильтрации была вызвана
        mock_filter.assert_called_once_with(mock_manager)


def test_user_interaction_salary(mock_manager, capsys):
    """Тестирование выбора фильтрации по зарплате"""
    with patch("builtins.input", return_value="4"), patch("src.main.filtration_by_salary") as mock_filter:
        user_interaction(mock_manager)

        # Проверяем, что функция фильтрации была вызвана
        mock_filter.assert_called_once_with(mock_manager)


def test_user_interaction_invalid_choice(mock_manager, capsys):
    """Тестирование обработки неверного выбора"""
    with patch("builtins.input", return_value="5"):
        user_interaction(mock_manager)

        # Проверяем вывод сообщения об ошибке
        captured = capsys.readouterr()
        assert "Неверный выбор" in captured.out
