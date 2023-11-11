import json
import os
import sys
from abc import ABC, abstractmethod
import time
from datetime import datetime

import requests
from tqdm import trange
import re

from src.utils.constants import PATH_VAK_HH, SUPERJOB_API_KEY, PATH_VAK_SJ, ID_RUSSIA_HH, ID_RUSSIA_SJ


class Vacancies(ABC):
    """
    Абстрактный класс выполнения и обработки запросов по api
    для поиска, обработки, фильтрации и вывода вакансий.
    """

    @abstractmethod
    def request_to_api(self) -> str:
        pass

    @abstractmethod
    def vacancies_all(self) -> None:
        pass

    @abstractmethod
    def vacancies_print(self, count_vak) -> None:
        pass

    @abstractmethod
    def data_print(self, data: list) -> None:
        pass

    @abstractmethod
    def list_sort_salary(self, list_operations: list) -> list:
        pass

    @abstractmethod
    def __doc__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class VacHH(Vacancies):
    def __init__(self, position: str, area: int = ID_RUSSIA_HH, only_with_salary: bool = False, salary: int = 0,
                 per_page: int = 100, sort_method: int = 2) -> None:
        self.__url = 'https://api.hh.ru/vacancies'
        self.position = str(position)  # Текст фильтра
        self.area = area  # Поиск по-умолчанию осуществляется по вакансиям России (id=113)
        self.only_with_salary = only_with_salary  # Показывать вакансии только с указанием зарплаты или все
        self.salary = salary  # Ожидаемый размер заработной платы
        self.per_page = per_page  # Кол-во вакансий на 1 странице
        self.size_dict = 0  # Счётчик количества словарей с вакансиями
        self.sort_method = sort_method  # Метод сортировки: 1 - по датам, 2 - по размеру зарплаты

    def request_to_api(self, page: int = 0) -> str:
        """
        Получение запроса по api
        :page: Индекс страницы поиска HH.
        :return: ответ запроса, <class 'requests.models.Response'>.
        """
        try:
            if self.salary != 0:
                # С фильтрацией по размеру заработной платы
                params = {
                    'text': self.position,  # Текст фильтра
                    'area': self.area,  # Поиск по-умолчанию осуществляется по вакансиям России (id=113)
                    'page': page,
                    'salary': self.salary,
                    'only_with_salary': self.only_with_salary,
                    'per_page': self.per_page
                }
            else:
                # Без фильтрации по размеру заработной платы
                params = {
                    'text': self.position,  # Текст фильтра
                    'area': self.area,  # Поиск по-умолчанию осуществляется по вакансиям России (id=113)
                    'page': page,
                    'per_page': self.per_page
                }

            # Посылаем запрос к API
            data_prof = requests.get(url=self.__url, params=params).text
            return data_prof
        except Exception as e:
            raise Exception(f'Ошибка при получении данных с {self.__url}. {e}')

    def vacancies_all(self) -> None:
        """
        Считывает первые 2000 вакансий и постранично (по 100 шт.) сохраняет их в json-файлы.
        """
        print('Мы собираем для Вас информацию'
              ' о вакансиях в указанном регионе/населённом пункте...')
        # Очищаем папку с файлами, хранящими устаревшие данные
        self.delete_files_in_folder(PATH_VAK_HH)
        try:
            for page in trange(20, desc='Подождите, пожалуйста. Анализируем страницы', initial=1):
                # Преобразуем текст ответа запроса в словарь Python.
                js_obj = json.loads(self.request_to_api(page))

                # Получем количество записей
                self.size_dict += len(js_obj['items'])

                # Создаём номер файла для адекватной последовательной сортировки в дальнейшем
                if page < 10:
                    page_num = '0' + str(page)
                else:
                    page_num = str(page)
                # Создаём новый документ, записываем в него ответ запроса
                self.save_to_json(js_obj['items'], os.path.join(PATH_VAK_HH, f'vakhh_{page_num}.json'))

                # Проверка на последнюю страницу, если вакансий меньше 2000
                if (js_obj['pages'] - page) <= 1:
                    break

                # Задержка, чтобы не нагружать сервисы hh.
                time.sleep(0.03)

            # Вывод данных о количестве вакансий
            if self.size_dict != 0:
                print(f'\nПо вашему запросу на hh.ru найдено {self.size_dict} вакансий.\n')
            else:
                print('\nИзвините. Мы ничего не нашли по Вашему запросу. Попробуйте его сформулировать по-другому.\n')
                # Удаляем пустой файл из папки data\hh
                self.delete_files_in_folder(PATH_VAK_HH)
        except KeyError as e:
            raise KeyError(f'Ошибка обращения к полученным данным. {e}')

    def vacancies_print(self, count_vak) -> None:
        """
        Выводит вакансии на экран в количестве, заданном пользователем.
        :param count_vak: Необходимое количество, int.
        :return: Выводит на экран информацию о вакансиях.
        """
        # Пустой список
        data = []
        # Перемещаемся по файлам в папке, считывая значения, объединяя их в один список словарей.
        for filename in os.listdir(PATH_VAK_HH):
            file_path = os.path.join(PATH_VAK_HH, filename)
            try:
                if os.path.isfile(file_path):
                    # Считываем данные из всех файлов в директории, объединяя их в один список.
                    data += self.load_json(file_path)
            except Exception as e:
                print(f'Ошибка при открытии и/или чтении файла {file_path}. {e}')
        # Сортируем список по датам или зарплате, выводя, заданное пользователем, количество словарей.
        if self.sort_method == 1:
            data = self.list_sort_salary(data)[:count_vak]
        else:
            data = self.list_sort_date(data)[:count_vak]
        # Выводим данные на экран из списка, в котором отсортированы словари.
        self.data_print(data)
        # Выводим информацию об окончании вывода.
        print('----------------------\n'
              'Выведены все вакансии.')

    def data_print(self, data: list) -> None:
        """
        Выводит данные на экран.
        :param data: Список словарей с данными о вакансиях, list.
        :return: Выводит на экран вакансии, отсортированные по дате.
        """
        # Анализируем список словарей, выводим необходимые данные на экран.

        for c_enum, dict_vak in enumerate(data, start=1):

            # Номер, дата публикации вакансии, наименование должности.
            # Номер.
            enum = '№ ' + str(c_enum) + ','  # номер
            # Дата.
            date_publ = dict_vak["published_at"].split('T')
            date_publ = ' от ' + date_publ[0][-2:] + '.' + date_publ[0][5:7] + '.' + date_publ[0][:4] + ': '
            # Должность.
            name = dict_vak["name"] + '.'

            # Вывод строки с данными ('заголовок вакансии').
            print('-' * (len(enum) + len(date_publ) + len(name)))
            print(f'{enum}{date_publ}{name}')
            print('-' * (len(enum) + len(date_publ) + len(name)))

            # Объявляем словарь, определяем структуру данных.
            # Номерация ключей используется их сортировки во время вывода на экран (номера не выводятся).
            vacancy = {
                '01 Работодатель': 'нет данных.',
                '02 Населённый пункт': 'нет данных.',
                '03 Адрес': 'нет данных.',
                '04 Зарплата': 'нет данных.',
                '05 График работы': 'нет данных.',
                '06 Занятость': 'нет данных.',
                '07 Опыт работы': 'нет данных.',
                '08 Требования к соискателю': 'нет данных.',
                '09 Обязанности': 'нет данных.',
                '10 Подробнее здесь (URL)': 'нет данных.'
            }

            # Заполняем словарь данными, проверяя наличие необходимых ключей.
            # Ключи с однотипным ('двойным') уровнем вложенности.
            keys = {
                '01 Работодатель': ["employer", "name"],
                '02 Населённый пункт': ["area", "name"],
                '03 Адрес': ["address", "raw"],
                '05 График работы': ["schedule", "name"],
                '06 Занятость': ["employment", "name"],
                '07 Опыт работы': ["experience", "name"],
                '08 Требования к соискателю': ["snippet", "requirement"],
                '09 Обязанности': ["snippet", "responsibility"],
            }

            # Заполняем словарь vacancy по ключам 01-03, 05-09,
            # имеющим "двойной" уровень вложенности.
            for key_0, key in keys.items():
                self.two_levels(dict_vak, vacancy, key_0, key[0], key[1])

            # Зарплата.
            # Получаем данные о зарплате (от и до)
            sal_from = self.two_levels_salary(dict_vak, "salary", "from", 'от')
            sal_to = self.two_levels_salary(dict_vak, "salary", "to", 'до')
            # Помещаем данные в словарь, удаляя лишние пробелы
            if sal_from != '' or sal_to != '':
                vacancy['04 Зарплата'] = self.del_space(
                    f'{str(sal_from)} {str(sal_to)} ({dict_vak["salary"]["currency"]}).')

            # URL вакансии
            self.one_level(dict_vak, vacancy, '10 Подробнее здесь (URL)', "alternate_url")

            # Выводим словарь на экран, удаляя номера у ключей, лишние символы и выполняя переносы длинных строк.
            for key, value in sorted(vacancy.items()):
                if key == "08 Требования к соискателю":
                    print(f"  {key[3:]}: {self.break_down_lines(self.del_html_tag(self.del_space(value)), 130, 27)}")
                elif key == "09 Обязанности":
                    print(f"  {key[3:]}: {self.break_down_lines(self.del_html_tag(self.del_space(value)), 140, 15)}")
                else:
                    print(f"  {key[3:]}: {self.del_html_tag(self.del_space(value))}")

            # Поочерёдный вывод вакансий и завершение работы программы
            i = input("\n ✅ Нажмите [Enter], чтобы продолжить\n"
                      " ❌ Введите 'q', чтобы выйти из программы: ").strip().lower()
            if not i:
                continue
            elif i == 'q':
                print(f'\nДо свидания! 👋')
                sys.exit('Работа программы завершена.\n')

    @staticmethod
    def two_levels(dict_vak: dict, vacancy: dict, key_0: str, key_1: str, key_2: str) -> None:
        """
        Проверка и обработка данных из исходного словаря.
        Два уровня вложенности ключей в словаре.
        :param dict_vak: Словарь вакансии (анализируемый), dict.
        :param vacancy: Словарь вакансии (заполняемый), dict.
        :param key_0: Ключ создаваемого словаря, str.
        :param key_1: Ключ 1-го уровня вложенности анализируемого словаря, str.
        :param key_2: Ключ 2-го уровня вложенности анализируемого словаря, str.
        :return: Добавляет в словарь пару ключ: значение.
        """
        try:
            if all(dict_vak.get(key_1).get(key_2)):
                vacancy[key_0] = dict_vak[key_1][key_2]
        except (TypeError, AttributeError):
            pass

    @staticmethod
    def two_levels_salary(dict_vak: dict, key_1: str, key_2: str, from_to: str) -> str:
        """
        Проверка и обработка данных по зарплате из исходного словаря.
        Два уровня вложенности ключей в словаре.
        :param dict_vak: Словарь вакансии (анализируемый), dict.
        :param key_1: Ключ 1-го уровня вложенности анализируемого словаря, str.
        :param key_2: Ключ 2-го уровня вложенности анализируемого словаря, str.
        :param from_to: Строки 'от' или 'до', str.
        :return: Выводит данные о зарплате в виде строки, str.
        """
        str_salary = ''
        try:
            if all(str(dict_vak.get(key_1).get(key_2))):
                if str(dict_vak.get(key_1).get(key_2)) != 'None':
                    str_salary = f'{from_to} {str(dict_vak[key_1][key_2])}'
        except (TypeError, AttributeError):
            pass
        return str_salary

    @staticmethod
    def one_level(dict_vak: dict, vacancy: dict, key_0: str, key_1: str) -> None:
        """
        Проверка и обработка данных из исходного словаря.
        Два уровня вложенности ключей в словаре.
        :param dict_vak: Словарь вакансии (анализируемый), dict.
        :param vacancy: Словарь вакансии (заполняемый), dict.
        :param key_0: Ключ создаваемого словаря, str.
        :param key_1: Ключ 1-го уровня вложенности анализируемого словаря, str.
        :return: Добавляет в словарь пару ключ: значение.
        """
        try:
            if all(dict_vak.get(key_1)):
                vacancy[key_0] = dict_vak[key_1]
        except (TypeError, AttributeError):
            pass

    @staticmethod
    def del_space(txt: str) -> str:
        """
        Удаляет лишние пробелы в тексте.
        :param txt: Строка для анализа, str.
        :return: Строка с одинарными пробелами, str.
        """
        # Удаляем лишние пробелы в тексте (в начале, в конце, двойные, тройные),
        # оставляя по одному между словами.
        txt = ' '.join(txt.strip().split())
        # txt = re.sub(r'\s+', ' ', txt.strip())
        return txt

    @staticmethod
    def del_html_tag(txt: str) -> str:
        """
        Удаляет все html-теги из текста.
        :param txt: Строка для анализа, str.
        :return: Строка без html-тегов, str.
        """
        txt = re.sub(r'\<[^>]*\>', '', txt)
        return txt

    @staticmethod
    def list_sort_date(list_operations: list) -> list:
        """
        Возвращает список словарей, сортированный по дате и времени
        в обратном порядке.
        :param list_operations: Несортированный список словарей, list.
        :return: Сортированный список словарей, list.
        """
        # Сортируем словари в списке по дате и времени в обратном порядке.
        list_operations = sorted(list_operations,
                                 key=lambda x: datetime.strptime(x['published_at'], '%Y-%m-%dT%H:%M:%S%z'),
                                 reverse=True)
        return list_operations

    @staticmethod
    def key_sort_salary(my_dict: dict):
        """
        Условия сортировки для метода сортировки list_sort_salary.
        :param my_dict: Словарь из списка словарей, dict.
        :return: Ключ для сортировки.
        """
        if my_dict['salary']['from'] is not None:
            return my_dict['salary']['from']
        else:
            return my_dict['salary']['to']

    def list_sort_salary(self, list_operations: list) -> list:
        """
        Возвращает список словарей, сортированный по заработной плате
        от большей к меньшей.
        :param list_operations: Несортированный список словарей, list.
        :return: Сортированный список словарей, list.
        """
        # Сортируем словари в списке по зарплате в обратном порядке.
        list_operations = sorted(list_operations, key=self.key_sort_salary, reverse=True)
        return list_operations

    @staticmethod
    def save_to_json(data: dict, path: str) -> None:
        """
        Сохраняет данные в json-файл.
        :param data: Словарь с данными, dict
        :return: Ничего не возвращает.
        """
        with open(path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_json(path_json: str) -> list:
        """
        Чтение данных из файла json и возвращение структуры.
        :param path_json: Путь к файлу, str.
        :return: Структура файла (список словарей).
        """
        # открываем файл на чтение
        with open(path_json, 'r', encoding='utf-8') as file:
            # считываем список словарей из файла
            content = json.load(file)
        return content

    @staticmethod
    def delete_files_in_folder(folder_path):
        """
        Удаление файлов из папки.
        :param folder_path: Путь к папке, str.
        :return:
        """
        # Определяем полные имена файлов в директории
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Удаляем файл
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f'Ошибка при удалении файла {file_path}. {e}')

    @staticmethod
    def break_down_lines(value: str, len_cut: int = 100, count_space: int = 15) -> str:
        """
        Разбивает длинные строки на несколько строк при помощи \n.
        :param value: Длинная строка без переносов, str.
        :param len_cut: Примерное количество символов для разбивки строки, int.
        :param count_space: Количество пробелов (отступ) слева, int.
        :return: Строка, разделённая на несколько строк, str.
        """
        # Итоговая строка
        result_string = ""
        if len(value) > len_cut:
            # Нижняя граница среза строки.
            lower_cut = 0
            # Количество "целых" строк, которые нужно вывести на экран.
            count_iter = len(value) // len_cut
            if count_iter == 1:
                # Находим индекс последнего пробела в подстроке.
                index_space = value[:len_cut].rfind(' ')
                # "Склеиваем" одну (полную) и вторую (неполную) строки.
                result_string = value[:index_space] + '\n' + ' ' * count_space + value[index_space + 1:]
            else:
                # Список строк
                list_str = []
                for i in range(1, count_iter + 1):
                    # Если не дошли до конца строки (последней подстроки для переноса)
                    if i <= count_iter:
                        # Находим индекс последнего пробела в подстроке.
                        index_space = value[lower_cut:i * len_cut].rfind(' ')
                        # Добавляем строку в список
                        list_str.append(value[lower_cut:lower_cut + index_space])
                        # Добавляем в конец подстроки вместо пробела символ переноса.
                        result_string += value[lower_cut:lower_cut + index_space] + '\n'
                        # Увеличиваем нижнюю границу на длину подстроки.
                        lower_cut = len(result_string) - 1
                    else:
                        # Последняя "неполная" строка
                        list_str.append(value[lower_cut:])
                # Разделитель (отступ)
                space = '\n' + ' ' * count_space
                result_string = space.join(list_str)
        else:
            result_string = value
        return result_string

    def __str__(self) -> str:
        return f'Получение, обработка (включая сортировку) и вывод данных с сервиса hh.ru по API {self.__url}'

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}('{self.__url}', {self.position},"
                f"{self.area}, {self.only_with_salary}, {self.salary}, "
                f"{self.per_page}, {self.size_dict}, {self.sort_method})")


