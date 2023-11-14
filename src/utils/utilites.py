# Функции для модуля main.py
from src.utils.areas import AreasHH, AreasSJ
from src.utils.vacancies import VacHH, VacSJ, VacPrint


def loading_regions_hh():
    """
    Загружает перечни регионов и городов с сервиса hh.ru.
    :return: Json-файл с регионами/населёнными пунктами.
    """
    # Создаём экземпляр класса AreasHH, по-умолчанию регион "Россия".
    area_hh = AreasHH()
    # Получаем словарь с регионами и сохраняем его в json-файл.
    area_hh.request_to_api()


def loading_regions_sj() -> None:
    """
    Загружает перечни регионов и городов с сервиса superjob.ru.
    :return: Json-файл с регионами/населёнными пунктами.
    """
    # Создаём экземпляр класса AreasSJ, по-умолчанию регион "Россия".
    area_sj = AreasSJ()
    # Получаем словарь с регионами и сохраняем его в json-файл.
    area_sj.request_to_api()


def user_name() -> str:
    """
    Информация о программе.
    Выводит приветствие для пользователя.
    :return: Вывод обращения к пользователю, его имени, str.
    """
    name = input('\nЗдравствуйте! Наша программа поможет Вам изучить имеющиеся вакансии,\n'
                 'предлагаемые работодателями на территории Российской Федерации,\n'
                 'размещённые на сервисах HeadHunter (hh.ru) и SuperJob (superjob.ru).\n\n'
                 'Как Вас зовут? ').strip()
    # Вывод обращения к пользователю.
    match name:
        # Если name == ""
        case '':
            name = 'Пользователь'
            print(f'Хорошо, будем называть Вас {name}. 👌\n')
        # Сохранить имя в name, если оно не пустая строка.
        case name:
            print(f'Очень приятно, {name}. 🤝\n')
    return name


def exit_program(name) -> None:
    """
    Выход из приложения.
    :return: Выводит сообщение и выходит из приложения.
    """
    print(f'\nДо свидания, {name}! 👋')
    raise SystemExit('Работа программы завершена.\n')


def service_selection(name: str) -> int:
    """
    Выбираем сервис для получения и вывода данных.
    :param name: Имя пользователя, str.
    :return: Возвращает номер выбранного сервиса (int) или выходит из программы.
    """
    num_vak = input(f'\nВыберите сервис, с которого хотите получить информацию.\n'
                    f'Для этого введите:\n'
                    f'   ✅ HeadHunter (hh.ru)........ - 1\n'
                    f'   ✅ SuperJob (superjob.ru).... - 2\n'
                    f'   ❌ Завершить работу программы - 0.\n\n'
                    f'Введите команду: ')
    all_ok = False
    while not all_ok:
        try:
            match int(num_vak):
                # HeadHunter (hh.ru)
                case 1:
                    print(f'\n{name}, Вы выбрали HeadHunter (hh.ru). 👌\n')
                # SuperJob (superjob.ru)
                case 2:
                    print(f'\n{name}, Вы выбрали SuperJob (superjob.ru). 👌\n')
                # Завершение работы программы.
                case 0:
                    exit_program(name)  # Выход из приложения
        except ValueError:
            num_vak = input(f'\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: ')
        else:
            # Возвращение номера выбранного сервиса
            return int(num_vak)


