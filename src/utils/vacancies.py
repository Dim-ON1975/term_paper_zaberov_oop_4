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
            vacancy[key_0] = 'нет данных.'

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
            vacancy[key_0] = 'нет данных.'

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
            vacancy[key_0] = 'нет данных.'

    @staticmethod
    def one_level_salary(dict_vak: dict, key_1: str) -> int:
        """
        Проверка и обработка данных по зарплате из исходного словаря.
        Один уровень вложенности ключей в словаре.
        :param dict_vak: Словарь вакансии (анализируемый), dict.
        :param key_1: Ключ 1-го уровня вложенности анализируемого словаря, str.
        :return: Выводит данные о зарплате, int.
        """
        salary = 0
        try:
            if dict_vak.get(key_1) != 0:
                salary = dict_vak[key_1]
        except (TypeError, AttributeError):
            pass
        return salary

    @staticmethod
    def two_levels_salary(dict_vak: dict, key_1: str, key_2: str) -> int:
        """
        Проверка и обработка данных по зарплате из исходного словаря.
        Два уровня вложенности ключей в словаре.
        :param dict_vak: Словарь вакансии (анализируемый), dict.
        :param key_1: Ключ 1-го уровня вложенности анализируемого словаря, str.
        :param key_2: Ключ 2-го уровня вложенности анализируемого словаря, str.
        :return: Выводит данные о зарплате, 0.
        """
        salary = 0
        try:
            if all(str(dict_vak.get(key_1).get(key_2))):
                if str(dict_vak.get(key_1).get(key_2)) != 'None':
                    salary = dict_vak[key_1][key_2]
        except (TypeError, AttributeError):
            pass
        return salary

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
    def list_sort_date(list_operations: list, key: str) -> list:
        """
        Возвращает список словарей, сортированный по дате и времени
        в обратном порядке.
        :param list_operations: Несортированный список словарей, list.
        :param key: Ключ для сортировки даты, str.
        :return: Сортированный список словарей, list.
        """
        # Сортируем словари в списке по дате в обратном порядке.
        list_operations = sorted(list_operations,
                                 key=lambda x: datetime.strptime(x[key], '%Y-%m-%d'),
                                 reverse=True)
        return list_operations

    @staticmethod
    def list_sort_salary(list_operations: list, key_1: str, key_2: str) -> list:
        """
        Возвращает список словарей, сортированный по заработной плате
        от большей к меньшей.
        :param list_operations: Несортированный список словарей, list.
        :param key_1: Ключ словаря "зарплата от", str.
        :param key_2: Ключ словаря "зарплата до", str.
        :return: Сортированный список словарей, list.
        """
        # Сортируем словари в списке по зарплате в обратном порядке.
        # list_operations = sorted(list_operations, key=lambda x: x[key_1] if x[key_1] != 0 else x[key_2], reverse=True)
        # Сортировка по усреднённой заработной плате в пределах "вилки" "от и до".
        list_operations = sorted(list_operations, key=lambda x: (x[key_1] + x[key_2]) // 2, reverse=True)
        return list_operations

    @staticmethod
    def save_to_json(data: list, path: str) -> None:
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
    def delete_files_in_folder(folder_path) -> None:
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
    """
    Получение данных по API с hh.ru, их обработка и сохранение.
    """

    def __init__(self, position: str, area: int = ID_RUSSIA_HH, only_with_salary: bool = False, salary: int = 0,
                 per_page: int = 100) -> None:
        self.__url = 'https://api.hh.ru/vacancies'
        self.__position = str(position)  # Текст фильтра
        self.__area = area  # Поиск по-умолчанию осуществляется по вакансиям России (id=113)
        self.__only_with_salary = only_with_salary  # Показывать вакансии только с указанием зарплаты или все
        self.__salary = salary  # Ожидаемый размер заработной платы
        self.__per_page = per_page  # Кол-во вакансий на 1 странице
        self.size_dict = 0  # Счётчик количества словарей с вакансиями

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

                # Формируем собственный список словарей для сохранения в json-файл,
                # отбирая только нужные данные.
                vak_js = []  # список словарей для записи в файл

                # Ключи с однотипным ('двойным') уровнем вложенности.
                keys = {
                    '03 Работодатель': ["employer", "name"],
                    '04 Населённый пункт': ["area", "name"],
                    '05 Адрес': ["address", "raw"],
                    '08 Валюта': ["salary", "currency"],
                    '09 График работы': ["schedule", "name"],
                    '10 Занятость': ["employment", "name"],
                    '11 Опыт работы': ["experience", "name"],
                    '12 Требования к соискателю': ["snippet", "requirement"],
                    '13 Обязанности': ["snippet", "responsibility"],
                }
                # Обработка данных полученного словаря
                for value in js_obj['items']:
                    # словарь вакансии
                    vacancy = {
                        '01 Дата публикации': value["published_at"].split('T')[0],
                        '02 Должность': value["name"] + '.',
                        '06 Зарплата от': self.two_levels_salary(value, "salary", "from"),
                        '07 Зарплата до': self.two_levels_salary(value, "salary", "to"),
                    }
                    # Заполняем словарь vacancy по ключам 03-05, 08-13
                    # имеющим "двойной" уровень вложенности.
                    for key_0, key in keys.items():
                        self.two_levels(value, vacancy, key_0, key[0], key[1])
                    # Ссылка на страницу вакансии
                    self.one_level(value, vacancy, '14 Подробнее здесь (URL)', "alternate_url")
                    # Добавляем словарь с вакансией в список
                    vak_js.append(dict(sorted(vacancy.items())))

                # Создаём номер файла для адекватной последовательной сортировки в дальнейшем
                if page < 10:
                    page_num = '0' + str(page)
                else:
                    page_num = str(page)
                # Создаём новый документ, записываем в него ответ запроса
                self.save_to_json(vak_js, os.path.join(PATH_VAK_HH, f'vakhh_{page_num}.json'))

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

    def __str__(self) -> str:
        return f'Получение, обработка (включая сортировку) и вывод данных с сервиса hh.ru по API {self.__url}'

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.__url}, {self.__position},"
                f" {self.__area}, {self.__only_with_salary}, {self.__salary},"
                f" {self.__per_page}, {self.size_dict})")


