from abc import ABC, abstractmethod
from typing import Any

from src.classes.vacancy import Vacancy


class Repository(ABC):
    """
    Класс Repository, обеспечивает требования к реализации методов для работы со списком вакансий.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        """
        Добавление вакансии к списку вакансий менеджера.

        Args:
            vacancy: Вакансия, которая будет добавлена к списку менеджера.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy):
        """
        Удаляет выбранную вакансию из списка менеджера.

        Args:
            vacancy: Вакансия, которая будет удалена.
        Returns:
            True, если удаление прошло успешно, иначе False.
        """
        pass

    @staticmethod
    @abstractmethod
    def save_to_json(vacancies_list: list[Vacancy], filename: str, home_directiry: str = None):
        pass

    @staticmethod
    @abstractmethod
    def load_from_json(filename: str, home_directiry: str = None) -> list[Any] | Any:
        pass
