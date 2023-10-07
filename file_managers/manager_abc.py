from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class FileNotFound(Exception):
    pass


class FileManager(ABC):
    """
    Абстрактный класс файлового менеджера.
    """
    def __call__(self, file_path: Path) -> None:
        """
        Переназначение файла,
        который обрабатывает менеджер.
        :param file_path: путь до нового файла.
        :type file_path: Path
        :return: None
        :rtype: None
        """
        if file_path.exists():
            self.file = file_path
        else:
            raise FileNotFound(f"File {file_path} does not exist")

    @abstractmethod
    def add_vacancy(self, vacancy) -> None:
        """
        Добавление вакансии в файл.
        :param vacancy: форматированный словарь вакансии
            согласно VacancySchema
        :type vacancy: dict
        :return: None
        :rtype: None
        """
        pass

    @abstractmethod
    def delete_vacancy(self, *, index: Optional[int] = None, vacancy_id: Optional[int] = None):
        """
        Удаление вакансии из файла по ID или индексу.
        :param index: индекс вакансии в Array[VacancySchema]
        :type index: int
        :param vacancy_id: ID вакансии по полю id
        :type vacancy_id: int
        :return: None
        :rtype: None
        """
        pass

    @abstractmethod
    def order_by(self, fields: list[str], desc: bool = False) -> None:
        """
        Сортировка объектов вакансий в файле.
        :param fields: список полей, по которым необходима
            сортировка (порядок полей влияет на сортировку).
        :type fields: list
        :param desc: флаг обратного порядка сортировки.
            По умолчанию False.
        :type desc: bool
        :return: None
        :rtype: None
        """
        pass

    @abstractmethod
    def filter(self, **params) -> None:
        """
        Преобразовывает файл, в котором будут содержаться
        только отфильтрованные объекты вакансий.
        :param params: параметры, по которым необходимо
            применить фильтр.
        :type params:
        :return: None
        :rtype: None
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Очистка файла от содержимого.
        :return: None
        :rtype: None
        """
        pass