class VacSJ(Vacancies, Mixin):
    """
    Получение данных по API с superjob.ru, их обработка и сохранение.
    """

    def __init__(self, position: str, area: int = ID_RUSSIA_SJ, only_with_salary: bool = False, salary: int = 0,
                 per_page: int = 100) -> None:
        self.__url = 'https://api.superjob.ru/2.0/vacancies/'
        self.__keyword = str(position)  # Текст фильтра
        self.__area = area  # Поиск по-умолчанию осуществляется по вакансиям России (id=1)
        self.__only_with_salary = only_with_salary  # Показывать вакансии только с указанием зарплаты или все
        self.__salary = salary  # Ожидаемый размер заработной платы
        self.__per_page = per_page  # Кол-во вакансий на 1 странице
        self.size_dict = 0  # Счётчик количества словарей с вакансиями

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

                # Формируем собственный список словарей для сохранения в json-файл,
                # отбирая только нужные данные.
                vak_js = []  # список словарей для записи в файл

                # Ключи с однотипным ('одинарным') уровнем вложенности.
                keys_1 = {
                    '05 Адрес': ["address"],
                    '08 Валюта': ["currency"],
                    '13 Обязанности': ["vacancyRichText"],
                    '14 Подробнее здесь (URL)': ["link"]
                }
                # Ключи с однотипным ('двойным') уровнем вложенности.
                keys_2 = {
                    '03 Работодатель': ["client", "title"],
                    '09 График работы': ["place_of_work", "title"],
                    '10 Занятость': ["type_of_work", "title"],
                    '11 Опыт работы': ["experience", "title"],
                    '12 Требования к соискателю': ["education", "title"],
                }
                # Обработка данных полученного словаря
                for value in js_obj['objects']:
                    # словарь вакансии
                    vacancy = {
                        '01 Дата публикации': time.strftime("%Y-%m-%d", time.gmtime(float(value["date_published"]))),
                        '02 Должность': value["profession"] + '.',
                        '06 Зарплата от': self.one_level_salary(value, "payment_from"),
                        '07 Зарплата до': self.one_level_salary(value, "payment_to"),
                    }

                    # Заполняем словарь vacancy
                    # по ключам 05, 08, 13, 14, имеющим "одинарный" уровень вложенности.
                    for key_0, key in keys_1.items():
                        self.one_level(value, vacancy, key_0, key[0])

                    # по ключам 03, 09-12, имеющим "двойной" уровень вложенности.
                    for key_0, key in keys_2.items():
                        self.two_levels(value, vacancy, key_0, key[0], key[1])
                    # по ключу 04, имеющему тройной уровень вложенности
                    self.three_levels(value, vacancy, '04 Населённый пункт', "client", "town", "title")

                    # Добавляем словарь с вакансией в список
                    vak_js.append(dict(sorted(vacancy.items())))

                # Создаём номер файла для адекватной последовательной сортировки в дальнейшем
                if page < 10:
                    page_num = '0' + str(page)
                else:
                    page_num = str(page)
                # Создаём новый документ, записываем в него ответ запроса
                self.save_to_json(vak_js, os.path.join(PATH_VAK_SJ, f'vaksj_{page_num}.json'))

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

    def __str__(self) -> str:
        return f'Получение, обработка (включая сортировку) и вывод данных с сервиса superjob.ru по API {self.__url}'

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.__url}, {self.__keyword},"
                f" {self.__area}, {self.__only_with_salary}, {self.__salary},"
                f" {self.__per_page}, {self.size_dict}")


