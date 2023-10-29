from pathlib import Path

import psycopg2

from settings import DB_NAME

from database.config import get_config
from database.setub_db.setup import setup


def get_script(file: Path):
    if file.exists():
        with open(file) as file:
            script = file.read()
        return script


class DBManager:
    __is_db_exists = False
    __instance = None
    connection = None
    __config = get_config()

    def __new__(cls, *args, **kwargs):
        instance = cls.__instance

        if not cls.__is_db_exists:
            setup()
            cls.__is_db_exists = True
            cls.connection = next(cls.connect())

        if instance is None:
            instance = super().__new__(cls)

        return instance

    @classmethod
    def connect(cls):
        with psycopg2.connect(dbname=DB_NAME, **cls.__config) as con:
            yield con

    @classmethod
    def create_tables(cls):
        with cls.connection as con:
            with con.cursor() as cur:
                cur.execute(
                    get_script(Path(__file__).resolve().parent / "sql_scripts" / "create_tables.sql")
                )
                cur.close()
            con.close()


db_manager = DBManager()

DBManager.create_tables()
