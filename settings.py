from pathlib import Path

from utils.functions import setup


BASE_DIR = Path(__file__).resolve().parent

json_vacancies_path = BASE_DIR / "file_managers" / "json_vacancies"

JSON_PATH = json_vacancies_path / "vacancies.json"

DB_INI_FILE = BASE_DIR / "database" / "database.ini"

DB_NAME = "vacancy_parser"

setup(directory=json_vacancies_path, file=JSON_PATH)
