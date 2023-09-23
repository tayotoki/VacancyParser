from abc import ABC, abstractmethod
from typing import Optional

import requests


class API(ABC):
    API_URI: str
    SEARCH_GET_PARAMETER: str
    API_SECRET: Optional[str] = None
    HEADER_FOR_SECRET: Optional[str] = None

    extra_filters: list[str] = []

    @abstractmethod
    def get_vacancies(self, search_term: str, **extra_filters):
        ...

    def request_method_get(
            self,
            *,
            search_term: str,
            url: str = "/vacancies",
            params: Optional[dict[str, str]] = None,
            **extra_filters
    ) -> dict[str, int | str | list[dict]]:

        with requests.Session() as session:
            response: requests.Response = session.get(
                url=f"{self.request_payload['url']}"
                    f"{url if url.endswith('/') else url + '/'}",
                headers=self.request_payload["headers"],
                params={
                    self.SEARCH_GET_PARAMETER: search_term,
                    **extra_filters
                } if params is None else params
            )

            if response.status_code == 200:
                data: dict[str, int | str | list[dict]] = response.json()

                return data

    @property
    def request_payload(self) -> dict[str, None | str | dict[str, None | str]]:
        return {
            "url": f"{self.API_URI[:-1] if self.API_URI.endswith('/') else self.API_URI}",
            "headers": {
                self.HEADER_FOR_SECRET: self.API_SECRET
            } if self.HEADER_FOR_SECRET else None,
            "params": {
                self.SEARCH_GET_PARAMETER: None,
            }
        }

    @property
    def __name__(self) -> str:
        return self.__class__.__name__.lower().replace("api", "")  # noqa
