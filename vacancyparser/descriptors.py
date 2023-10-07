from abc import ABC, abstractmethod

from termcolor import colored

__all__ = [
    "ID",
    "Salary",
    "Area",
    "Employer",
    "Description",
    "Name",
    "Publish"
]


class ColorMixin:
    COLOR = "blue"
    FIELD_NAME = ""

    def __init__(self):
        self.default_header = colored(self.FIELD_NAME, color=self.COLOR)


class Field(ABC):
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __set__(self, instance, value):
        self.check_value(value)

        setattr(instance, self.name, value)

    def __get__(self, instance, owner):
        field_value = self.format_data(
            getattr(instance, self.name)
        )

        return field_value

    @abstractmethod
    def check_value(self, value):
        pass

    @abstractmethod
    def format_data(self, attr):
        pass


class ID(Field, ColorMixin):
    FIELD_NAME = "id:"
    COLOR = "green"

    def __set__(self, instance, value):
        if isinstance(value, str):
            try:
                value = int(value)
            except Exception as e:
                raise ValueError(f"{e}. Can't reformat ID into int type")

        super().__set__(instance, value)

    def check_value(self, value):
        if not isinstance(value, int):
            raise ValueError("Invalid value for ID")

    def format_data(self, attr):
        return f"{self.default_header} {attr}"


class Area(Field, ColorMixin):
    FIELD_NAME = "Место работы:"

    def check_value(self, value):
        pass

    def format_data(self, attr):
        return f"{self.default_header} {attr}"


class Salary(Field, ColorMixin):
    FIELD_NAME = "Зарплата:"

    def check_value(self, value):
        pass

    def format_data(self, attr):
        if attr:
            return f"{self.default_header} {'от ' + str(attr['from']) if attr['from'] else ''} " \
                   f"{'до ' + str(attr['to']) if attr['to'] else ''} " \
                   f"{attr['currency'] if attr.get('currency') else ''}"

        return f"{self.default_header} Данные отсутствуют"


class Employer(Field, ColorMixin):
    FIELD_NAME = "Работодатель:"

    def check_value(self, value):
        pass

    def format_data(self, attr):
        default_value = f"{self.default_header} {attr['name']}"

        if not (vacancies_link := attr["vacancies"]):
            return default_value
        else:
            return f"{default_value}\n\tСсылка на остальные вакансии: {vacancies_link}"


class Description(Field):
    def check_value(self, value):
        pass

    def format_data(self, attr):
        default_headers = [
            colored(header, color="blue") for header
            in ["Кандидат:", "Требования:", "Обязанности:"]
        ]

        if isinstance(attr, dict):
            if (
                requirement := attr.get("requirement")
            ) and (
                responsibility := attr.get("responsibility")
            ):
                return (f"{default_headers[0]}\n\t"
                        f"{default_headers[1]} {requirement if requirement else '--'}\n\t"
                        f"{default_headers[2]} {responsibility if responsibility else '--'}")

        return f"{default_headers[0]} {attr}"


class Name(Field, ColorMixin):
    FIELD_NAME = "Название:"

    def check_value(self, value):
        pass

    def format_data(self, attr):
        return f"{self.default_header} {attr}"


class Publish(Field, ColorMixin):
    FIELD_NAME = "Дата публикации:"

    def check_value(self, value):
        pass

    def format_data(self, attr):
        return f"{self.default_header} {attr}"
