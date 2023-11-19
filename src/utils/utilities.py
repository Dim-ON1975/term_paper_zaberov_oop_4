# Функции для модуля main.py
from src.utils.areas import AreasHH, AreasSJ
from src.utils.constants import PATH_VAK_DIR_HH, PATH_ARE_HH, PATH_VAK_DIR_SJ, PATH_ARE_SJ, URL_AREAS_HH, URL_AREAS_SJ
from src.utils.vacancies import VacHH, VacSJ, VacPrint


def loading_regions_hh(url: str = URL_AREAS_HH, path_vak_dir_hh: str = PATH_VAK_DIR_HH,
                       path_are_hh: str = PATH_ARE_HH) -> None:
    """
    Загружает перечни регионов и городов с сервиса hh.ru.
    :param url: URL регионов, str.
    :param path_vak_dir_hh: Путь к директории для хранения файла, str.
    :param path_are_hh: Полное имя файла, str.
    :return: Json-файл с регионами/населёнными пунктами.
    """
    # Создаём экземпляр класса AreasHH, по-умолчанию регион "Россия".
    area_hh = AreasHH(url=url, path_vak_dir_hh=path_vak_dir_hh, path_are_hh=path_are_hh)
    # Получаем словарь с регионами и сохраняем его в json-файл.
    area_hh.request_to_api()


def loading_regions_sj(url: str = URL_AREAS_SJ, path_vak_dir_sj: str = PATH_VAK_DIR_SJ,
                       path_are_sj: str = PATH_ARE_SJ) -> None:
    """
    Загружает перечни регионов и городов с сервиса superjob.ru.
    :param url: URL регионов, str.
    :param path_vak_dir_sj: Путь к директории для хранения файла, str.
    :param path_are_sj: Полное имя файла, str.
    :return: Json-файл с регионами/населёнными пунктами.
    """
    # Создаём экземпляр класса AreasSJ, по-умолчанию регион "Россия".
    area_sj = AreasSJ(url=url, path_vak_dir_sj=path_vak_dir_sj, path_are_sj=path_are_sj)
    # Получаем словарь с регионами и сохраняем его в json-файл.
    area_sj.request_to_api()


def program_info() -> str:
    """
    Выводит информацию о программе, знакомимся с пользователем.
    :return: Имя, введённое пользователем или пустую строку, если нажата клавиша [Enter], str.
    """
    return input('\nЗдравствуйте! Наша программа поможет Вам изучить имеющиеся вакансии,\n'
                 'предлагаемые работодателями на территории Российской Федерации,\n'
                 'размещённые на сервисах HeadHunter (hh.ru) и SuperJob (superjob.ru).\n\n'
                 'Как Вас зовут? ').strip()


def user_name(name) -> str:
    """
     Выводит приветствие для пользователя.
    :param name: Переданное значение имени пользователя, str.
    :return: Вывод обращения к пользователю, его имени, str.
    """
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


def service_menu_selection() -> str:
    """
    Ввод пункта меню для выбора сервиса.
    :return: Возвращает выбор пользователем пункта меню, str.
    """
    return input(f'\nВыберите сервис, с которого хотите получить информацию.\n'
                 f'Для этого введите:\n'
                 f'   ✅ HeadHunter (hh.ru)........ - 1\n'
                 f'   ✅ SuperJob (superjob.ru).... - 2\n'
                 f'   ❌ Завершить работу программы - 0.\n\n'
                 f'Введите команду: ')


def service_selection(name: str, num_vak: str) -> int:
    """
    Выбираем сервис для получения и вывода данных.
    :param name: Имя пользователя, str.
    :param num_vak: Номер сервиса из меню, введённый пользователем, str.
    :return: Возвращает номер выбранного сервиса (int) или выходит из программы.
    """

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
            num_vak = error_input(f'\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: ')
        else:
            # Возвращение номера выбранного сервиса
            return int(num_vak)


def error_input(value: str) -> str:
    """
    Ввод данных при возникновении ошибки
    :param value: Сообщение для пользователя, str.
    :return:
    """
    return input(value)


def area_vak_input() -> str:
    return input(
        f'\nДля поиска вакансий введите, пожалуйста, название одного региона или города России\n'
        f'без указания кратких обозначений "г.", "с.", "х." и т.д., например:\n'
        f'Москва, Санкт-Петербург, Ростовская область, Ростов-на-Дону.\n'
        f'Введите название региона/населённого пункта: ').strip().lower()


