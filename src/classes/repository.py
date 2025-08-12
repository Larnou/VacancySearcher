from abc import ABC, abstractmethod

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


    @abstractmethod
    def save_to_file(self):
        pass


    @abstractmethod
    def load_from_file(self):
        pass
