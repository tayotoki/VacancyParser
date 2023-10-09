from tqdm import tqdm

from api import headhunter_api, superjob_api
from file_managers import json_manager
from utils.functions import (
    create_vacancy_objects_from_json,
    show_vacancies,
    get_user_salary,
    get_user_sort_fields
)

hh_api = headhunter_api.HeadHunterAPI()
sj_api = superjob_api.SuperJobAPI()

json_handler = json_manager.JSONManager()

# Вызов метода __call__
# для инициализации файла по умолчанию
json_handler()

# Очистка файла от предыдущих результатов
json_handler.clear()


def main():
    search_term = input(
        "Введите поисковый запрос:\n"
    )

    hh_vacancies = hh_api.get_vacancies(search_term=search_term)
    sj_vacancies = sj_api.get_vacancies(search_term=search_term)

    # Добавление всех найденных вакансий в файл.
    for vacancy in tqdm([*hh_vacancies, *sj_vacancies]):
        json_handler.add_vacancy(vacancy)

    user_chose = input(
        f"Найдено {len(hh_vacancies) + len(sj_vacancies)} "
        f"результатов. Показать результаты?\n"
        f"Введите 'да' или оставьте поле пустым\n"
    )

    if user_chose.strip().lower() == "да":
        create_vacancy_objects_from_json(json_handler.file)
        show_vacancies()

    user_filters = input(
        "Отфильтровать вакансии по зарплате? "
        "Введите 'да' или оставьте поле пустым.\n"
    )

    if user_filters.strip().lower() == "да":
        salary_from, salary_to = get_user_salary()

        if salary_from is salary_to is None:
            pass
        else:
            json_handler.filter(salary_from=salary_from, salary_to=salary_to)

            user_chose = input(
                "Фильтры применены.\n"
                "Показать результаты?\n"
                "Введите 'да' или оставьте поле пустым\n"
            )

            if user_chose.strip().lower() == "да":
                create_vacancy_objects_from_json(json_handler.file)
                show_vacancies()

    user_sort = input(
        "Отсортировать вакансии? "
        "Введите 'да' или оставьте поле пустым\n"
    )

    if user_sort.strip().lower() == "да":
        user_fields, desc = get_user_sort_fields()

        json_handler.order_by(fields=user_fields, desc=desc)

        user_chose = input(
            "Соритровка выполнена\n"
            "Показать результаты?\n"
            "Введите 'да' или оставьте поле пустым\n"
        )

        if user_chose.strip().lower() == "да":
            create_vacancy_objects_from_json(json_handler.file)
            show_vacancies()

    user_delete = input(
        "Вы можете удалить лишние вакансии по индексу, "
        "индекс выглядит как нумерация в терминале - "
        "'...--<номер>--...', или по ID вакансии (подсвечивается "
        "зеленым цветом).\n"
        f"Также ID вакансии можно посмотреть в файле {json_handler.file}\n"
        "Введите 'да' если хотите удалить вакансию, иначе оставьте поле "
        "ввода пустым.\n"
    ).strip().lower()

    if user_delete == "да":
        while True:
            user_index = input(
                "Введите индекс вакансии, или оставьте поле пустым "
                "чтобы ввести ID\n"
            )

            if user_index.isnumeric():
                op_code = json_handler.delete_vacancy(index=int(user_index))

                if op_code == -1:
                    print("Такой вакансии нет!")
                else:
                    print("Вакансия удалена")
            else:
                user_vacancy_id = input("Введите ID вакансии\n").strip()

                if user_vacancy_id.isnumeric():
                    op_code = json_handler.delete_vacancy(vacancy_id=int(user_vacancy_id))

                    if op_code == -1:
                        print("Такой вакансии нет!")
                    else:
                        print("Вакансия удалена")

            repeat_deletion = input(
                "Повторить удаление? Введите 'да' или оставьте поле ввода пустым\n"
            )

            if repeat_deletion == "да":
                continue
            else:
                break

    print("Конец программы. Итоговый файл находится в \n"
          f"{json_handler.file}")


if __name__ == "__main__":
    main()