def num_area_input() -> str:
    """
    Меню выбора при поиске id
    :return: Результат ввода пользователем, str
    """
    return input(f'\nМы не нашли, указанный Вами регион/населённый пункт, в имеющейся базе.\n'
                 f'Можем показать вакансии, имеющиеся в России.\n'
                 f'Чтобы продолжить введите одну из следующих команд:\n'
                 f'   ✅ Выбрать другой регион/населённый пункт - 1\n'
                 f'   ✅ Показать вакансии в России............ - 2\n'
                 f'   ❌ Заверишь работу программы............. - 0\n\n'
                 f'Введите команду: ')


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
        # Вводим регион/населённый пункт
        area_vak = area_vak_input()
        # Ищем id на указанном сервисе
        area_id = search_area_id(area_vak, service, name)

        # Если не нашли, указанный пользователем, регион/населённый пункт
        if area_id == area_id_country:
            # Выбор разделов меню
            all_ok_area = False
            while not all_ok_area:
                # Выбор пункта меню
                num_area = num_area_input()
                # Определяем поведение в соответствии с выбранным пунктом меню
                all_ok_area, all_ok = selection_menu_sections_id(num_area, name)
        else:
            all_ok = True
    return area_id


def search_area_id(area_vak: str, service: str, name: str) -> int:
    """
    Поиск id региона/населённого пункта на указанном сервисе.
    :param area_vak: Наименование региона/населённого пункта, str.
    :param service: Строка, указывающая на выбор сервиса: "hh" - HeadHunter, "sj" - SuperJob, str.
    :param name: Имя пользователя, str.
    :return: Возвращает id, если регион/населённый пункт не найден, то id России, int.
    """
    try:
        # Если выбран HeadHunter
        if service == 'hh':
            # Переопределяем экземпляр класса AreasHH с указанием региона, указанного пользователем.
            area_hh = AreasHH(area=area_vak)
            # Получаем id региона/населённого пункта, который указал пользователь.
            return area_hh.extract_area_id()
        # Если выбран SuperJob
        elif service == 'sj':
            # Переопределяем экземпляр класса AreasSJ с указанием региона, указанного пользователем.
            area_sj = AreasSJ(area=area_vak)
            # Получаем id региона/населённого пункта, который указал пользователь.
            return area_sj.extract_area_id()
        # Если указано что-то другое
        else:
            print('Программа не ищет данные на указанном сервисе.')
            exit_program(name)
    except ValueError:
        raise ValueError('Некорректные данные о сервисе.')


def selection_menu_sections_id(num_area: str, name: str) -> tuple:
    """
    Выбор пунктов меню для поиска id региона/населённого пункта.
    :param num_area: Номер пункта меню, str.
    :param name: Имя пользователя, str.
    :return: Флаги в кортеже для работы с циклом while, tuple(bool, bool).
    """
    try:
        match int(num_area):
            # Вывод сообщения, прерывание цикла
            case 1:
                print(f'\n{name}, введите другой регион/населённый пункт.\n')
                return True, False
            # Вывод сообщения, прерывание циклов
            case 2:
                print(f'\n{name}, мы подберём для Вас вакансии на территории России.\n')
                return True, True
            # Завершение работы программы
            case 0:
                exit_program(name)  # Выход из приложения
    except ValueError:
        print('Введена некорректная команда.\n')
        return False, False


def name_vak_word(name: str) -> str:
    """
    Ввод называния вакансии (ключевого слова)
    :param name: Имя пользователя, str.
    :return: Возвращает ключевое слово для поиска вакансии, str.
    """
    return input(f'\n{name}, введите ключевое слово, по которому мы будем осуществлять поиск вакансий.\n'
                 f'Например: водитель, программист, python, java и т.д.\n\n'
                 f'Должность: ').lower()


def show_only_with_salary(name: str) -> bool:
    """
    Определяем нужно ли выводить данные только с зарплатой или все имеющиеся вакансии.
    :param name: Имя пользователя, str.
    :return: Флаг с зарплатой (True) или все (False), bool.
    """
    only_with_salary = False  # Показывать только с зарплатой
    all_ok = False
    while not all_ok:
        # Варианты вакансий (с зарплатой или без неё)
        salary_vak = salary_vak_input()
        # Обработка команд
        only_with_salary, all_ok = all_ok_salary(salary_vak, name)
    return only_with_salary


