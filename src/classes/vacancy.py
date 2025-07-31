
# Создать класс для работы с вакансиями. В этом классе самостоятельно определить атрибуты,
# такие как название вакансии, ссылка на вакансию, зарплата, краткое описание или требования и т. п.
# (всего не менее четырех атрибутов). Класс должен поддерживать методы сравнения вакансий между собой
# по зарплате и валидировать данные, которыми инициализируются его атрибуты.

class Vacancy:
    """
    Класс Vacancy, позволяет хранить информацию о вакансии в удобном виде.
    Обеспечивает возможность сравнения вакансий по средней зарабной плате.
    """

    __slots__ = ("name", "salary", "has_test", "experience", "requirement", "employer", "alternate_url", "avg_salary")

    def __init__(self,
                 name: str,
                 salary: None | dict,
                 employer: str,
                 requirement: str,
                 experience: str,
                 has_test: bool,
                 alternate_url: str
                 ) -> None:
        """
        Создаёт объект Vacancy.
        """

        # Валидация данных
        if not name:
            raise ValueError("Название вакансии не может быть пустым")

        if not requirement:
            raise ValueError("Описание вакансии не может быть пустым")

        if not alternate_url.startswith("http"):
            raise ValueError("Некорректный URL вакансии")

        self.name = name
        self.salary = salary
        self.avg_salary = self.calculate_avg_salary()
        self.requirement = self.remove_from_requirement(requirement)
        self.has_test = has_test
        self.experience = experience
        self.employer = employer
        self.alternate_url = alternate_url

    @staticmethod
    def remove_from_requirement(requirement: str) -> str:
        """
        Очистка строки требований от HTML тегов после обращения к API.

        Args:
            requirement: Ключевое слово, по которому будет проводиться поиск вакансий.
        Returns:
            Строка требований.
        """
        new_requirement = requirement.replace("<highlighttext>", "")
        new_requirement = new_requirement.replace("</highlighttext>", "")
        return new_requirement

    def calculate_avg_salary(self) -> float:
        """Рассчитывает среднюю зарплату для сравнений"""
        salary_from = self.salary.get('from', 0) or 0
        salary_to = self.salary.get('to', 0) or 0

        # Если указаны обе границы
        if salary_from and salary_to:
            return (salary_from + salary_to) / 2

        # Если указана только одна граница
        return salary_from or salary_to or 0


    def get_salary_info(self) -> str:
        """
            Возвращает форматированную информацию о зарплате.

            Returns:
                Форматированная информация о зарплате.
        """

        if not self.salary:
            return "Не указана"

        salary_from = self.salary.get('from', '')
        salary_to = self.salary.get('to', '')
        currency = self.salary.get('currency', '')

        # Обработка различных вариантов
        if salary_from and salary_to and salary_from != salary_to:
            return f"{salary_from} - {salary_to} {currency}"
        if salary_from:
            return f"от {salary_from} {currency}"
        if salary_to:
            return f"до {salary_to} {currency}"
        return "Не указана"


    def __str__(self) -> str:
        """
            Строковое представление вакансии: Вакансия, Зарплата, Компания,
            Требования, Опыт работы, Тестовое задание, Ссылка


            Returns:
                Строковое представление вакансии.
        """
        salary_info = self.get_salary_info()
        has_test_info = 'Есть' if self.has_test else 'Нет'

        return (
            f"Вакансия: {self.name}\n"
            f"Зарплата: {salary_info}\n"
            f"Компания: {self.employer[:100]}\n"
            f"Требования: {self.requirement[:140]}\n"
            f"Опыт работы: {self.experience}\n"
            f"Тестовое задание: {has_test_info}\n"
            f"Ссылка: {self.alternate_url}\n"
        )

    # Методы сравнения по средней зарплате
    # Если зп в разных валютах, надо перевести к рублям и сравнить
    def __eq__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return False
        return self.avg_salary == other.avg_salary

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только объекты Vacancy")
        return self.avg_salary < other.avg_salary

    def __le__(self, other) -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только объекты Vacancy")
        return self.avg_salary > other.avg_salary

    def __ge__(self, other) -> bool:
        return self.__gt__(other) or self.__eq__(other)





    def cast_to_object_list(self):
        pass
