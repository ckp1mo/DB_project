from src.DBManager import DBManager


def user_interaction(params: dict) -> None:
    """
    Функция для взаимодействия с пользователем посредством методов класса DBManager.
    :return:
    """

    print('Привет!\n'
          'Выбирай, что мы будем делать?')
    while True:
        print('1. Посмотреть список всех компаний и кол-во вакансий у них.\n'
              '2. Посмотреть подробный список всех вакансий.\n'
              '3. Посмотреть среднюю зарплату.\n'
              '4. Посмотреть вакансии, у которых зарплата выше средней.\n'
              '5. Посмотреть вакансии по ключевым словам.\n'
              '0. Для выхода\n')
        user_choice = input()
        if user_choice == '1':
            [print(company) for company in DBManager(params).get_companies_and_vacancies_count()]
            continue
        elif user_choice == '2':
            [print(vacancy) for vacancy in DBManager(params).get_all_vacancies()]
            continue
        elif user_choice == '3':
            print(DBManager(params).get_avg_salary())
            continue
        elif user_choice == '4':
            [print(vacancy) for vacancy in DBManager(params).get_vacancies_with_higher_salary()]
            continue
        elif user_choice == '5':
            key_word = input('Введите слова для поиска: \n').split()
            if DBManager(params).get_vacancies_with_key(key_word):
                [print(vacancy) for vacancy in DBManager(params).get_vacancies_with_key(key_word)]
                continue
            else:
                continue
        elif user_choice == '0':
            print('>> Хорошего дня!')
            break
        else:
            print('>> Некорректный запрос.')
            continue
