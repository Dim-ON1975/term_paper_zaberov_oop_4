from src.utils.areas import AreasHH
from src.utils.utilites import user_name, exit_program
from src.utils.vacancies import VacHH

if __name__ == '__main__':

    # Создаём экземпляр класса AreasHH, по-умолчанию регион "Россия".
    area_hh = AreasHH()
    # Получаем словарь с регионами и сохраняем его в json-файл.
    area_hh.request_to_api()

    # Выводим информацию о работе программы.
    # Знакомимся с пользователем.
    name = input('\nЗдравствуйте! Наша программа поможет Вам изучить имеющиеся вакансии,\n'
                 'предлагаемые работодателями на территории Российской Федерации,\n'
                 'размещённые на сервисах HeadHunter (hh.ru) и SuperJob (superjob.ru).\n\n'
                 'Как Вас зовут? ').strip()
    # Вывод обращения к пользователю.
    name = user_name(name)

    # Выбираем сервис для получения данных или завершаем работу программы
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
                case 1:
                    print(f'\n{name}, Вы выбрали HeadHunter (hh.ru). 👌\n')
                case 2:
                    print(f'\n{name}, Вы выбрали SuperJob (superjob.ru). 👌\n')
                case 0:
                    exit_program(name)  # Выход из приложения
        except ValueError:
            num_vak = input(f'\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: ')
        else:
            num_vak = int(num_vak)
            all_ok = True

        if num_vak == 1:
            # Блок для работы с ресурсами HeadHunter (hh.ru).
            # Выбираем id региона/населённого пункта для получения данных о вакансиях на hh.ru
            all_ok = False
            while not all_ok:
                # Регион, который указывает пользователь.
                area_vak = input(
                    f'\nДля поиска вакансий введите, пожалуйста, название одного региона или города России\n'
                    f'без указания кратких обозначений "г.", "с.", "х." и т.д., например:\n'
                    f'Москва, Санкт-Петербург, Ростовская область, Ростов-на-Дону.\n'
                    f'Введите название региона/населённого пункта: ').strip().lower()

                # Переопределяем экземпляр класса AreasHH с указанием региона, указанного пользователем.
                area_hh = AreasHH(area_vak)

                # Получаем id региона/населённого пункта, который указал пользователь.
                area_id = area_hh.extract_area_id()

                # Если не нашли, указанный пользователем, регион/населённый пункт
                if area_id == 113:
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
                                case 1:
                                    print(f'\n{name}, введите другой регион/населённый пункт.\n')
                                    all_ok_area = True
                                case 2:
                                    print(f'\n{name}, мы подберём для Вас вакансии на территории России.\n')
                                    all_ok_area = True
                                    all_ok = True
                                case 0:
                                    exit_program(name)  # Выход из приложения
                        except ValueError:
                            num_area = input(f'\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: ')
                else:
                    all_ok = True

            # Блок получения данных по запросу пользователя.
            # Получаем название должности, которую ищет пользователь.
            name_vak = input(
                f'\n{name}, введите ключевое слово, по которому мы будем осуществлять поиск вакансий.\n'
                f'Например: водитель, программист, python, java и т.д.\n\n'
                f'Должность: ').lower()

            only_with_salary = False  # Показывать только с зарплатой
            salary_vak = input('\nВыберите одну из команд:\n'
                               '   ✅ Показать вакансии только с указанием зарплаты - 1\n'
                               '   ❎ Показать все имеющиеся вакансии.............. - 2\n'
                               '   ❌ Завершить работу программы................... - 0\n\n'
                               'Введите команду: ')
            all_ok = False
            while not all_ok:
                # Обработка команд
                try:
                    match int(salary_vak):
                        case 1:
                            print(f'\nOK, {name}.\n')
                            only_with_salary = True
                            all_ok = True
                        case 2:
                            print(f'\nOK, {name}.\n')
                            all_ok = True
                        case 0:
                            exit_program(name)  # Выход из приложения
                except ValueError:
                    salary_vak = input(f'\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: ')

            salary = 0  # Размер искомой зарплаты
            if only_with_salary:
                salary = input('\nУкажите ожидаемый размер заработной платы (в рублях): ')
                all_ok = False
                while not all_ok:
                    # Обработка команд
                    try:
                        salary = int(salary)
                        if salary <= 0:
                            salary = 0
                        all_ok = True
                    except ValueError:
                        salary = input(f'\n❗{name}, нужно ввести целое положительное число: ')

            sort_method = 1  # Метод сортировки: 1 - по датам, 2 - по размеру зарплаты
            if only_with_salary:
                sort_method = input('\nКак нам отсортировать вакансии?\n'
                                    '   ✅ По заработной плате (от большей к меньшей)  - 1\n'
                                    '   ❎ По дате публикации (от "свежих" к "старым") - 2\n'
                                    '   ❌ Завершить работу программы................. - 0\n\n'
                                    'Введите команду: ')
                all_ok = False
                while not all_ok:
                    # Обработка команд
                    try:
                        match int(sort_method):
                            case 1:
                                sort_method = 1
                                all_ok = True
                            case 2:
                                sort_method = 2
                                all_ok = True
                            case 0:
                                exit_program(name)  # Выход из приложения
                    except ValueError:
                        sort_method = input(f'\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: ')

            all_ok = False
            while not all_ok:
                # Создаём экземпляр класса VacHH - вакансии с hh.ru.
                if only_with_salary or salary != 0:
                    prof_hh = VacHH(position=name_vak, area=area_id, only_with_salary=only_with_salary, salary=salary,
                                    sort_method=sort_method)
                else:
                    prof_hh = VacHH(position=name_vak, area=area_id)

                # Получаем все вакансии в соответствии с запросом пользователя,
                # сохраняя их в json-файлы.
                prof_hh.vacancies_all()
                if prof_hh.size_dict == 0:
                    commands_prg = input('\nВыберите одну из команд:\n'
                                         '   ✅ Ввести наименование должности заново - 1\n'
                                         '   ❌ Заверишь работу программы........... - 0\n\n'
                                         'Введите команду: ')
                    # Обработка команд
                    try:
                        match int(commands_prg):
                            case 1:
                                name_vak = input(f'\n{name}, введите должность: ').lower()
                            case 0:
                                exit_program(name)  # Выход из приложения
                    except ValueError:
                        commands_prg = input(f'\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: ')
                else:
                    # Вывод информации о вакансиях
                    count_vak = input(f'Какое количество вакансий из найденных '
                                      f'({prof_hh.size_dict} шт.) Вы бы хотели увидеть? ')

                    # Проверка корректности введённых данных
                    if not count_vak.isdigit() or int(count_vak) > prof_hh.size_dict:
                        # Количество вакансий для вывода в случае некорректного ввода (все).
                        count_vak = prof_hh.size_dict
                        print(f'\nВы ввели некорректные данные, '
                              f'поэтому мы покажем Вам все найденные вакансии ({count_vak} шт.).\n')
                        # Выводим информацию
                        prof_hh.vacancies_print(count_vak)
                        all_ok = True
                    else:
                        # Количество вакансий, заданное пользователем, для вывода.
                        count_vak = int(count_vak)
                        print(f'\nНиже будут представлены вакансии, '
                              f'которые мы нашли по Вашему запросу ({count_vak} шт.).\n')
                        # Выводим информацию
                        prof_hh.vacancies_print(count_vak)
                        all_ok = True
    else:
        # Блок для работы с ресурсами SuperJob (superjob.ru).
        pass
