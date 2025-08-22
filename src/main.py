from src.classes.headhunter_api import HeadHunterAPI
from src.classes.rates_api import RatesAPI
from src.classes.vacancy import Vacancy
from src.classes.vacancy_manager import VacancyManager
from src.utils import filtration_by_experience, filtration_by_keywords, filtration_by_min_salary, filtration_by_salary


def user_interaction(manager: VacancyManager):
    """Функция для взаимодействия с пользователем"""
    print("\nДоступные команды фильтрации:")
    print("1. По ключевым словам")
    print("2. По минимальной зарплате")
    print("3. По опыту работы")
    print("4. Только с указанной зарплатой")

    choice = input("\nВыберите тип фильтра (1-4): ").strip()

    if choice == "1":
        filtration_by_keywords(manager)
        return None

    elif choice == "2":
        filtration_by_min_salary(manager)
        return None

    elif choice == "3":
        filtration_by_experience(manager)
        return None

    elif choice == "4":
        filtration_by_salary(manager)
        return None

    else:
        print("Неверный выбор")
        return None


if __name__ == "__main__":
    # Создание экземпляра класса для работы с API сайтов с вакансиями и курса валют
    hh_api = HeadHunterAPI()
    rates_api = RatesAPI()

    # Получение вакансий с hh.ru в формате JSON и курса валют для вычисления зарплат в рублях
    hh_vacancies = hh_api.get_vacancies("Python")
    rates_dict = rates_api.get_rates_by_api()

    # Загрузка набора данных из JSON в список объектов
    vacancy_manager = VacancyManager()
    vacancy_data = vacancy_manager.load_from_json("vacancies.json")
    vacancies = Vacancy.cast_to_object_list(vacancy_data, rates_dict)
    vacancy_manager.add_list_of_vacancies(vacancies)

    # Преобразование набора данных из JSON в список объектов
    # vacancies_list = Vacancy.cast_to_object_list(hh_vacancies, rates_dict)
    # vacancy_manager = VacancyManager()
    # vacancy_manager.add_list_of_vacancies(vacancies_list)
    # vacancy_manager.save_to_json('vacan.json')

    user_interaction(vacancy_manager)