def choosing_region(service: str, name: str, area_id_country: int) -> int:
    """
    Выбор региона для отображения вакансий.
    :param service: Строка, указывающая на выбор сервиса: "hh" - HeadHunter, "sj" - SuperJob, str.
    :param name: Имя пользователя, str.
    :param area_id_country: id страны по умолчанию (Россия), int.
    :return: Выводит id региона для поиска вакансий, int.
    """
    all_ok = False
    while not all_ok:
        # Регион, который указывает пользователь.
        area_vak = input(
            f'\nДля поиска вакансий введите, пожалуйста, название одного региона или города России\n'
            f'без указания кратких обозначений "г.", "с.", "х." и т.д., например:\n'
            f'Москва, Санкт-Петербург, Ростовская область, Ростов-на-Дону.\n'
            f'Введите название региона/населённого пункта: ').strip().lower()

        # Ищем id на указанном сервисе
        try:
            # Если выбран HeadHunter
            if service == 'hh':
                # Переопределяем экземпляр класса AreasHH с указанием региона, указанного пользователем.
                area_hh = AreasHH(area=area_vak)
                # Получаем id региона/населённого пункта, который указал пользователь.
                area_id = area_hh.extract_area_id()
            # Если выбран SuperJob
            elif service == 'sj':
                # Переопределяем экземпляр класса AreasSJ с указанием региона, указанного пользователем.
                area_sj = AreasSJ(area=area_vak)
                # Получаем id региона/населённого пункта, который указал пользователь.
                area_id = area_sj.extract_area_id()
            # Если указано что-то другое
            else:
                print('Программа не ищет данные на указанном сервисе.')
                exit_program(name)
        except ValueError:
            raise ValueError('Некорректные данные о сервисе.')

        # Если не нашли, указанный пользователем, регион/населённый пункт
        if area_id == area_id_country:
            num_area = input(f'\nМы не нашли, указанный Вами регион/населённый пункт, в имеющейся базе.\n'
                             f'Можем показать вакансии, имеющиеся в России.\n'
                             f'Чтобы продолжить введите одну из следующих команд:\n'
                             f'   ✅ Выбрать другой регион/населённый пункт - 1\n'
                             f'   ✅ Показать вакансии в России............ - 2\n'
                             f'   ❌ Заверишь работу программы............. - 0\n\n'
                             f'Введите команду: ')

            # Выбор разделов меню
            all_ok_area = False
            while not all_ok_area:
                try:
                    match int(num_area):
                        # Вывод сообщения, прерывание цикла
                        case 1:
                            print(f'\n{name}, введите другой регион/населённый пункт.\n')
                            all_ok_area = True
                        # Вывод сообщения, прерывание циклов
                        case 2:
                            print(f'\n{name}, мы подберём для Вас вакансии на территории России.\n')
                            all_ok_area = True
                            all_ok = True
                        # Завершение работы программы
                        case 0:
                            exit_program(name)  # Выход из приложения
                except ValueError:
                    num_area = input(f'\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: ')
        else:
            all_ok = True
    return area_id


def name_vak_word(name: str) -> str:
    """
    Ввод называния вакансии (ключевого слова)
    :param name: Имя пользователя, str.
    :return: Возвращает ключевое слово для поиска вакансии, str.
    """
    name_vak = input(f'\n{name}, введите ключевое слово, по которому мы будем осуществлять поиск вакансий.\n'
                     f'Например: водитель, программист, python, java и т.д.\n\n'
                     f'Должность: ').lower()
    return name_vak


def show_only_with_salary(name: str) -> bool:
    """
    Определяем нужно ли выводить данные только с зарплатой или все имеющиеся вакансии.
    :param name: Имя пользователя, str.
    :return: Флаг с зарплатой (True) или все (False), bool.
    """
    only_with_salary = False  # Показывать только с зарплатой
    salary_vak = input('\nВыберите одну из команд:\n'
                       '   ✅ Показать вакансии только с указанием зарплаты - 1\n'
                       '   ✅ Показать все имеющиеся вакансии.............. - 2\n'
                       '   ❌ Завершить работу программы................... - 0\n\n'
                       'Введите команду: ')
    all_ok = False
    while not all_ok:
        # Обработка команд
        try:
            match int(salary_vak):
                # Запрос данных с api только с зарплатой.
                case 1:
                    print(f'\nOK, {name}.\n')
                    only_with_salary = True
                    all_ok = True
                # Запрос данных с api любых вакансий, в т.ч. без зарплаты.
                case 2:
                    print(f'\nOK, {name}.\n')
                    all_ok = True
                # Завершение работы программы.
                case 0:
                    exit_program(name)  # Выход из приложения
        except ValueError:
            salary_vak = input(f'\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: ')
    return only_with_salary


def looking_salary(only_with_salary: bool, name: str) -> int:
    """
    Выводит размер желаемой заработной платы для поиска вакансий.
    :param only_with_salary: Флаг с зарплатой (True) или все (False), bool.
    :param name: Имя пользователя, str.
    :return: Размер желаемой заработной платы, int.
    """
    salary = 0  # Размер искомой зарплаты
    if only_with_salary:
        salary = input('\nУкажите ожидаемый размер заработной платы (в рублях): ')
        all_ok = False
        while not all_ok:
            # Обработка ввода
            try:
                # Размер ожидаемой зарплаты.
                salary = int(salary)
                if salary <= 0:
                    salary = 0
                all_ok = True
            except ValueError:
                salary = input(f'\n❗{name}, нужно ввести целое положительное число: ')
    return salary


def choose_sort_method(only_with_salary: bool, name: str) -> int:
    """
    Выбор метода сортировки: 1 - по датам, 2 - по размеру зарплаты.
    :param only_with_salary: Флаг с зарплатой (True) или все (False), bool.
    :param name: Имя пользователя, str.
    :return: Целое число — выбранный метод, int.
    """
    sort_method = 1
    if only_with_salary:
        sort_method = input('\nКак нам отсортировать вакансии?\n'
                            '   ✅ По заработной плате (по убыванию)  - 1\n'
                            '   ✅ По дате публикации (по убыванию).. - 2\n'
                            '   ❌ Завершить работу программы........ - 0\n\n'
                            'Введите команду: ')
        all_ok = False
        while not all_ok:
            # Обработка команд
            try:
                match int(sort_method):
                    # Метод сортировки по зарплате (от большей к меньшей), выход из цикла.
                    case 1:
                        sort_method = 1
                        all_ok = True
                    # Метод сортировки датам (от ранних к поздним), выход из цикла.
                    case 2:
                        sort_method = 2
                        all_ok = True
                    # Завершение работы программы.
                    case 0:
                        exit_program(name)
            except ValueError:
                sort_method = input(f'\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: ')
    return sort_method


