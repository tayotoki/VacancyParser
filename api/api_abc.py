from abc import ABC, abstractmethod
from typing import Optional, TypedDict, Any

import requests


class Request(TypedDict):
    """Структура HTTP-запроса"""
    url: Optional[str]
    headers: Optional[dict[str, Any]]
    params: Optional[dict[str, Any]]


class VacancySchema(TypedDict):
    """Структура словаря, который должен
    возвращать объект конкретного API"""
    id: str | int
    name: str
    area: str
    salary: dict[str, int | float | str]
    employer: dict[str, int | str]
    description: dict[str, str] | str
    published_at: str  # ISO 8601


class API(ABC):
    """Абстрактный класс для работы с API.
    Содержит классовые атрибуты:
    API_URI - строка с URI конкретного API;
    SEARCH_GET_PARAMETER - строка с GET-параметром для поиска;
    API_SECRET - строка с секретным ключом вашего приложения;
    HEADER_FOR_SECRET - заголовок запроса для передачи секретного ключа."""
    API_URI: str
    SEARCH_GET_PARAMETER: str
    API_SECRET: Optional[str] = None
    HEADER_FOR_SECRET: Optional[str] = None

    def get_vacancies(self, search_term: str) -> list[VacancySchema]:
        """
        Метод для получения вакансий из API.
        :param search_term: строка с поисковым запросом.
        :type search_term: str
        :return: список объектов вакансий в соответствии со структурой VacancySchema
        :rtype: list[VacancySchema]
        """
        params = {
            self.SEARCH_GET_PARAMETER: search_term
        }
        raw_data = self.request_method_get(params=params)
        return self._parse_raw(raw_data)

    @abstractmethod
    def _parse_raw(self, data: dict) -> list[VacancySchema]:
        """
        Абстрактный метод для парсинга данных из ответа API
        согласно структуре ответа конкретного API.
        Должен быть переопределен дочерними классами.
        :param data: сырые данные ответа API
        :type data: dict
        """
        pass

    def request_method_get(
            self,
            url: Optional[str] = None,
            headers: Optional[dict[str, Any]] = None,
            params: Optional[dict[str, Any]] = None
    ) -> dict[str, int | str | list[dict]]:
        """
        Метод для совершения HTTP GET-запроса.
        Переданные аргументы объединяются с property
        default_request_payload или переопределяют тело запроса
        по умолчанию в случае совпадения ключей в заголовке[headers] или
        параметрах[params]. Если никакие аргументы не были переданы
        используется стандартная структура запроса - default_request_payload.
        :param url: адрес, на который нужно отправить запрос.
        :type url: str
        :param headers: заголовки, используемые в запросе (например для передачи
            секретных ключей)
        :type headers: Optional[dict[str, Any]]
        :param params: параметры get-запроса.
        :type params: Optional[dict[str, Any]]
        :return: сырые данные ответа API.
        :rtype: dict
        """
        if headers:
            headers = self.default_request_payload["headers"] | headers
        if params:
            params = self.default_request_payload["params"] | params

        with requests.Session() as session:
            response: requests.Response = session.get(
                url=self.API_URI + (url or self.default_request_payload["url"]),
                headers=(headers or self.default_request_payload["headers"]),
                params=(params or self.default_request_payload["params"])
            )

            if response.status_code == 200:
                data: dict[str, int | str | list[dict]] = response.json()

                return data

    @property
    @abstractmethod
    def default_request_payload(self) -> Request:
        """
        Стандартная структура запроса под конкретное API.
        Должна соответствовать Request.
        """
        pass
