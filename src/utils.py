from src.classes.vacancy import Vacancy
from src.classes.vacancy_manager import VacancyManager


def followup_actions(manager: VacancyManager, vacancies: list[Vacancy]) -> None:
    """
    Дилоговые действия с пользователем о дальнейшем выборе после получения списка вакансий.

    Args:
        manager: Менеджер вакансий, в котором содержится список вакансий после работы API-сервисов.
        vacancies: Список вакансий полученный после фильтрации.
    """
    print("Выберите дальнейшие действие:")
    print("1. Сохранить результат в файл")
    print("2. Вывести результат в консоль")

    choice = input("\nВыберите дальнейшее действие (1 или 2): ").strip()

    if choice == "1":
        filename = input("Введите название файла: ")
        manager.save_to_json(vacancies, filename)

    if choice == "2":
        print(f"\nВсего вакансий: {len(vacancies)}")
        for i, vacancy in enumerate(vacancies):
            print(vacancy)


def filtration_by_keywords(manager: VacancyManager) -> None:
    """
    Фильтрация вакансий с использованием ключевых слов.

    Args:
        manager: Менеджер вакансий, в котором содержится список вакансий после работы API-сервисов.
    """
    keywords = input("\nВведите ключевые слова: ").strip()
    vacancies = manager.filter_by_keywords(keywords)
    followup_actions(manager, vacancies)


def filtration_by_min_salary(manager: VacancyManager) -> None:
    """
    Фильтрация вакансий по уровню минимальной зарплаты, среди всех вакансий (с учётом: Не указано).

    Args:
        manager: Менеджер вакансий, в котором содержится список вакансий после работы API-сервисов.
    """
    salary = float(input("\nМинимальная зарплата: "))
    vacancies = manager.filter_by_min_salary(salary)
    followup_actions(manager, vacancies)


def filtration_by_experience(manager: VacancyManager) -> None:
    """
    Фильтрация вакансий по наличию опыта.

    Args:
        manager: Менеджер вакансий, в котором содержится список вакансий после работы API-сервисов.
    """
    print("\nВыберите соотвествующий опыт: ")
    print("1. Нет опыта")
    print("2. От 1 года до 3 лет")
    print("3. От 3 до 6 лет")
    print("4. Более 6 лет")

    choice = input("\nВыберите подходящий вариант (1-4): ").strip()
    choice_variants = {"1": "Нет опыта", "2": "От 1 года до 3 лет", "3": "От 3 до 6 лет", "4": "Более 6 лет"}
    vacancies = manager.filter_by_experience(choice_variants[choice])
    followup_actions(manager, vacancies)


def filtration_by_salary(manager: VacancyManager) -> None:
    """
    Фильтрация вакансий по уровню минимальной зарплаты, среди вакансий с указанным уровнем зарботной платы.

    Args:
        manager: Менеджер вакансий, в котором содержится список вакансий после работы API-сервисов.
    """
    salary = float(input("\nМинимальная зарплата: "))
    vacancies = manager.filter_by_salary(salary)
    followup_actions(manager, vacancies)
