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


def get_user_salary() -> tuple[int | None, int | float | None]:
    user_salary_from = input(
        "Введите начальное значение зарплаты "
        "или оставьте поле пустым\n"
    ).strip()

    user_salary_to = input(
        "Введите конечное значение зарплаты "
        "или оставьте поле пустым\n"
    ).strip()

    match [user_salary_from, user_salary_to]:
        case ("", ""):
            print("Фильтры не были применены\n")
            return None, None
        case ("", to) if to.strip().isnumeric():
            return 0, int(to)
        case (from_, "") if from_.strip().isnumeric():
            return int(from_), float("inf")
        case (from_, to) if from_.strip().isnumeric and to.strip().isnumeric():
            return int(from_), int(to)
        case _:
            print("Вы ввели некорректные данные. Давайте повторим ввод\n")
            return get_user_salary()


def get_user_sort_fields() -> tuple[list, bool]:
    fields = {
        "0": "published_at",
        "1": "name",
        "2": "area"
    }

    user_fields = input(
        "Введите численное представление полей, "
        "по которым нужно отсортировать, из таблицы ниже.\n"
        "Вводить последовательно, без пробелов.\n\n"
        "Дата публикации: 0,\n"
        "Название: 1,\n"
        "Город: 2,\n"
    )

    order_fields = {
        fields.get(key)
        for key in user_fields.strip().replace(" ", "")
        if key in fields
    }

    if order_fields:

        user_desc = input(
            "Сортировать в прямом порядке? "
            "Введите 'нет' если хотите отсортировать в обратном, "
            "если в прямом - оставьте поле пустым\n"
        )

        desc = False

        if user_desc.strip().lower() == "нет":
            desc = True
    else:
        print("Вы ввели некорректиные числа. Попробуйте еще раз.\n")
        return get_user_sort_fields()

    return list(order_fields), desc
