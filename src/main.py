

from src.classes.headhunter_api import HeadHunterAPI
from src.classes.ratesapi import RatesAPI
from src.classes.vacancy import Vacancy
from src.classes.vacancy_manager import VacancyManager

# Та самая точка входа в работу программы
# Создание экземпляра класса для работы с API сайтов с вакансиями и курса валют
hh_api = HeadHunterAPI()
rates_api = RatesAPI()

# Получение вакансий с hh.ru в формате JSON
hh_vacancies = hh_api.get_vacancies("Python")
rates_dict = rates_api.get_rates_by_api()

# Преобразование набора данных из JSON в список объектов
vacancies_list = Vacancy.cast_to_object_list(hh_vacancies, rates_dict)

print(vacancies_list)
for i, vacancy in enumerate(vacancies_list, 1):
    print(i)
    print(vacancy)
    print("\n")

# Сохранение информации о вакансиях в файл
vacancy = Vacancy(name="Similar", salary={"from": 100000, "to": 150000, "currency": "RUB"}, employer="Company", requirement="Desc",
        experience="1-3 years", has_test=True, alternate_url="https://example.com/similar", rates_dict={})
vacancy1 = Vacancy(name="Developer", salary={"from": 10000, "to": 150000, "currency": "RUB"}, employer="Company", requirement="Desc",
        experience="1-3 years", has_test=True, alternate_url="https://example.com/delepop", rates_dict={})

# VacancyManager init
json_saver = VacancyManager()

# add vacancy
json_saver.add_vacancy(vacancy)
json_saver.add_vacancy(vacancy1)

# check vacancies
vac = json_saver.get_vacancies()
print(vac)

json_saver.delete_vacancy(vacancy)
vac = json_saver.get_vacancies()
print(vac)


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