def salary_vak_input() -> str:
    """
    Функция выбора пункта меню для отображения вакансий всех или только с зарплатой.
    :return: Ввод пользователя, str.
    """
    return input('\nВыберите одну из команд:\n'
                 '   ✅ Показать вакансии только с указанием зарплаты - 1\n'
                 '   ✅ Показать все имеющиеся вакансии.............. - 2\n'
                 '   ❌ Завершить работу программы................... - 0\n\n'
                 'Введите команду: ')


def all_ok_salary(salary_vak: str, name: str) -> tuple:
    """
    Выбор пунктов меню для отображений вакансий только с зарплатой или всех имеющихся.
    :param salary_vak: Варианты вакансий (с зарплатой или без неё), str.
    :param name: Имя пользователя, str.
    :return: Кортеж, содержащий флаги с зарплатой / без зарплаты и завершить/возобновить итерацию, tuple(bool,bool)
    """
    try:
        match int(salary_vak):
            # Запрос данных с api только с зарплатой.
            case 1:
                print(f'\nOK, {name}.\n')
                return True, True
            # Запрос данных с api любых вакансий, в т.ч. без зарплаты.
            case 2:
                print(f'\nOK, {name}.\n')
                return False, True
            # Завершение работы программы.
            case 0:
                exit_program(name)  # Выход из приложения
    except ValueError:
        print('Введена некорректная команда.\n')
        return False, False


def looking_salary(only_with_salary: bool) -> int:
    """
    Выводит размер желаемой заработной платы для поиска вакансий.
    :param only_with_salary: Флаг с зарплатой (True) или все (False), bool.
    :return: Размер желаемой заработной платы, int.
    """
    salary = 0  # Размер искомой зарплаты
    if only_with_salary:
        all_ok = False
        while not all_ok:
            # Ожидаемый размер заработной платы
            salary = salary_input()
            # Обработка ввода
            salary, all_ok = all_ok_salary_input(salary)
    return salary


def salary_input() -> str:
    """
    Ввод размера заработной платы.
    :return: Ожидаемый размер зарплаты, str.
    """
    return input('\nУкажите ожидаемый размер заработной платы (в рублях): ')


def all_ok_salary_input(salary: str) -> tuple:
    """
    Обработка введённого значения ожидаемой зарплаты.
    :param salary: Размер ожидаемой зарплаты, str.
    :return: Размер ожидаемой зарплаты и флаг завершения/продолжения работы цикла.
    """
    try:
        # Размер ожидаемой зарплаты.
        salary = int(salary)
        if salary <= 0:
            print(f'Ошибка ввода данных. Введите целое положительное число.')
            return 0, False
        return salary, True
    except ValueError:
        print(f'Ошибка ввода данных. Введите целое положительное число.')
        return 0, False


def sort_method_input() -> str:
    """
    Функция выбора пункта меню для отображения отсортированных вакансий.
    :return: Ввод пользователя, str.
    """
    return input('\nКак нам отсортировать вакансии?\n'
                 '   ✅ По заработной плате (по убыванию)  - 1\n'
                 '   ✅ По дате публикации (по убыванию).. - 2\n'
                 '   ❌ Завершить работу программы........ - 0\n\n'
                 'Введите команду: ')


def sort_method_int(sort_method: str, name: str) -> tuple:
    """
    Определение метода сортировки: 1 - по размеру зарплаты, 2 - по датам.
    :param sort_method: Выбранный пользователем метод сортировки, str.
    :param name: Имя пользователя, str.
    :return: Код (номер) метода сортировки, tuple (int, bool).
    """
    try:
        match int(sort_method):
            # Метод сортировки по зарплате (от большей к меньшей), выход из цикла.
            case 1:
                return 1, True
            # Метод сортировки датам (от ранних к поздним), выход из цикла.
            case 2:
                return 2, True
            # Завершение работы программы.
            case 0:
                exit_program(name)
    except ValueError:
        print('Введена некорректная команда.\n')
        return 1, False


