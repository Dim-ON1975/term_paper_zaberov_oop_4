from src.utils.constants import ID_RUSSIA_HH, ID_RUSSIA_SJ
from src.utils.utilites import user_name, loading_regions_hh, loading_regions_sj, service_selection, \
    choosing_region, name_vak_word, show_only_with_salary, looking_salary, choose_sort_method, displaying_jobs_screen

if __name__ == '__main__':

    # Загружаем справочники регионов
    loading_regions_hh()  # hh.ru
    loading_regions_sj()  # superjob.ru

    # Выводим информацию о работе программы, знакомство с пользователем
    name = user_name()

    # Выбираем сервис для получения данных или завершаем работу программы
    num_vak = service_selection(name)

    # Блок для работы с ресурсами HeadHunter (hh.ru).
    if num_vak == 1:
        # Выбираем id региона/населённого пункта для получения данных о вакансиях на hh.ru.
        area_id = choosing_region('hh', name, ID_RUSSIA_HH)

        # Блок получения данных по запросу пользователя.
        # Получаем название должности, которую ищет пользователь.
        name_vak = name_vak_word(name)

        # Получаем сведения об отображении вакансий с зарплатой или всех имеющихся.
        only_with_salary = show_only_with_salary(name)

        # Получаем сведения о размере желаемой заработной платы
        salary = looking_salary(only_with_salary, name)

        # Получаем данные о методе сортировки: 1 - по датам, 2 - по размеру зарплаты.
        sort_method = choose_sort_method(only_with_salary, name)

        # Выводим данные о вакансиях на экран.
        displaying_jobs_screen('hh', name, name_vak, area_id, only_with_salary, salary, sort_method)

    # Блок для работы с ресурсами SuperJob (superjob.ru).
    else:
        # Выбираем id региона/населённого пункта для получения данных о вакансиях на superjob.ru.
        area_id = choosing_region('sj', name, ID_RUSSIA_SJ)

        # Блок получения данных по запросу пользователя.
        # Получаем название должности, которую ищет пользователь.
        name_vak = name_vak_word(name)

        # Получаем сведения об отображении вакансий с зарплатой или всех имеющихся=.
        only_with_salary = show_only_with_salary(name)

        # Получаем сведения о размере желаемой заработной платы
        salary = looking_salary(only_with_salary, name)

        # Получаем данные о методе сортировки: 1 - по датам, 2 - по размеру зарплаты.
        sort_method = choose_sort_method(only_with_salary, name)

        # Выводим данные о вакансиях на экран.
        displaying_jobs_screen('sj', name, name_vak, area_id, only_with_salary, salary, sort_method)
