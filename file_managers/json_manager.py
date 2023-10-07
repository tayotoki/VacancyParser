import json
from pathlib import Path
from typing import Optional

from settings import JSON_PATH

from file_managers.manager_abc import FileManager


class JSONManager(FileManager):
    save_path: Path = JSON_PATH

    def __call__(self, file_path: Path | None = None):
        if file_path is None:
            self.file = self.save_path
        else:
            super().__call__(file_path)

    def add_vacancy(self, vacancy):
        with open(self.file, "r+") as file:
            if file.read() == "":
                data = []
            else:
                file.seek(0)
                data = json.load(file)

            data.append(vacancy)
            file.seek(0)
            file.write(json.dumps(data, indent=2, ensure_ascii=False))

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

        with open(self.file, "w") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def clear(self):
        with open(self.file, "w"):
            pass

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

        with open(self.file, "w") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def filter(self, *, salary_from: int = 0, salary_to: int = float("inf")):
        with open(self.file, "r+") as file:
            data = json.loads(file.read())

        filtered = []

        for vacancy in data:
            match vacancy:
                case {
                    "salary": {
                        "from": None,
                        "to": int() | float() as to,
                        **kwargs_,
                    },
                    **kwargs
                }:
                    if salary_from <= to <= salary_to:
                        filtered.append(vacancy)
                case {
                    "salary": {
                        "from": int() | float() as from_,
                        "to": None,
                        **kwargs_,
                    },
                    **kwargs
                }:
                    if from_ >= salary_from:
                        filtered.append(vacancy)
                case {
                    "salary": {
                        "salary_from": int() | float() as from_,
                        "salary_to": int() | float() as to,
                        **kwargs_,
                    },
                    **kwargs
                }:
                    if to <= salary_to and from_ >= salary_from:
                        filtered.append(vacancy)

            with open(self.file, "w") as file:
                file.write(json.dumps(filtered, indent=2, ensure_ascii=False))
