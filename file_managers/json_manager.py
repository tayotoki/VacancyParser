import json
from typing import Optional

from file_managers.manager_abc import FileManager


class JSONManager(FileManager):
    def add_vacancy(self, vacancy):
        with open(self.file, "r+") as file:
            data = json.load(file)
            data.append(vacancy)
            json.dump(data, file, indent=2, ensure_ascii=False)

    def delete_vacancy(self, *, index: Optional[int] = None, vacancy_id: Optional[int] = None):
        if any(
            (
                index is None and vacancy_id is None,
                index is not None and vacancy_id is not None,
            )
        ):
            raise ValueError("One argument 'index' or 'vacancy_id' must be passed")

        with open(self.file, "r+") as file:
            data: list[dict] = json.load(file)

            if index:
                try:
                    data[index]
                except IndexError:
                    pass
                else:
                    del data[index]

            if vacancy_id:
                for i, vacancy in enumerate(data):
                    if vacancy["id"] == vacancy_id:
                        del data[i]
                        break

            json.dump(data, file, indent=2, ensure_ascii=False)

    def order_by(self, fields: list[str], desc: bool = False):
        if not isinstance(desc, bool):
            raise ValueError("desc argument must be a boolean type")

        with open(self.file, "r+") as file:
            data: list[dict] = json.load(file)

            data = sorted(
                data,
                key=lambda vacancy: [vacancy.get(field) for field in fields],
                reverse=desc
            )

            json.dump(data, file, indent=2, ensure_ascii=False)

    def filter(self, *, salary_from: int = 0, salary_to: int = float("inf")):
        with open(self.file, "r+") as file:
            data = json.load(file)

            filtered = []

            for vacancy in data:
                match vacancy:
                    case {
                        "salary_from": None,
                        "salary_to": int() | float() as to,
                        **kwargs
                    }:
                        if to <= salary_to:
                            filtered.append(vacancy)
                    case {
                        "salary_from": int() | float() as from_,
                        "salary_to": None,
                        **kwargs
                    }:
                        if from_ >= salary_from:
                            filtered.append(vacancy)
                    case {
                        "salary_from": int() | float() as from_,
                        "salary_to": int() | float() as to,
                        **kwargs
                    }:
                        if to <= salary_to and from_ >= salary_from:
                            filtered.append(vacancy)

            json.dump(filtered, file)
