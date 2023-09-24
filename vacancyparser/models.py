from __future__ import annotations

from typing import Optional, TypeVar

from pydantic import (
    BaseModel,
    Field,
    AnyHttpUrl,
    PositiveInt,
    PositiveFloat,
    AliasChoices,
    ConfigDict
)


class GlobalConfig:
    model_config = ConfigDict(
        populate_by_name=True
    )


# EXTRA MODELS
class EmployerHH(BaseModel):
    id: str
    name: str
    url: AnyHttpUrl
    vacancies_url: AnyHttpUrl


class EmployerSJ(BaseModel, GlobalConfig):
    id: PositiveInt
    name: str = Field(alias="title")
    url: AnyHttpUrl = Field(alias="link")


class ExperienceHH(BaseModel):
    id: str
    name: str


class ExperienceSJ(BaseModel):
    id: PositiveInt
    name: str = Field(alias="title")


class SalaryHH(BaseModel, GlobalConfig):
    from_: Optional[PositiveInt | PositiveFloat] = Field(alias="from")
    to: Optional[PositiveInt | PositiveFloat]
    currency: str


class AreaHH(BaseModel):
    id: int
    name: str
    url: AnyHttpUrl


class AreaSJ(BaseModel, GlobalConfig):
    id: PositiveInt
    name: str = Field(alias="title")


class DescriptionHH(BaseModel):  # snippet in JSON
    requirement: str
    responsibility: str


# TYPE VARS
Employers = TypeVar(
    "Employers",
    EmployerHH,
    EmployerSJ
)

Areas = TypeVar(
    "Areas",
    AreaHH,
    AreaSJ
)


# MAIN MODELS
class Vacancy(BaseModel, GlobalConfig):
    id: str | PositiveInt
    name: str = Field(alias="profession")
    area: Areas = Field(
        validation_alias=AliasChoices(
            "area",
            "town",
        )
    )
    salary: Optional[SalaryHH] = None
    employer: Employers = Field(
        validation_alias=AliasChoices(
            "client",
            "employer",
        )
    )
    description: DescriptionHH | str = Field(
        validation_alias=AliasChoices(
            "candidat",
            "snippet",
        )
    )
    payment_from: Optional[int] = None
    payment_to: Optional[int] = None


class Vacancies(BaseModel, GlobalConfig):
    items: list[Vacancy] = Field(alias="objects")
    total: int = Field(alias="found")
