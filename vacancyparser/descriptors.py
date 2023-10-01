from abc import ABC, abstractmethod


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

    @classmethod
    @abstractmethod
    def check_value(cls, value):
        pass

    @classmethod
    @abstractmethod
    def format_data(cls, attr):
        pass


class ID(Field):
    def __set__(self, instance, value):
        if isinstance(value, str):
            try:
                value = int(value)
            except Exception as e:
                raise ValueError(f"{e}. Can't reformat ID into int type")

        super().__set__(instance, value)

    @classmethod
    def check_value(cls, value):
        if not isinstance(value, int):
            raise ValueError("Invalid value for ID")

    @classmethod
    def format_data(cls, attr):
        return attr


class Area(Field):
    @classmethod
    def check_value(cls, value):
        pass

    @classmethod
    def format_data(cls, attr):
        ...