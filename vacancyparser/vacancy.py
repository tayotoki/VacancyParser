from .descriptors import (
    ID,
    Salary,
    Area,
    Employer,
    Description,
    Name,
    Publish
)


class Vacancy:
    all = []

    id = ID()
    name = Name()
    salary = Salary()
    area = Area()
    employer = Employer()
    description = Description()
    published_at = Publish()

    __slots__ = (
        "_id",
        "_name",
        "_area",
        "_salary",
        "_employer",
        "_description",
        "_published_at"
    )

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls.all.append(instance)
        return instance

    def __init__(
            self,
            id: str | int,
            name: str,
            area: str,
            salary: dict[str, int | float | str],
            employer: dict[str, int | str],
            description: dict[str, str] | str,
            published_at: str,
    ) -> None:
        self._id = id
        self._name = name
        self._area = area
        self._salary = salary
        self._employer = employer
        self._description = description
        self._published_at = published_at

    def __repr__(self):
        return (f"{self.id}\n"
                f"{self.name}\n"
                f"{self.area}\n"
                f"{self.salary}\n"
                f"{self.employer}\n"
                f"{self.description}\n"
                f"{self.published_at}")
