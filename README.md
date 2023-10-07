# Описание
Приложение для парсинга вакансий с помощью публичных API Headhunter и SuperJob

## Установка
Создать виртуальное окружение python версии 3.11(рекомедуется) в папке .../VacancyParser:

    python3.11 -m venv env
    source ./env/bin/activate
    pip install -r requirements.txt

Или с помощью poetry:

    poetry env use python3.11
    poetry shell
    poetry install

## Данные для авторизации
Необходимо создать ```.env``` файл в ```.../VacancyParser```.
Пример файла ```example_env_file``` находится в корневом каталоге.

## Запуск
Запуск производится с помощью команды ```make```:

    make start_parser