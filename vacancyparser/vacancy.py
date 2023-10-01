class Vacancy:
    all = []

    def __new__(cls, *args, **kwargs):
        instance = cls(*args, **kwargs)
        cls.all.append(instance)
        return super().__new__(cls, *args, **kwargs)

    def __init__(
            self,
            id: str | int,
            name: str,
            area,
            salary: dict[str, int | float | str],
            employer: dict[str, int | str],
            description: dict[str, str] | str,
            published_at: str,
    ) -> None:
        self._id = id
        self._name = name
        self._salary = salary
        self._employer = employer
        self._description = description
        self._published_at = published_at

    @property
    def salary_from(self) -> int | str | None:
        if self.salary.get("from") is None:
            return "Нет данных"
        return self.salary["from"]

    @property
    def salary_to(self) -> int | str | None:
        if self.salary.get("to") is None:
            return "Нет данных"
        return self.salary["to"]

    @property
    def employer_name(self) -> str:
        try:
            name = self.employer["name"]
        except KeyError:
            name = self.employer["title"]

        return name

    @property
    def employer_vacancies_link(self) -> str:
        try:
            link = self.employer["vacancies_url"]
        except KeyError:
            link = self.employer