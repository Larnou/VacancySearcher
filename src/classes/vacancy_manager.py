import json

from pathlib import Path
from typing import Any

from src.classes.repository import Repository
from src.classes.vacancy import Vacancy


class VacancyManager(Repository):
    """
    Класс VacancyManager, позволяет хранить, создавать, удалять и возвращать список вакансий типа Vacancy.
    Хранение реализовано через словарь с ключом по url вакансии.
    """
    def __init__(self):
        """
        Создаёт объект VacancyManager.
        """
        self.vacancies = {}

    def add_vacancy(self, vacancy: Vacancy):
        """
        Добавление вакансии к списку вакансий менеджера.

        Args:
            vacancy: Вакансия, которая будет добавлена к списку менеджера.
        """
        print(vacancy)
        url = vacancy.alternate_url
        if url not in self.vacancies:
            self.vacancies[url] = vacancy
        else:
            raise ValueError('Эта вакансия уже добавлена в список!')

    def add_list_of_vacancies(self, list_of_vacancies: list):
        """
        Добавление набора вакансий к списку вакансий менеджера.

        Args:
            list_of_vacancies: Набор вакансий, которая будет добавлена к списку менеджера.
        """
        for vacancy in list_of_vacancies:
            self.add_vacancy(vacancy)

    def get_vacancies(self, print_vacancies: bool = False):
        """
        Возвращает список вакансий, добавленных в менеджер.

        Args:
            print_vacancies: Если параметр True, то дополнительно будет выведен список вакансий в консоль.
        Returns:
            Список вакансий Vacancy.
        """
        if print_vacancies:
            for vacancy in self.vacancies.values():
                print(vacancy)
                print('\n')
        return self.vacancies.values()

    def delete_vacancy(self, vacancy: Vacancy):
        """
        Удаляет выбранную вакансию из списка менеджера.

        Args:
            vacancy: Вакансия, которая будет удалена.
        Returns:
            True, если удаление прошло успешно, иначе False.
        """
        url_index = vacancy.alternate_url
        try:
            del self.vacancies[url_index]
            return True
        except KeyError:
            return False


    def save_to_file(self, json_file):
        pass

    @staticmethod
    def load_from_json(filename: str, home_directiry: str = None) -> list[Any] | Any:
        """
        Чтение json-файла.
        Args:
            filename: Название файла.
            home_directiry: Директория хранения файлов.

        Returns: JSON-файл.
        """
        if home_directiry is None:
            current_file = Path(__file__).resolve()
            BASE_DIR = current_file.parent.parent.parent
            DATA_PATH = BASE_DIR / "data" / filename
        else:
            current_file = Path(__file__).resolve()
            base_dir = current_file.parent.parent.parent
            DATA_PATH = base_dir / home_directiry / filename

        try:
            with open(DATA_PATH, encoding="utf8") as f:
                data = json.load(f)

            return data['items']
        except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError, PermissionError, IsADirectoryError) as e:
            print(e)
            return []
