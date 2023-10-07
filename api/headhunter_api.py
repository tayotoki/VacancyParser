from .api_abc import API, Request, VacancySchema
from datetime import datetime


class HeadHunterAPI(API):
    API_URI = "https://api.hh.ru"
    SEARCH_GET_PARAMETER = "text"

    MAX_RESULTS = 100  # <=100

    def _parse_raw(self, data: dict) -> list[VacancySchema]:
        result = []

        for vacancy_fields in data["items"]:
            result.append(
                VacancySchema(
                    id=vacancy_fields["id"],
                    name=vacancy_fields["name"],
                    area=vacancy_fields["area"]["name"],
                    salary=vacancy_fields["salary"],
                    employer={
                        "name": vacancy_fields["employer"]["name"],
                        "vacancies": vacancy_fields["employer"].get("vacancies_url"),
                    },
                    description=vacancy_fields["snippet"],
                    published_at=str(datetime.fromisoformat(vacancy_fields["published_at"]))
                )
            )

        return result

    @property
    def default_request_payload(self) -> Request:
        return Request(
            url="/vacancies",
            headers=None,
            params={
                "describe_arguments": True,
                "per_page": self.MAX_RESULTS,
                self.SEARCH_GET_PARAMETER: None
            }
        )
