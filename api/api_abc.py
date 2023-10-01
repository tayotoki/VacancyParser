from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, TypedDict, Any

import requests


class Request(TypedDict):
    url: Optional[str]
    headers: Optional[dict[str, Any]]
    params: Optional[dict[str, Any]]


class VacancySchema(TypedDict):
    id: str | int
    name: str
    area: dict[str, str | int]
    salary: dict[str, int | float | str]
    employer: dict[str, int | str]
    description: dict[str, str] | str
    published_at: str  # ISO 8601


class API(ABC):
    API_URI: str
    SEARCH_GET_PARAMETER: str
    API_SECRET: Optional[str] = None
    HEADER_FOR_SECRET: Optional[str] = None

    def get_vacancies(self, search_term: str) -> list[VacancySchema]:
        params = {
            self.SEARCH_GET_PARAMETER: search_term
        }
        raw_data = self.request_method_get(params=params)
        return self._parse_raw(raw_data)

    @abstractmethod
    def _parse_raw(self, data: dict) -> list[VacancySchema]:
        pass

    def request_method_get(
            self,
            url: Optional[str] = None,
            headers: Optional[dict[str, Any]] = None,
            params: Optional[dict[str, Any]] = None
    ) -> dict[str, int | str | list[dict]]:

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
        pass
