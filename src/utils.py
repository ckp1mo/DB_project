"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2


def create_tables(params: dict) -> None:
    """
    Функция создает табилцы в БД PostgresQL
    :return: None
    """
    connect = psycopg2.connect(**params)
    with connect as conn:
        with conn.cursor() as cur:
            # Создаем таблицу companies
            cur.execute(
                """CREATE TABLE if not exists companies
                (
                company_id serial PRIMARY KEY,
                company_hh_id int NOT NULL,
                company_name varchar(100) NOT NULL,
                open_vacancies int,
                url text,
                logo_path text
                )"""
            )
        with conn.cursor() as cur:
            # создаем таблицу vacancies
            cur.execute(
                """CREATE TABLE if not exists vacancies
                (
                vacancy_id serial PRIMARY KEY,
                company_id int REFERENCES companies(company_id),
                name varchar(100) NOT NULL,
                salary_from int,
                salary_to int, 
                town varchar(50) NOT NULL,
                requirement varchar(300),
                responsibility varchar(300),
                schedule varchar(100),
                professional_role varchar(100),
                experience varchar(100),
                employment varchar(100),
                url text
                )"""
            )


def filling_tables(employees_list: list[dict], params: dict) -> None:
    """
    Функция наполняет таблицы данными в БД PostgreSQL
    :param employees_list: массив с данными, содержит список словарей с работодателями.
    Каждый работодатель содержит список словарей свакансиями
    :return: None
    """
    connect = psycopg2.connect(**params)
    with connect as conn:
        with conn.cursor() as cur:
            for company in employees_list:
                cur.execute(
                    """
                    INSERT INTO companies (company_hh_id, company_name, open_vacancies, url, logo_path)
                    VALUES(%s, %s, %s, %s, %s)
                    RETURNING company_id
                    """,
                    (company['id'], company['name'], company['open_vacancies'], company['alternate_url'],
                     company['logo_url'])
                )
                company_id = cur.fetchone()[0]
                for vacancy in company['vacancies']:
                    if vacancy['salary']:
                        salary_from = vacancy['salary']['from']
                        salary_to = vacancy['salary']['to']
                    else:
                        salary_from = None
                        salary_to = None
                    cur.execute(
                        """
                        INSERT INTO vacancies (company_id, name, salary_from, salary_to, town, requirement, 
                        responsibility, schedule, professional_role, experience, employment, url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            company_id, vacancy['name'], salary_from, salary_to, vacancy['town'],
                            vacancy['snippet']['requirement'], vacancy['snippet']['responsibility'],
                            vacancy['schedule']['name'], vacancy['professional_roles'][0]['name'],
                            vacancy['experience']['name'], vacancy['employment']['name'], vacancy['alternate_url']
                        )
                    )
            conn.commit()
    conn.close()
