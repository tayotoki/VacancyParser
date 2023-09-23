from typing import Optional

from credentials import superjob

from .api_abc import API


class HeadHunterAPI(API):
    API_URI = "https://api.hh.ru"
    SEARCH_GET_PARAMETER = "text"

    def get_vacancies(self, search_term: str, **extra_filters) -> dict[str, int | str | list[dict]]:
        return self.request_method_get(search_term=search_term, **extra_filters)

    def request_method_get(
            self,
            *,
            search_term: str,
            url: str = "/vacancies",
            params: Optional[dict[str, str]] = None,
            **extra_filters
    ) -> dict[str, int | str | list[dict]]:
        params = self.request_payload["params"]

        # Требование API headhunter.
        if extra_filters:
            params["describe_arguments"] = "true"

        return super().request_method_get(
            search_term=search_term,
            params=params,
            **extra_filters
        )


class SuperJobAPI(API):
    API_URI = "https://api.superjob.ru/2.0"
    API_SECRET = superjob.SECRET_KEY
    HEADER_FOR_SECRET = "X-Api-App-Id"
    SEARCH_GET_PARAMETER = "keyword"

    def get_vacancies(self, search_term: str, **extra_filters) -> dict[str, int | str | list[dict]]:
        return self.request_method_get(search_term=search_term, **extra_filters)