def choose_sort_method(only_with_salary: bool, name: str) -> int:
    """
    Выбор метода сортировки: 1 - по размеру зарплаты, 2 - по датам.
    :param only_with_salary: Флаг с зарплатой (True) или все (False), bool.
    :param name: Имя пользователя, str.
    :return: Целое число — выбранный метод, int.
    """
    sort_method = 1
    if only_with_salary:
        all_ok = False
        while not all_ok:
            # Ввод команды пользователем
            sort_method = sort_method_input()
            # Обработка команд
            sort_method, all_ok = sort_method_int(sort_method, name)
    return sort_method


def get_job_info(service: str, name: str, name_vak: str, area_id: int, only_with_salary: bool, salary: int,
                 sort_method: int) -> tuple:
    """
    Получение информации о вакансиях при помощи классов VakHH и VakSJ.
    :param service: Строка, указывающая на выбор сервиса: "hh" - HeadHunter, "sj" - SuperJob, str.
    :param name: Имя пользователя, str.
    :param name_vak: Ключевое слово для поиска вакансии, str.
    :param area_id: ID региона для поиска вакансий, int.
    :param only_with_salary: Флаг с зарплатой (True) или все (False) вакансии, bool.
    :param salary: Размер желаемой заработной платы, int.
    :param sort_method: Целое число — выбранный метод сортировки (по датам или размеру зарплаты), int.
    :return: Сохраняет данные в json-файлах, возвращает кол-во вакансий и экз. класса VacPrint, tuple(int, object).
    """
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
            return prof_hh.size_dict, prof_print

        # Если выбран SuperJob
        elif service == 'sj':
            # Создаём экземпляр класса VacSJ - вакансии с superjob.ru.
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
            return prof_sj.size_dict, prof_print

        # Если указано что-то другое
        else:
            print('Программа не ищет данные на указанном сервисе.')
            exit_program(name)
    except ValueError:
        raise ValueError('Некорректные данные о сервисе.')


def reselect_position() -> str:
    """
    Выбор команды меню (повторный ввод должности или выход из программы).
    :return: Данные, введённые пользователем, str.
    """
    return input('\nВыберите одну из команд:\n'
                 '   ✅ Ввести наименование должности заново - 1\n'
                 '   ❌ Заверишь работу программы........... - 0\n\n'
                 'Введите команду: ')


def print_vacancies(service: str, count_vak: str, size_dict_vak: int, prof_print: object, one_each: int = 1) -> bool:
    """
    Вывод вакансий на экран.
    :param service: Строка, указывающая на выбор сервиса: "hh" - HeadHunter, "sj" - SuperJob, str.
    :param count_vak: Количество вакансий, выбранных пользователем, str.
    :param size_dict_vak: Найденное количество вакансий, int.
    :param prof_print: Экземпляр класса вывода вакансий в терминал, object.
    :param one_each: Вывод вакансий: 1 - по одной, другое - все сразу, int.
    :return: Флаг, который при выполнении задачи, прекращает итерации цикла, bool.
    """

    # Проверка корректности введённых данных
    if not count_vak.isdigit() or int(count_vak) > size_dict_vak:
        # Количество вакансий для вывода в случае некорректного ввода (все).
        count_vak = size_dict_vak
        print(f'\nВы ввели некорректные данные, '
              f'поэтому мы покажем Вам все найденные вакансии ({count_vak} шт.).\n')

        # Выводим информацию
        prof_print.vacancies_print(count_vak, service, one_each)
        return True

    else:
        # Количество вакансий, заданное пользователем, для вывода.
        count_vak = int(count_vak)
        print(f'\nНиже будут представлены вакансии, '
              f'которые мы нашли по Вашему запросу ({count_vak} шт.).\n')

        # Выводим информацию
        prof_print.vacancies_print(count_vak, service, one_each)
        return True


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
        # Найденное количество вакансий
        size_dict_vak, prof_print = get_job_info(service, name, name_vak, area_id, only_with_salary, salary,
                                                 sort_method)
        # Если не найдено ни одной вакансии по запросу пользователя.
        if size_dict_vak == 0:
            # Обработка команд
            all_ok_position = False
            while not all_ok_position:
                # Выбор команды меню (повторный ввод должности или выход из программы).
                commands_prg = reselect_position()
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
                    print(f'\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: ')
                    all_ok_position = False
        else:
            # Вывод информации о вакансиях
            count_vak = input(f'Какое количество вакансий из найденных '
                              f'({size_dict_vak} шт.) Вы бы хотели увидеть? ')

            all_ok = print_vacancies(service, count_vak, size_dict_vak, prof_print)
