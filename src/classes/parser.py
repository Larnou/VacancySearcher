from abc import ABC, abstractmethod

import requests


class Parser(ABC):
    """
    Класс Parser, обеспечивает требования к реализации методов для подключения к API.
    """

    @abstractmethod
    def connect_to_api(self) -> requests.Response:
        """
        Подключение к HH Api.

        Returns:
            Response подключения API.
        """
        pass