def displaying_jobs_screen(service: str, name: str, name_vak: str, area_id: int, only_with_salary: bool, salary: int,
                           sort_method: int) -> None:
    """
    Вывод данных о вакансиях на экран.
    :param service: Строка, указывающая на выбор сервиса: "hh" - HeadHunter, "sj" - SuperJob, str.
    :param name: Имя пользователя, str.
    :param name_vak: Ключевое слово для поиска вакансии, str.
    :param area_id: ID региона для поиска вакансий, int.
    :param only_with_salary: Флаг с зарплатой (True) или все (False) вакансии, bool.
    :param salary: Размер желаемой заработной платы, int.
    :param sort_method: Целое число — выбранный метод сортировки (по датам или размеру зарплаты), int.
    :return: Выводит данные на экран.
    """
    all_ok = False
    while not all_ok:
        # Инициализация экземпляров классов зависит от выбранного сервиса
        try:
            # Если выбран HeadHunter
            if service == 'hh':
                # Создаём экземпляр класса VacHH - вакансии с hh.ru.
                if only_with_salary or salary != 0:
                    prof_hh = VacHH(position=name_vak, area=area_id, only_with_salary=only_with_salary, salary=salary)
                    prof_print = VacPrint(sort_method=sort_method)
                else:
                    prof_hh = VacHH(position=name_vak, area=area_id)
                    prof_print = VacPrint()

                # Получаем все вакансии в соответствии с запросом пользователя,
                # сохраняя их в json-файлы.
                prof_hh.vacancies_all()

                # Размер словаря с вакансиями.
                size_dict_vak = prof_hh.size_dict

            # Если выбран SuperJob
            elif service == 'sj':
                # Создаём экземпляр класса VacHH - вакансии с hh.ru.
                if only_with_salary or salary != 0:
                    prof_sj = VacSJ(position=name_vak, area=area_id, only_with_salary=only_with_salary, salary=salary)
                    prof_print = VacPrint(sort_method=sort_method)
                else:
                    prof_sj = VacSJ(position=name_vak, area=area_id)
                    prof_print = VacPrint()

                # Получаем все вакансии в соответствии с запросом пользователя,
                # сохраняя их в json-файлы.
                prof_sj.vacancies_all()

                # Размер словаря с вакансиями.
                size_dict_vak = prof_sj.size_dict

            # Если указано что-то другое
            else:
                print('Программа не ищет данные на указанном сервисе.')
                exit_program(name)
        except ValueError:
            raise ValueError('Некорректные данные о сервисе.')

        if size_dict_vak == 0:
            commands_prg = input('\nВыберите одну из команд:\n'
                                 '   ✅ Ввести наименование должности заново - 1\n'
                                 '   ❌ Заверишь работу программы........... - 0\n\n'
                                 'Введите команду: ')
            # Обработка команд
            all_ok_position = False
            while not all_ok_position:
                try:
                    match int(commands_prg):
                        # Ввод наименования должности заново.
                        case 1:
                            name_vak = input(f'\n{name}, введите должность: ').lower()
                            all_ok_position = True
                        # Завершение работы программы.
                        case 0:
                            exit_program(name)  # Выход из приложения
                except ValueError:
                    commands_prg = input(f'\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: ')
        else:

            # Вывод информации о вакансиях
            count_vak = input(f'Какое количество вакансий из найденных '
                              f'({size_dict_vak} шт.) Вы бы хотели увидеть? ')

            # Проверка корректности введённых данных
            if not count_vak.isdigit() or int(count_vak) > size_dict_vak:
                # Количество вакансий для вывода в случае некорректного ввода (все).
                count_vak = size_dict_vak
                print(f'\nВы ввели некорректные данные, '
                      f'поэтому мы покажем Вам все найденные вакансии ({count_vak} шт.).\n')

                # Выводим информацию
                prof_print.vacancies_print(count_vak, service)
                all_ok = True

            else:
                # Количество вакансий, заданное пользователем, для вывода.
                count_vak = int(count_vak)
                print(f'\nНиже будут представлены вакансии, '
                      f'которые мы нашли по Вашему запросу ({count_vak} шт.).\n')

                # Выводим информацию
                prof_print.vacancies_print(count_vak, service)
                all_ok = True

