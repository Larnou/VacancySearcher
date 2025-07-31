from abc import ABC, abstractmethod


class Parser(ABC):

    @abstractmethod
    def get_vacancies_by_api(self):
        pass

    @abstractmethod
    def get_vacancies(self, keyword) -> list[dict]:
        pass