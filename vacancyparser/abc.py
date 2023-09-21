from abc import ABC, abstractmethod
from typing import Optional

import requests

from credentials import superjob


class API(ABC):
    API_URI: str
    SEARCH_GET_PARAMETER: str
    API_SECRET: Optional[str] = None
    HEADER_FOR_SECRET: Optional[str] = None

    @abstractmethod
    def get_vacancies(self, search_term: str):
        ...

    def request_method_get(self, *, search_term: str, url: str = "/vacancies") -> dict[str, int | str | list[dict]]:
        with requests.Session() as session:
            response: requests.Response = session.get(
                url=f"{self.API_URI[:-1] if self.API_URI.endswith('/') else self.API_URI}"
                    f"{url if url.endswith('/') else url + '/'}",
                headers={
                    self.HEADER_FOR_SECRET: self.API_SECRET
                } if self.HEADER_FOR_SECRET else None,
                params={
                    self.SEARCH_GET_PARAMETER: search_term
                }
            )

            if response.status_code == 200:
                data: dict[str, int | str | list[dict]] = response.json()

                return data

    @property
    def __name__(self):
        return self.__class__.__name__.lower().replace("api", "")


class HeadHunterAPI(API):
    API_URI = "https://api.hh.ru"
    SEARCH_GET_PARAMETER = "text"

    def get_vacancies(self, search_term: str) -> list[dict]:
        return self.request_method_get(search_term=search_term).get("items")


class SuperJobAPI(API):
    API_URI = "https://api.superjob.ru/2.0"
    API_SECRET = superjob.SECRET_KEY
    HEADER_FOR_SECRET = "X-Api-App-Id"
    SEARCH_GET_PARAMETER = "keyword"

    def get_vacancies(self, search_term: str) -> list[dict]:
        return self.request_method_get(search_term=search_term).get("objects")


if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    sj_api = SuperJobAPI()

    search_term = "Python junior"

    print(hh_api.get_vacancies(search_term=search_term))
    print("_____________________________")
    print(sj_api.get_vacancies(search_term=search_term))
