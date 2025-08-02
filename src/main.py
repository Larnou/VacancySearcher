import requests
from cbrf.asyncio import DailyCurrenciesRates

from src.classes.headhunterapi import HeadHunterAPI
from src.classes.ratesapi import RatesAPI
from src.classes.vacancy import Vacancy

# Та самая точка входа в работу программы
# Создание экземпляра класса для работы с API сайтов с вакансиями и курса валют
hh_api = HeadHunterAPI()
rates_api = RatesAPI()

# Получение вакансий с hh.ru в формате JSON
hh_vacancies = hh_api.get_vacancies("Python")
rates_dict = rates_api.get_rates_by_api()

for i, vacancy in enumerate(hh_vacancies, 1):
    vacancy = Vacancy(
        vacancy["name"],
        vacancy["salary"],
        vacancy["employer"]["name"],
        vacancy["snippet"]["requirement"],
        vacancy["experience"]["name"],
        vacancy["has_test"],
        vacancy["alternate_url"],
        rates_dict,
    )

    print(i)
    print(vacancy)

print("\n\n\n")


# Преобразование набора данных из JSON в список объектов
vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)


# Сохранение информации о вакансиях в файл
json_saver = JSONSaver()
json_saver.add_vacancy(vacancy)
json_saver.delete_vacancy(vacancy)


# Функция для взаимодействия с пользователем
def user_interaction():
    platforms = ["HeadHunter"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
