from typing import Optional

from credentials import superjob

from api_abc import API, Request, VacancySchema


class HeadHunterAPI(API):
    API_URI = "https://api.hh.ru"
    SEARCH_GET_PARAMETER = "text"

    def _parse_raw(self, data: dict) -> list[VacancySchema]:
        return data

    @property
    def default_request_payload(self) -> Request:
        return {
            "url": "/vacancies",
            "headers": None,
            "params": {
                "describe_arguments": True,
                self.SEARCH_GET_PARAMETER: None
            }

        }


class SuperJobAPI(API):
    API_URI = "https://api.superjob.ru/2.0"
    API_SECRET = superjob.SECRET_KEY
    HEADER_FOR_SECRET = "X-Api-App-Id"
    SEARCH_GET_PARAMETER = "keyword"

    def _parse_raw(self, data: dict) -> list[VacancySchema]:
        return data

    @property
    def default_request_payload(self) -> Request:
        return {
            "url": "/vacancies",
            "headers": {
                self.HEADER_FOR_SECRET: self.API_SECRET
            },
            "params": {
                self.SEARCH_GET_PARAMETER: None
            }
        }