class VacSJ(Vacancies):
    def __init__(self, position: str, area: int = ID_RUSSIA_SJ, only_with_salary: bool = False, salary: int = 0,
                 per_page: int = 100, sort_method: int = 2) -> None:
        self.__url = 'https://api.superjob.ru/2.0/vacancies/'
        self.keyword = str(position)  # Текст фильтра
        self.area = area  # Поиск по-умолчанию осуществляется по вакансиям России (id=1)
        self.only_with_salary = only_with_salary  # Показывать вакансии только с указанием зарплаты или все
        self.salary = salary  # Ожидаемый размер заработной платы
        self.per_page = per_page  # Кол-во вакансий на 1 странице
        self.size_dict = 0  # Счётчик количества словарей с вакансиями
        self.sort_method = sort_method  # Метод сортировки: 1 - по датам, 2 - по размеру зарплаты

    def request_to_api(self, page: int = 0) -> str:
        """
        Получение запроса по api
        :page: Индекс страницы поиска HH.
        :return: ответ запроса, <class 'requests.models.Response'>.
        """
        try:
            # Если выбран конкретный город или регион
            if self.area != 1:
                if self.salary != 0:
                    # С фильтрацией по размеру заработной платы
                    if self.only_with_salary:
                        self.only_with_salary = 1
                    params = {
                        'keyword': self.keyword,  # Текст фильтра
                        'town': self.area,
                        'page': page,
                        'count': self.per_page,
                        'payment_from': self.salary,
                        'payment_to': self.salary * 5,
                        'no_agreement': self.only_with_salary,
                    }
                else:
                    # Без фильтрации по размеру заработной платы
                    params = {
                        'keyword': self.keyword,  # Текст фильтра
                        'town': self.area,
                        'page': page,
                        'count': self.per_page,
                    }
            else:
                # Поиск по России
                if self.salary != 0:
                    # С фильтрацией по размеру заработной платы
                    if self.only_with_salary:
                        self.only_with_salary = 1
                    params = {
                        'keyword': self.keyword,  # Текст фильтра
                        'c': self.area,  # Поиск по-умолчанию осуществляется по вакансиям России (id=1)
                        'page': page,
                        'count': self.per_page,
                        'payment_from': self.salary,
                        'payment_to': self.salary * 5,
                        'no_agreement': self.only_with_salary,
                    }
                else:
                    # Без фильтрации по размеру заработной платы
                    params = {
                        'keyword': self.keyword,  # Текст фильтра
                        'c': self.area,  # Поиск по-умолчанию осуществляется по вакансиям России (id=1)
                        'page': page,
                        'count': self.per_page,
                    }

            # Посылаем запрос к API
            headers = {'X-Api-App-Id': SUPERJOB_API_KEY}
            data_prof = requests.get(url=self.__url, headers=headers, params=params).text
            return data_prof
        except Exception as e:
            raise Exception(f'Ошибка при получении данных с {self.__url}. {e}')

    def vacancies_all(self, page: int = 0) -> None:
        """
        Считывает первые 500 вакансий и постранично (по 100 шт.) сохраняет их в json-файлы.
        """
        print('Мы собираем для Вас информацию'
              ' о вакансиях в указанном регионе/населённом пункте...')
        try:
            # Очищаем папку с файлами, хранящими устаревшие данные
            self.delete_files_in_folder(PATH_VAK_SJ)
            for page in trange(5, desc='Подождите, пожалуйста. Анализируем страницы', initial=1):
                # Преобразуем текст ответа запроса в словарь Python.
                js_obj = json.loads(self.request_to_api(page))

                # Получем количество записей
                self.size_dict += len(js_obj['objects'])

                # Создаём номер файла для адекватной последовательной сортировки в дальнейшем
                if page < 10:
                    page_num = '0' + str(page)
                else:
                    page_num = str(page)
                # Создаём новый документ, записываем в него ответ запроса
                self.save_to_json(js_obj['objects'], os.path.join(PATH_VAK_SJ, f'vaksj_{page_num}.json'))

                # Проверка на последнюю страницу, если вакансий меньше 500
                if js_obj['total'] < self.per_page:
                    break

                # Задержка, чтобы не нагружать сервисы sj.
                time.sleep(0.03)

            # Вывод данных о количестве вакансий
            if self.size_dict != 0:
                print(f'\nПо вашему запросу на superjob.ru найдено {self.size_dict} вакансий.\n')
            else:
                print('\nИзвините. Мы ничего не нашли по Вашему запросу. Попробуйте его сформулировать по-другому.\n')
                # Удаляем пустой файл из папки data\sj
                self.delete_files_in_folder(PATH_VAK_SJ)
        except KeyError as e:
            raise KeyError(f'Ошибка обращения к полученным данным. {e}')

    def vacancies_print(self, count_vak) -> None:
        """
                Выводит вакансии на экран в количестве, заданном пользователем.
                :param count_vak: Необходимое количество, int.
                :return: Выводит на экран информацию о вакансиях.
                """
        # Пустой список
        data = []
        # Перемещаемся по файлам в папке, считывая значения, объединяя их в один список словарей.
        for filename in os.listdir(PATH_VAK_SJ):
            file_path = os.path.join(PATH_VAK_SJ, filename)
            try:
                if os.path.isfile(file_path):
                    # Считываем данные из всех файлов в директории, объединяя их в один список.
                    data += self.load_json(file_path)
            except Exception as e:
                print(f'Ошибка при открытии и/или чтении файла {file_path}. {e}')
        # Сортируем список по датам или зарплате, выводя, заданное пользователем, количество словарей.
        if self.sort_method == 1:
            data = self.list_sort_salary(data)[:count_vak]
        else:
            data = self.list_sort_date(data)[:count_vak]
        # Выводим данные на экран из списка, в котором отсортированы словари.
        self.data_print(data)
        # Выводим информацию об окончании вывода.
        print('----------------------\n'
              'Выведены все вакансии.')

    def data_print(self, data: list) -> None:
        """
                Выводит данные на экран.
                :param data: Список словарей с данными о вакансиях, list.
                :return: Выводит на экран вакансии, отсортированные по дате.
                """
        # Анализируем список словарей, выводим необходимые данные на экран.

        for c_enum, dict_vak in enumerate(data, start=1):

            # Номер, дата публикации вакансии, наименование должности.
            # Номер.
            enum = '№ ' + str(c_enum) + ','  # номер
            # Дата (unix)
            date_publ = time.strftime("%d.%m.%Y", time.gmtime(float(dict_vak["date_published"])))
            date_publ = ' от ' + date_publ + ': '
            # Должность.
            name = dict_vak["profession"] + '.'

            # Вывод строки с данными ('заголовок вакансии').
            print('-' * (len(enum) + len(date_publ) + len(name)))
            print(f'{enum}{date_publ}{name}')
            print('-' * (len(enum) + len(date_publ) + len(name)))

            # Объявляем словарь.
            vacancy = {}
            # Заполняем словарь данными, проверяя наличие необходимых ключей.
            # Номерация ключей используется их сортировки во время вывода на экран.
            for key in dict_vak:
                match key:
                    # Работодатель, регион/населённый пункт
                    case 'client':
                        try:
                            if len(dict_vak["client"]) > 1:
                                vacancy['01 Работодатель'] = self.two_levels(dict_vak["client"]["title"])
                                vacancy['02 Населённый пункт'] = self.three_levels(dict_vak["client"],
                                                                                   dict_vak["town"]["title"])
                            else:
                                vacancy['01 Работодатель'] = 'нет данных.'
                                vacancy['02 Населённый пункт'] = 'нет данных.'
                        except TypeError:
                            vacancy['01 Работодатель'] = 'нет данных.'
                            vacancy['02 Населённый пункт'] = 'нет данных.'
                    # Адрес
                    case 'address':
                        try:
                            vacancy['03 Адрес'] = dict_vak["address"]
                        except TypeError:
                            vacancy['03 Адрес'] = 'нет данных.'
                    # Зарплата
                    case 'payment_from':
                        try:
                            # от и до
                            sal_from = self.print_data_val_two(dict_vak["payment_from"])
                            sal_to = self.print_data_val_two(dict_vak["payment_to"])
                            # Выводим данные о зарплате
                            if sal_from > 0 and sal_to == 0:
                                vacancy['04 Зарплата'] = f'от {str(sal_from)} ({dict_vak["currency"]}).'
                            elif sal_from == 0 and sal_to > 0:
                                vacancy['04 Зарплата'] = f'до {str(sal_to)} ({dict_vak["currency"]}).'
                            elif sal_from > 0 and sal_to > 0:
                                vacancy[
                                    '04 Зарплата'] = f'от {str(sal_from)} до {str(sal_to)} ({dict_vak["currency"]}).'
                            else:
                                vacancy['04 Зарплата'] = 'нет данных.'
                        except TypeError:
                            vacancy['04 Зарплата'] = 'нет данных.'
                    # График работы
                    case 'place_of_work':
                        try:
                            vacancy['05 График работы'] = self.two_levels(dict_vak["place_of_work"]["title"])
                        except TypeError:
                            vacancy['05 График работы'] = 'нет данных.'
                    # Занятость
                    case 'type_of_work':
                        try:
                            vacancy['06 Занятость'] = self.two_levels(dict_vak["type_of_work"]["title"])
                        except TypeError:
                            vacancy['06 Занятость'] = 'нет данных.'
                    # Опыт работы
                    case 'experience':
                        try:
                            vacancy['07 Опыт работы'] = self.two_levels(dict_vak["experience"]["title"])
                        except TypeError:
                            vacancy['07 Опыт работы'] = 'нет данных.'
                    # Требования к соискателю, обязанности
                    case 'education':
                        # Образование
                        try:
                            vacancy['08 Требования к соискателю'] = 'Образование ' + self.two_levels(
                                dict_vak["education"]["title"]).lower() + '.'
                        except TypeError:
                            vacancy['08 Требования к соискателю'] = 'нет данных.'
                    case 'vacancyRichText':
                        # Обязанности
                        try:
                            rich_text = dict_vak["vacancyRichText"]
                            rich_text = rich_text.replace("Обязанности:", '').replace("·", '').replace("• ", '').strip()
                            rich_text = self.break_down_lines(self.del_html_tag(self.del_space(rich_text)), 140)
                            vacancy['09 Обязанности'] = rich_text
                        except TypeError:
                            vacancy['09 Обязанности'] = 'нет данных.'
                    # URL вакансии
                    case 'link':
                        try:
                            vacancy['10 Подробнее здесь (URL)'] = self.two_levels(dict_vak["link"])
                        except TypeError:
                            vacancy['10 Подробнее здесь (URL)'] = 'нет данных.'

            # Выводим словарь на экран, удаляя номера у ключей и делая отступ.
            for key, value in sorted(vacancy.items()):
                print(f"  {key[3:]}: {value}")

            # Поочерёдный вывод вакансий и завершение работы программы
            i = input("\n ✅ Нажмите [Enter], чтобы продолжить\n"
                      " ❌ Введите 'q', чтобы выйти из программы: ").strip().lower()
            if not i:
                continue
            elif i == 'q':
                print(f'\nДо свидания! 👋')
                sys.exit('Работа программы завершена.\n')

    def two_levels(self, param_1: str) -> str:
        """
        Проверка и обработка данных из исходного словаря.
        Два уровня вложенности в словаре.
        :param param_1: Данные из словаря в соответствии с параметром, str.
        :return: Возвращает строку с данными или информацию об их отсутствии, str.
        """
        if str(param_1) != 'None':
            # Удаляем из теста html-теги и лишние пробелы.
            param_1 = self.del_space(self.del_html_tag(param_1))
            return f"{param_1}."
        return 'нет данных.'

    def three_levels(self, param_1: str, param_2: str) -> str:
        """
        Проверка и обработка данных из исходного словаря.
        Три уровня вложенности в словаре.
        :param param_1: Данные из словаря в соответствии с параметром, str.
        :param param_2: Данные из словаря в соответствии с параметром, str.
        :return: Возвращает строку с данными или информацию об их отсутствии, str.
        """
        if str(param_1) != 'None':
            # Удаляем из теста html-теги и лишние пробелы.
            param_2 = self.del_space(self.del_html_tag(param_2))
            return self.two_levels(param_2)
        return 'нет данных.'

    @staticmethod
    def print_data_val_two(param_1: int) -> int:
        """
        Проверка данных из словаря и возвращение значения.
        :param param_1: Данные из словаря, которые требуют проверки, int.
        :return: Вывод строки в соответствии с наличием или отсутствием данных, int.
        """
        if param_1 != 0:
            sal = param_1
        else:
            sal = 0
        return sal

    @staticmethod
    def del_space(txt: str) -> str:
        """
        Удаляет лишние пробелы в тексте.
        :param txt: Строка для анализа, str.
        :return: Строка с одинарными пробелами, str.
        """
        # Удаляем лишние пробелы в тексте (в начале, в конце, двойные, тройные),
        # оставляя по одному между словами.
        txt = ' '.join(txt.strip().split())
        # txt = re.sub(r'\s+', ' ', txt.strip())
        return txt

    @staticmethod
    def del_html_tag(txt: str) -> str:
        """
        Удаляет все html-теги из текста.
        :param txt: Строка для анализа, str.
        :return: Строка без html-тегов, str.
        """
        txt = re.sub(r'\<[^>]*\>', '', txt)
        return txt

    @staticmethod
    def list_sort_date(list_operations: list) -> list:
        """
        Возвращает список словарей, сортированный по дате и времени
        в обратном порядке.
        :param list_operations: Несортированный список словарей, list.
        :return: Сортированный список словарей, list.
        """
        # Сортируем словари в списке по дате и времени в обратном порядке.
        list_operations = sorted(list_operations,
                                 key=lambda x: time.strftime("%d.%m.%Y", time.gmtime(float(x["date_published"]))),
                                 reverse=True)
        return list_operations

    @staticmethod
    def key_sort_salary(my_dict: dict):
        """
        Условия сортировки для метода сортировки list_sort_salary.
        :param my_dict: Словарь из списка словарей, dict.
        :return: Ключ для сортировки.
        """
        if my_dict['payment_from'] != 0:
            return my_dict['payment_from']
        else:
            return my_dict['payment_to']

    def list_sort_salary(self, list_operations: list) -> list:
        """
        Возвращает список словарей, сортированный по заработной плате
        от большей к меньшей.
        :param list_operations: Несортированный список словарей, list.
        :return: Сортированный список словарей, list.
        """
        # Сортируем словари в списке по зарплате в обратном порядке.
        list_operations = sorted(list_operations, key=self.key_sort_salary, reverse=True)
        return list_operations

    @staticmethod
    def save_to_json(data: dict, path: str) -> None:
        """
        Сохраняет данные в json-файл.
        :param data: Словарь с данными, dict
        :return: Ничего не возвращает.
        """
        with open(path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_json(path_json: str) -> list:
        """
        Чтение данных из файла json и возвращение структуры.
        :param path_json: Путь к файлу, str.
        :return: Структура файла (список словарей).
        """
        # открываем файл на чтение
        with open(path_json, 'r', encoding='utf-8') as file:
            # считываем список словарей из файла
            content = json.load(file)
        return content

    @staticmethod
    def delete_files_in_folder(folder_path):
        """
        Удаление файлов из папки.
        :param folder_path: Путь к папке, str.
        :return:
        """
        # Определяем полные имена файлов в директории
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Удаляем файл
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f'Ошибка при удалении файла {file_path}. {e}')

    @staticmethod
    def break_down_lines(value: str, len_cut: int = 100, count_space: int = 15) -> str:
        """
        Разбивает длинные строки на несколько строк при помощи \n.
        :param value: Длинная строка без переносов, str.
        :param len_cut: Примерное количество символов для разбивки строки, int.
        :param count_space: Количество пробелов (отступ) слева, int.
        :return: Строка, разделённая на несколько строк, str.
        """
        if len(value) > len_cut:
            # Итоговая строка
            result_string = ""
            # Нижняя граница среза строки.
            lower_cut = 0
            # Количество "целых" строк, которые нужно вывести на экран.
            count_iter = len(value) // len_cut
            # Список строк
            list_str = []
            for i in range(1, count_iter + 1):
                # Если не дошли до конца строки (последней подстроки для переноса)
                if i <= count_iter:
                    # Находим индекс последнего пробела в подстроке.
                    index_space = value[lower_cut:i * len_cut].rfind(' ')
                    # Добавляем строку в список
                    list_str.append(value[lower_cut:lower_cut + index_space])
                    # Добавляем в конец подстроки вместо пробела символ переноса.
                    result_string += value[lower_cut:lower_cut + index_space] + '\n'
                    # Увеличиваем нижнюю границу на длину подстроки.
                    lower_cut = len(result_string) - 1
                else:
                    # Последняя "неполная" строка
                    list_str.append(value[lower_cut:])
            # Разделитель (отступ)
            space = '\n' + ' ' * count_space
            return space.join(list_str)

    def __str__(self) -> str:
        return f'Получение, обработка (включая сортировку) и вывод данных с сервиса superjob.ru по API {self.__url}'

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.__url}, {self.keyword}, "
                f"{self.area}, {self.only_with_salary}, {self.salary}, "
                f"{self.per_page}, {self.size_dict}, {self.sort_method}")
