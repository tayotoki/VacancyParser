import json

from api import headhunter_api, superjob_api
from file_managers import json_manager
from utils.functions import create_vacancy_objects_from_json, show_vacancies, get_user_salary, get_user_sort_fields

test_search = "Python developer"


hh_api = headhunter_api.HeadHunterAPI()
sj_api = superjob_api.SuperJobAPI()

json_handler = json_manager.JSONManager()

# Вызов метода __call__
# для применения файла по умолчанию
json_handler()


def main():
    search_term = input(
        "Введите поисковый запрос:\n"
    )

    hh_vacancies = hh_api.get_vacancies(search_term=search_term)
    sj_vacancies = sj_api.get_vacancies(search_term=search_term)

    # Добавление всех найденных вакансий в файл.
    for vacancy in [*hh_vacancies, *sj_vacancies]:
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


if __name__ == "__main__":
    main()
