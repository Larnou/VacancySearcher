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


    def load_from_file(self, json_file):
        pass

    def save_to_file(self, json_file):
        pass

