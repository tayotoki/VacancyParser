from datetime import datetime

from credentials import superjob

from api_abc import API, Request, VacancySchema


class SuperJobAPI(API):
    API_URI = "https://api.superjob.ru/2.0"
    API_SECRET = superjob.SECRET_KEY
    HEADER_FOR_SECRET = "X-Api-App-Id"
    SEARCH_GET_PARAMETER = "keyword"

    MAX_RESULTS = 100  # <=100

    def _parse_raw(self, data: dict) -> list[VacancySchema]:
        result = []

        for vacancy_fields in data["objects"]:
            result.append(
                VacancySchema(
                    id=vacancy_fields["id"],
                    name=vacancy_fields["profession"],
                    area=vacancy_fields["town"],
                    salary={
                        "from": vacancy_fields["payment_from"],
                        "to": vacancy_fields["payment_to"],
                    },
                    employer=vacancy_fields["client"],
                    description=vacancy_fields["candidat"],
                    published_at=datetime.fromtimestamp(vacancy_fields["registered_date"])
                )
            )

        return result

    @property
    def default_request_payload(self) -> Request:
        return Request(
            url="/vacancies",
            headers={
                self.HEADER_FOR_SECRET: self.API_SECRET
            },
            params={
                self.SEARCH_GET_PARAMETER: None,
                "count": self.MAX_RESULTS,
            }
        )
