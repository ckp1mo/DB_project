import psycopg2


class DBManager:
    """
    Класс для работы с БД PostgreSQL
    """

    def __init__(self, params):
        self.params = params
        self.connect = psycopg2.connect(**self.params)

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT company_name, count(distinct vacancies) as vacancies
                    from vacancies
                    join companies using(company_id)
                    group by company_name
                    """
                )
                result = cur.fetchall()
        conn.close()
        return result

    def get_all_vacancies(self) -> list[tuple]:
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select name, company_name, salary_from, salary_to, vacancies.url
                    from vacancies
                    join companies using(company_id)
                    order by company_name
                    """
                )
                result = cur.fetchall()
        conn.close()
        return result

    def get_avg_salary(self) -> int:
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select avg(salary_from)
                    from vacancies
                    """
                )
                result = int(cur.fetchall()[0][0])
        conn.close()
        return result

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select name, salary_from
                    from vacancies
                    where salary_from > (select avg(salary_from) from vacancies)
                    order by salary_from DESC
                    """
                )
                result = cur.fetchall()
        conn.close()
        return result

    def get_vacancies_with_key(self, key_word: list[str]) -> list:
        with self.connect as conn:
            with conn.cursor() as cur:
                result_list = []
                for word in key_word:
                    cur.execute(
                        f"""
                        select *
                        from vacancies
                        where name ilike '%{word.lower()}%'
                        """
                    )
                    result = cur.fetchall()
                    result_list.extend(result)
        conn.close()
        if len(result_list) == 0:
            print('Поиск не удался')
        else:
            return result_list
