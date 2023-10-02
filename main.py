import json

from api import headhunter_api, superjob_api
from file_managers import json_manager
from utils.functions import create_vacancy_objects_from_json, show_vacancies

test_search = "Python developer"


hh_api = headhunter_api.HeadHunterAPI()
sj_api = superjob_api.SuperJobAPI()

json_handler = json_manager.JSONManager()


def main():
    search_term = test_search

    hh_vacancies = hh_api.get_vacancies(search_term=search_term)
    sj_vacancies = sj_api.get_vacancies(search_term=search_term)

    json_handler()
    json_handler.clear()

    for vacancy in [*hh_vacancies, *sj_vacancies]:
        json_handler.add_vacancy(vacancy)

    # json_handler.filter(salary_from=100000)
    json_handler.order_by(["published_at"])
    # json_handler.delete_vacancy(index=-1)

    create_vacancy_objects_from_json(json_handler.file)
    show_vacancies()


main()