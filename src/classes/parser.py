from abc import ABC, abstractmethod


class Parser(ABC):
    """
    Класс Parser, обеспечивает требования к реализации методов для подключения к API.
    """

    @abstractmethod
    def get_vacancies_by_api(self) -> list[dict]:
        """
        Получает список вакансий через подключение к HH Api.

        Returns:
            Список вакансий
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword) -> list[dict]:
        """
        Получение вакансий по заданному ключевому слову keyword.

        Args:
            keyword: Ключевое слово, по которому будет проводиться поиск вакансий.
        Returns:
            Список вакансий, содержащих ключевое слово.
        """
        pass
