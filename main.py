from src.config import config
from src.user_interaction import user_interaction
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


# Функция для пользовательского взаимодействия с классом DBManager через его методы.
# user_interaction(config())
