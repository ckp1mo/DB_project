from src.config import config
from src.utils import create_tables, filling_tables
from src.requests_api import get_requests
from src.DBManager import DBManager

employees_id_list = ['1942330', '49357', '78638', '2748', '2180', '1648566', '1942336', '3529', '9498120',
                     '9498112', '4352']


def main() -> None:
    """
    Основная функция для запуска скрипта
    :return: None
    """
    params = config()
    # Вызывается функция для создания таблиц
    create_tables(params)
    #
    # Вызывается функция для получения данных по API запросу
    employees_list = get_requests(employees_id_list)

    # Вызывается функция для заполения таблиц данными
    filling_tables(employees_list, params)


main()


# проверка работы методов класса

# params = config()
# test_class = DBManager(params)
# print(test_class.get_companies_and_vacancies_count())  # компания и кол-во вакансий
# print(test_class.get_all_vacancies())  # все вакансии с названием компании, названия вакансииб зарплаты и ссылки
# print(test_class.get_avg_salary())  # получает среднюю зарплату по вакансиям
# print(test_class.get_vacancies_with_higher_salary())  # список вакансий, у которых зп выше средней по всем вакансиям.
# print(test_class.get_vacancies_with_key(input().split()))  # поиск по вакансий по словам
