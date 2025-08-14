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
            raise ValueError("Эта вакансия уже добавлена в список!")

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
                print("\n")
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

    def save_to_json(self, vacancies_list: list[Vacancy], filename: str, home_directiry: str = None):
        if home_directiry is None:
            current_file = Path(__file__).resolve()
            BASE_DIR = current_file.parent.parent.parent
            DATA_PATH = BASE_DIR / "data" / filename
        else:
            current_file = Path(__file__).resolve()
            base_dir = current_file.parent.parent.parent
            DATA_PATH = base_dir / home_directiry / filename

        data = [vacancy.to_dict() for vacancy in vacancies_list]
        json_data = {"found": len(vacancies_list), "items": data}
        # Создаем директорию, если её нет
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Сохраняем в файл с форматированием
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

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

            return data["items"]
        except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError, PermissionError, IsADirectoryError) as e:
            print(e)
            return []

    def filter_by_keywords(self, keywords: str):
        search_words = [word.strip().lower() for word in keywords.split(" ")]
        return [
            v
            for v in self.vacancies.values()
            if all(word in f"{v.name} {v.requirement} {v.employer}".lower() for word in search_words)
        ]

    def filter_by_min_salary(self, min_salary: float):
        return [v for v in self.vacancies.values() if v.avg_salary == 0 or v.avg_salary >= min_salary]

    def filter_by_experience(self, experience: str):
        return [v for v in self.vacancies.values() if v.experience == experience]

    def filter_by_salary(self, salary: float):
        return [v for v in self.vacancies.values() if v.avg_salary > 0 and v.avg_salary >= salary]
