from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class FileNotFound(Exception):
    pass


class FileManager(ABC):
    def __call__(self, file_path: Path):
        if file_path.exists():
            self.file = file_path
        else:
            raise FileNotFound(f"File {file_path} does not exist")

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, *, index: Optional[int] = None, vacancy_id: Optional[int] = None):
        pass

    @abstractmethod
    def order_by(self, filter_field: str, desc: bool):
        pass

    @abstractmethod
    def filter(self, **params):
        pass

    @abstractmethod
    def clear(self):
        pass