class VacPrint(Mixin):
    """
    Вывод данных на экран
    """

    def __init__(self, sort_method: int = 2):
        self.__sort_method = sort_method  # Метод сортировки: 1 - по размеру зарплаты, 2 - по датам

    def vacancies_print(self, count_vak, resource: str, one_each: int = 1) -> None:
        """
        Выводит вакансии на экран в количестве, заданном пользователем.
        :param count_vak: Необходимое количество, int.
        :param resource: Указатель ресурса: 'hh' или 'sj', str.
        :param one_each: Вывод вакансий: 1 - по одной, другое - все сразу, int.
        :return: Выводит на экран информацию о вакансиях.
        """
        if resource == 'hh':
            path = PATH_VAK_HH
        elif resource == 'sj':
            path = PATH_VAK_SJ
        else:
            print('Мы не готовы показать вакансии с указанного ресурса.')
            sys.exit('Работа программы завершена.\n')

        # Пустой список
        data = []
        # Перемещаемся по файлам в папке, считывая значения, объединяя их в один список словарей.
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path):
                    # Считываем данные из всех файлов в директории, объединяя их в один список.
                    data += self.load_json(file_path)
            except Exception as e:
                print(f'Ошибка при открытии и/или чтении файла {file_path}. {e}')
        # Сортируем список по датам или зарплате, выводя, заданное пользователем, количество словарей.
        if self.__sort_method == 1:
            data = self.list_sort_salary(data, "06 Зарплата от", "07 Зарплата до")[:count_vak]
        else:
            data = self.list_sort_date(data, '01 Дата публикации')[:count_vak]
        # Выводим данные на экран из списка, в котором отсортированы словари.
        self.data_print(data, one_each)
        # Выводим информацию об окончании вывода.
        print('----------------------\n'
              'Выведены все вакансии.')

    def data_print(self, data: list, one_each: int = 1) -> None:
        """
        Формирует словарь вакансий для вывода информации на экран.
        :param data: Список словарей с данными о вакансиях, list.
        :param one_each: Вывод вакансий: 1 - по одной, другое - все сразу, int.
        :return: Выводит на экран вакансии, отсортированные по дате.
        """
        # Анализируем список словарей, выводим необходимые данные на экран.

        for c_enum, dict_vak in enumerate(data, start=1):

            # Выводим словарь на экран
            self.print_display(dict_vak, c_enum)

            if one_each == 1:
                # Поочерёдный вывод вакансий и завершение работы программы
                i = input("\n ✅ Нажмите [Enter], чтобы продолжить\n"
                          " ❌ Введите 'q', чтобы выйти из программы: ").strip().lower()
                print()
                if not i:
                    continue
                elif i == 'q':
                    print(f'\nДо свидания! 👋')
                    sys.exit('Работа программы завершена.\n')

    def print_display(self, dict_vak: dict, enum: int) -> None:
        """
        Выводит информацию о вакансиях на экран.
        :param dict_vak: Словарь с вакансией, dict.
        :param enum: Порядковый номер вакансии (словаря), int.
        :return: Вывод информации на экран.
        """

        # Выводим словарь на экран, удаляя номера у ключей, лишние символы и выполняя переносы длинных строк.
        for key, value in sorted(dict_vak.items()):
            # Формируем и выводим заголовок вакансии
            if key == "01 Дата публикации":
                # Номер, дата публикации вакансии, наименование должности.
                # Номер.
                enum = '№ ' + str(enum) + ','  # номер
                # Дата.
                date_publ = dict_vak["01 Дата публикации"]
                date_publ = ' от ' + date_publ[-2:] + '.' + date_publ[5:7] + '.' + date_publ[:4] + ': '
                # Должность.
                name = dict_vak["02 Должность"] + '.'
                # Вывод строки с данными ('заголовок вакансии').
                print('-' * (len(enum) + len(date_publ) + len(name)))
                print(f'{enum}{date_publ}{name}')
                print('-' * (len(enum) + len(date_publ) + len(name)))
            # Если должность, то ничего не делаем (вывели вместе с датой)
            elif key == "02 Должность":
                pass
            # Обработка и вывод длинных строк
            elif key == "12 Требования к соискателю":
                string_print = self.break_down_lines(self.del_html_tag(self.del_space(value)), 130, 27)
                print(f"  {key[3:]}: {string_print}")
            # Обработка и вывод длинных строк
            elif key == "13 Обязанности":
                string_print = value.replace('Обязанности:', '')
                string_print = self.break_down_lines(self.del_html_tag(self.del_space(string_print)), 140, 15)
                print(
                    f"  {key[3:]}: {string_print}")
            # Вывод данных по остальным ключам
            else:
                print(f"  {key[3:]}: {self.del_html_tag(self.del_space(str(value)))}")

    def __str__(self) -> str:
        return f'Вывод данных о вакансиях на экран.'

    def __repr__(self) -> str:
        return f"{self.__sort_method}"
