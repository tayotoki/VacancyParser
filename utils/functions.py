import json
from pathlib import Path

from vacancyparser.vacancy import Vacancy

from termcolor import colored


def setup(directory: Path, file: Path):
    if not directory.exists():
        directory.mkdir()

    if not file.exists():
        file.touch()


def create_vacancy_objects_from_json(file: Path):
    with open(file) as data:
        Vacancy.all = []

        data = json.load(data)

        for obj in data:
            Vacancy(**obj)


def show_vacancies():
    for i, vacancy in enumerate(Vacancy.all, 1):
        print(f"----------------<{i}>-----------------------")
        print(vacancy)
        print("---------------------------------------------")
