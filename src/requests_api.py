import requests


PARAMS = {
    'area': '113',
    'per_page': '50',
    'only_with_vacancies': 'true',
    'sort_by': 'by_vacancies_open'
}


# функция выполняет два действия. что-то подсказывает, что нужно разделить функцию на две, пока не придумал как
def get_requests(employees_id: list[str]) -> list[dict]:
    """
    Функция выполняет API запрос, получает данные о работодателе, о вакансиях работодателя.
    Разбирает ответ сервера, собирает нужные ключи и создает словарь на этой основе.
    Каждый словарь содержит информацию о работодателе, а так же десять открытых вакансий.
    :return: массив
    """
    employees_list = []
    for emp_id in employees_id:
        vacancy_list = []

        # запрос данных о каждом работодателе
        url_emp = f'https://api.hh.ru/employers/{emp_id}'
        response_employees = requests.get(url_emp, headers={'User-Agent': 'slon'}, params=PARAMS)

        # запрос данных о вакансиях работодателя
        url_vac = f'https://api.hh.ru/vacancies?employer_id={emp_id}'
        response_vacancies = requests.get(url_vac, headers={'User-Agent': 'slon'}, params=PARAMS)
        for vac in response_vacancies.json()['items']:
            if len(vacancy_list) < 11:
                vacancy_list.append(
                    {
                        'id': vac['id'],
                        'name': vac['name'],
                        'town': vac['area']['name'],
                        'salary': vac['salary'],
                        'alternate_url': vac['alternate_url'],
                        'employer_id': vac['employer']['id'],
                        'employer_name': vac['employer']['name'],
                        'employer_url': vac['employer']['alternate_url'],
                        'snippet': vac['snippet'],
                        'schedule': vac['schedule'],
                        'professional_roles': vac['professional_roles'],
                        'experience': vac['experience'],
                        'employment': vac['employment'],
                    })
            else:
                break
        if response_employees.json()['logo_urls'] is None:
            logo = None
        else:
            logo = response_employees.json()['logo_urls']['original']
        employees_list.append(
            {
                'id': response_employees.json()['id'],
                'name': response_employees.json()['name'],
                'description': response_employees.json()['description'],
                'site_url': response_employees.json()['site_url'],
                'alternate_url': response_employees.json()['alternate_url'],
                'vacancies_url': response_employees.json()['vacancies_url'],
                'open_vacancies': response_employees.json()['open_vacancies'],
                'vacancies': vacancy_list,
                'logo_url': logo
            })
    return employees_list
