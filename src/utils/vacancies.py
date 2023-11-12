import json
import os
import sys
from abc import ABC, abstractmethod
import time
from datetime import datetime

import requests
from tqdm import trange
import re

from src.utils.constants import PATH_VAK_HH, SUPERJOB_API_KEY, PATH_VAK_SJ, ID_RUSSIA_HH, ID_RUSSIA_SJ, VACANCY


class Vacancies(ABC):
    """
    Абстрактный класс выполнения запросов по API:
    поиска, обработки, фильтрации и вывода вакансий.
    """

    @abstractmethod
    def __init__(self):
        pass

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
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


class Mixin:
    """
    Класс примеси содержит статические методы, позволяющие выполнять различные задачи наследникам.
    """

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
    def three_levels(dict_vak: dict, vacancy: dict, key_0: str, key_1: str, key_2: str, key_3: str) -> None:
        """
        Проверка и обработка данных из исходного словаря.
        Три уровня вложенности ключей в словаре.
        :param dict_vak: Словарь вакансии (анализируемый), dict.
        :param vacancy: Словарь вакансии (заполняемый), dict.
        :param key_0: Ключ создаваемого словаря, str.
        :param key_1: Ключ 1-го уровня вложенности анализируемого словаря, str.
        :param key_2: Ключ 2-го уровня вложенности анализируемого словаря, str.
        :param key_3: Ключ 3-го уровня вложенности анализируемого словаря, str.
        :return: Добавляет в словарь пару ключ: значение.
        """
        try:
            if all(dict_vak.get(key_1).get(key_2).get(key_3)):
                vacancy[key_0] = dict_vak[key_1][key_2][key_3]
        except (TypeError, AttributeError):
            pass

    @staticmethod
    def one_level_salary(dict_vak: dict, key_1: str, from_to: str) -> str:
        """
        Проверка и обработка данных по зарплате из исходного словаря.
        Один уровень вложенности ключей в словаре.
        :param dict_vak: Словарь вакансии (анализируемый), dict.
        :param key_1: Ключ 1-го уровня вложенности анализируемого словаря, str.
        :param from_to: Строки 'от' или 'до', str.
        :return: Выводит данные о зарплате в виде строки, str.
        """
        str_salary = ''
        try:
            if dict_vak.get(key_1) != 0:
                str_salary = f'{from_to} {str(dict_vak[key_1])}'
        except (TypeError, AttributeError):
            pass
        return str_salary

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
    def list_sort_date_unix(list_operations: list) -> list:
        """
        Возвращает список словарей, сортированный по дате и времени
        в формате unix в обратном порядке.
        :param list_operations: Несортированный список словарей, list.
        :return: Сортированный список словарей, list.
        """
        # Сортируем словари в списке по дате и времени в обратном порядке.
        list_operations = sorted(list_operations,
                                 key=lambda x: time.strftime("%d.%m.%Y", time.gmtime(float(x["date_published"]))),
                                 reverse=True)
        return list_operations

    @staticmethod
    def key_sort_salary_hh(my_dict: dict):
        """
        Условия сортировки для метода list_sort_salary.
        :param my_dict: Словарь из списка, dict.
        :return: Ключ для сортировки.
        """
        if my_dict['salary']['from'] is not None:
            return my_dict['salary']['from']
        else:
            return my_dict['salary']['to']

    @staticmethod
    def key_sort_salary_sj(my_dict: dict):
        """
        Условия сортировки для метода list_sort_salary.
        :param my_dict: Словарь из списка, dict.
        :return: Ключ для сортировки.
        """
        if my_dict['payment_from'] is not None:
            return my_dict['payment_from']
        else:
            return my_dict['payment_from']

    @staticmethod
    def save_to_json(data: dict, path: str) -> None:
        """
        Сохраняет данные в json-файл.
        :param path: Полное имя файла, str.
        :param data: Словарь с данными, dict.
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
        Разбивает длинные строки на несколько при помощи \n.
        :param value: Длинная строка без переносов, str.
        :param len_cut: Примерное количество символов для разбивки строки, int.
        :param count_space: Количество пробелов (отступ) слева, int.
        :return: Строка, разделённая на несколько, str.
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
                # Последняя "неполная" строка
                list_str.append(value[lower_cut:])
                # Разделитель (отступ)
                space = '\n' + ' ' * count_space
                result_string = space.join(list_str)
        else:
            result_string = value
        return result_string

    @staticmethod
    def coord_words_num(digit) -> str:
        """
            Согласование слова "вакансии" с числительными.
            :param digit: Числительное для согласования, int.
            :return: Слово "вакансии", согласованное с числительным, str.
        """
        if digit % 10 == 1 and digit != 11:
            return f'{digit} вакансия'
        elif digit % 10 in [2, 3, 4] and digit not in [12, 13, 14]:
            return f'{digit} вакансии'
        else:
            return f'{digit} вакансий'


class VacHH(Vacancies, Mixin):
    def __init__(self, position: str, area: int = ID_RUSSIA_HH, only_with_salary: bool = False, salary: int = 0,
                 per_page: int = 100, sort_method: int = 2) -> None:
        self.__url = 'https://api.hh.ru/vacancies'
        self.__position = str(position)  # Текст фильтра
        self.__area = area  # Поиск по-умолчанию осуществляется по вакансиям России (id=113)
        self.__only_with_salary = only_with_salary  # Показывать вакансии только с указанием зарплаты или все
        self.__salary = salary  # Ожидаемый размер заработной платы
        self.__per_page = per_page  # Кол-во вакансий на 1 странице
        self.size_dict = 0  # Счётчик количества словарей с вакансиями
        self.__sort_method = sort_method  # Метод сортировки: 1 - по датам, 2 - по размеру зарплаты
        # Объявляем словарь, определяем структуру данных для отображения пользователю
        self.__vacancy = VACANCY

    def request_to_api(self, page: int = 0) -> str:
        """
        Получение запроса по api
        :page: Индекс страницы поиска HH.
        :return: ответ запроса, <class 'requests.models.Response'>.
        """
        try:
            # Без фильтрации по размеру заработной платы
            params = {
                'text': self.__position,
                'area': self.__area,
                'page': page,
                'per_page': self.__per_page
            }
            if self.__salary != 0:
                # С фильтрацией по размеру заработной платы
                params['salary'] = self.__salary
                params['only_with_salary'] = self.__only_with_salary

            # Отправляем запрос к API
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
                print(f'\nПо вашему запросу на hh.ru найдено {self.coord_words_num(self.size_dict)} вакансий.\n')
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
        if self.__sort_method == 1:
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
        Формирует словарь вакансий для вывода информации на экран.
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
                self.two_levels(dict_vak, self.__vacancy, key_0, key[0], key[1])

            # Зарплата.
            # Получаем данные о зарплате (от и до)
            sal_from = self.two_levels_salary(dict_vak, "salary", "from", 'от')
            sal_to = self.two_levels_salary(dict_vak, "salary", "to", 'до')
            # Помещаем данные в словарь, удаляя лишние пробелы
            if sal_from != '' or sal_to != '':
                self.__vacancy['04 Зарплата'] = self.del_space(
                    f'{str(sal_from)} {str(sal_to)} ({dict_vak["salary"]["currency"]}).')

            # URL вакансии
            self.one_level(dict_vak, self.__vacancy, '10 Подробнее здесь (URL)', "alternate_url")

            # Выводим словарь на экран
            self.print_display()

            # Поочерёдный вывод вакансий и завершение работы программы
            i = input("\n ✅ Нажмите [Enter], чтобы продолжить\n"
                      " ❌ Введите 'q', чтобы выйти из программы: ").strip().lower()
            if not i:
                continue
            elif i == 'q':
                print(f'\nДо свидания! 👋')
                sys.exit('Работа программы завершена.\n')

    def print_display(self) -> None:
        """
        Выводит информацию о вакансиях на экран.
        :return: Вывод информации на экран.
        """
        # Выводим словарь на экран, удаляя номера у ключей, лишние символы и выполняя переносы длинных строк.
        for key, value in sorted(self.__vacancy.items()):
            if key == "08 Требования к соискателю":
                string_print = self.break_down_lines(self.del_html_tag(self.del_space(value)), 130, 27)
                print(f"  {key[3:]}: {string_print}")
            elif key == "09 Обязанности":
                string_print = value.replace('Обязанности:', '')
                string_print = self.break_down_lines(self.del_html_tag(self.del_space(string_print)), 140, 15)
                print(
                    f"  {key[3:]}: {string_print}")
            else:
                print(f"  {key[3:]}: {self.del_html_tag(self.del_space(value))}")

    def list_sort_salary(self, list_operations: list) -> list:
        """
        Возвращает список словарей, сортированный по заработной плате
        от большей к меньшей.
        :param list_operations: Несортированный список словарей, list.
        :return: Сортированный список словарей, list.
        """
        # Сортируем словари в списке по зарплате в обратном порядке.
        list_operations = sorted(list_operations, key=self.key_sort_salary_hh, reverse=True)
        return list_operations

    def __str__(self) -> str:
        return f'Получение, обработка (включая сортировку) и вывод данных с сервиса hh.ru по API {self.__url}'

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.__url}, {self.__position},"
                f"{self.__area}, {self.__only_with_salary}, {self.__salary}, "
                f"{self.__per_page}, {self.size_dict}, {self.__sort_method})")


class VacSJ(Vacancies, Mixin):
    def __init__(self, position: str, area: int = ID_RUSSIA_SJ, only_with_salary: bool = False, salary: int = 0,
                 per_page: int = 100, sort_method: int = 2) -> None:
        self.__url = 'https://api.superjob.ru/2.0/vacancies/'
        self.__keyword = str(position)  # Текст фильтра
        self.__area = area  # Поиск по-умолчанию осуществляется по вакансиям России (id=1)
        self.__only_with_salary = only_with_salary  # Показывать вакансии только с указанием зарплаты или все
        self.__salary = salary  # Ожидаемый размер заработной платы
        self.__per_page = per_page  # Кол-во вакансий на 1 странице
        self.size_dict = 0  # Счётчик количества словарей с вакансиями
        self.__sort_method = sort_method  # Метод сортировки: 1 - по датам, 2 - по размеру зарплаты
        # Объявляем словарь, определяем структуру данных для отображения пользователю
        self.__vacancy = VACANCY

    def request_to_api(self, page: int = 0) -> str:
        """
        Получение запроса по api
        :page: Индекс страницы поиска HH.
        :return: ответ запроса, <class 'requests.models.Response'>.
        """
        try:
            # Без фильтрации по зарплате, поиск по конкретному городу/региону России.
            params = {
                'keyword': self.__keyword,
                'town': self.__area,
                'page': page,
                'count': self.__per_page,
            }
            # Поиск по России
            if self.__area == 1:
                params['c'] = params.pop('town')
            # С фильтрацией по размеру заработной платы
            if self.__salary != 0:
                params['payment_from'] = self.__salary
                params['payment_to'] = self.__salary * 5
                params['no_agreement'] = self.__only_with_salary

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
                if js_obj['total'] < self.__per_page:
                    break

                # Задержка, чтобы не нагружать сервисы sj.
                time.sleep(0.03)

            # Вывод данных о количестве вакансий
            if self.size_dict != 0:
                print(
                    f'\nПо вашему запросу на superjob.ru найдено {self.coord_words_num(self.size_dict)} вакансий.\n')
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
        if self.__sort_method == 1:
            data = self.list_sort_salary(data)[:count_vak]
        else:
            data = self.list_sort_date_unix(data)[:count_vak]
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

            # Заполняем словарь данными, проверяя наличие необходимых ключей.
            # Ключи с однотипным ('одинарным') уровнем вложенности.
            keys_1 = {
                '03 Адрес': ["address"],
                '09 Обязанности': ["vacancyRichText"],
                '10 Подробнее здесь (URL)': ["link"]
            }
            # Ключи с однотипным ('двойным') уровнем вложенности.
            keys_2 = {
                '01 Работодатель': ["client", "title"],
                '05 График работы': ["place_of_work", "title"],
                '06 Занятость': ["type_of_work", "title"],
                '07 Опыт работы': ["experience", "title"],
                '08 Требования к соискателю': ["education", "title"],
            }

            # Заполняем словарь vacancy
            # по ключам 03, 09, 10, имеющим "одинарный" уровень вложенности.
            for key_0, key in keys_1.items():
                self.one_level(dict_vak, self.__vacancy, key_0, key[0])

            # по ключам 01, 05-08, имеющим "двойной" уровень вложенности.
            for key_0, key in keys_2.items():
                self.two_levels(dict_vak, self.__vacancy, key_0, key[0], key[1])

            # по ключу 02, имеющему тройной уровень вложенности
            self.three_levels(dict_vak, self.__vacancy, '02 Населённый пункт', "client", "town", "title")

            # Зарплата.
            # Получаем данные о зарплате (от и до)
            sal_from = self.one_level_salary(dict_vak, "payment_from", 'от')
            sal_to = self.one_level_salary(dict_vak, "payment_to", 'до')
            # Помещаем данные в словарь, удаляя лишние пробелы
            if sal_from != '' or sal_to != '':
                self.__vacancy['04 Зарплата'] = self.del_space(
                    f'{str(sal_from)} {str(sal_to)} ({dict_vak["currency"]}).')

            # Выводим словарь на экран
            self.print_display()

            # Поочерёдный вывод вакансий и завершение работы программы
            i = input("\n ✅ Нажмите [Enter], чтобы продолжить\n"
                      " ❌ Введите 'q', чтобы выйти из программы: ").strip().lower()
            if not i:
                continue
            elif i == 'q':
                print(f'\nДо свидания! 👋')
                sys.exit('Работа программы завершена.\n')

    def print_display(self) -> None:
        """
        Выводит информацию о вакансиях на экран.
        :return: Вывод информации на экран.
        """
        # Выводим словарь на экран, удаляя номера у ключей, лишние символы и выполняя переносы длинных строк.
        for key, value in sorted(self.__vacancy.items()):
            if key == "08 Требования к соискателю":
                string_print = self.break_down_lines(self.del_html_tag(self.del_space(value)), 130, 27)
                print(f"  {key[3:]}: {string_print}")
            elif key == "09 Обязанности":
                string_print = value.replace('Обязанности:', '')
                string_print = self.break_down_lines(self.del_html_tag(self.del_space(string_print)), 140, 15)
                print(
                    f"  {key[3:]}: {string_print}")
            else:
                print(f"  {key[3:]}: {self.del_html_tag(self.del_space(value))}")

    def list_sort_salary(self, list_operations: list) -> list:
        """
        Возвращает список словарей, сортированный по заработной плате
        от большей к меньшей.
        :param list_operations: Несортированный список словарей, list.
        :return: Сортированный список словарей, list.
        """
        # Сортируем словари в списке по зарплате в обратном порядке.
        list_operations = sorted(list_operations, key=self.key_sort_salary_sj, reverse=True)
        return list_operations

    def __str__(self) -> str:
        return f'Получение, обработка (включая сортировку) и вывод данных с сервиса superjob.ru по API {self.__url}'

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.__url}, {self.__keyword}, "
                f"{self.__area}, {self.__only_with_salary}, {self.__salary}, "
                f"{self.__per_page}, {self.size_dict}, {self.__sort_method}")
