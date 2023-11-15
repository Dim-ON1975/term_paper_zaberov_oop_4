import json
import os
from abc import ABC, abstractmethod
import requests
from src.utils.constants import PATH_ARE_HH, PATH_VAK_DIR_HH, PATH_VAK_DIR_SJ, SUPERJOB_API_KEY, PATH_ARE_SJ, \
    ID_RUSSIA_SJ, ID_RUSSIA_HH


class Areas(ABC):
    """
    Абстрактный класс получения справочника по API
    для поиска регионов/населённых пунктов России.
    """

    @abstractmethod
    def request_to_api(self) -> str:
        pass

    @abstractmethod
    def extract_area_id(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class Mixin:
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
        Чтение данных из файла json и возвращение структуры,
        содержащейся в нём.
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
        # Определяем полные имена файлов в директории.
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Удаляем файл
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f'Ошибка при удалении файла {file_path}. {e}')


class AreasHH(Areas, Mixin):
    def __init__(self, area: str = 'Россия', path_vak_dir_hh: str = PATH_VAK_DIR_HH,
                 path_are_hh: str = PATH_ARE_HH) -> None:
        self.__url = 'https://api.hh.ru/areas/113'  # Поиск регионов в России
        self.__id = ID_RUSSIA_HH  # По-умолчанию Россия
        self.__area = area.lower()
        # Путь к папке, в которой хранятся данные о регионах в России, полученных с HH.ru.
        self.__path_vak_dir_hh = path_vak_dir_hh
        # Путь к файлу, в котором хранятся данные о регионах в России, полученных с HH.ru.
        self.__path_are_hh = path_are_hh

    def request_to_api(self) -> None:
        """
        Получение запроса о регионах в России по api.
        :return: Сохраняет данные о регионах в json-файл.
        """
        # Удаляем старый файл с данными о регионах areas.json
        self.delete_files_in_folder(self.__path_vak_dir_hh)
        try:
            # Посылаем запрос к API, преобразуем его в словарь
            data_prof = json.loads(requests.get(url=self.__url).text)
            # Сохраняем данные в json-файл
            self.save_to_json(data_prof, self.__path_are_hh)
        except Exception as e:
            raise Exception(f'Ошибка при получении данных с {self.__url}. {e}')

    def extract_area_id(self):
        """Получение id региона (города)"""
        areas = self.load_json(self.__path_are_hh)
        # Ищем id указанного региона/населённого пункта.
        for area in areas['areas']:
            # Регион
            if str(area['name']).lower() == self.__area:
                self.__id = int(area['id'])
            else:
                # Населённый пункт
                for city in area['areas']:
                    if city['name'].lower() == self.__area:
                        self.__id = int(city['id'])
        return self.__id

    def __str__(self) -> str:
        return f'Получение справочника регионов/городов России с сервиса hh.ru по API {self.__url}'

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.__url}, {self.__id}, "
                f"{self.__area}, {self.__path_vak_dir_hh}, {self.__path_are_hh})")


class AreasSJ(Areas, Mixin):
    def __init__(self, area: str = 'Россия', path_vak_dir_sj: str = PATH_VAK_DIR_SJ,
                 path_are_sj: str = PATH_ARE_SJ) -> None:
        self.__url = 'https://api.superjob.ru/2.0/regions/combined/'  # Поиск регионов в России
        self.__id = ID_RUSSIA_SJ  # По-умолчанию Россия
        self.__area = area.lower()
        # Путь к папке, в которой хранятся данные о регионах в России, полученных с superjob.ru.
        self.__path_vak_dir_sj = path_vak_dir_sj
        # Путь к файлу, в котором хранятся данные о регионах в России, полученных с superjob.ru.
        self.__path_are_sj = path_are_sj

    def request_to_api(self) -> None:
        """
        Получение запроса о регионах в России по api.
        :return: Сохраняет данные о регионах в json-файл.
        """
        # Удаляем старый файл с данными о регионах areas.json
        self.delete_files_in_folder(self.__path_vak_dir_sj)
        try:
            # Посылаем запрос к API, преобразуем его в словарь
            headers = {'X-Api-App-Id': SUPERJOB_API_KEY}
            data_prof = json.loads(requests.get(url=self.__url, headers=headers).text)
            # data_prof = json.loads(requests.get(url=self.__url).text)
            # Сохраняем данные в json-файл только регионы и города России
            self.save_to_json(data_prof[0], self.__path_are_sj)
        except Exception as e:
            raise Exception(f'Ошибка при получении данных с {self.__url}. {e}')

    def extract_area_id(self):
        """Получение id региона (города)"""
        areas = self.load_json(self.__path_are_sj)

        # Ищем id указанного региона/населённого пункта.
        # Города федерального значения
        for area in areas['towns']:
            if str(area['title']).lower() == self.__area:
                self.__id = int(area['id'])

        # Остальные регионы и города России
        for area in areas['regions']:
            # Регион
            if str(area['title']).lower() == self.__area:
                self.__id = int(area['id'])
            else:
                # Населённый пункт
                for city in area['towns']:
                    if city['title'].lower() == self.__area:
                        self.__id = int(city['id'])
        return self.__id

    def __str__(self) -> str:
        return f'Получение справочника регионов/городов России с сервиса superjob.ru по API {self.__url}'

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.__url}, {self.__id}, "
                f"{self.__area}, {self.__path_vak_dir_sj}, {self.__path_are_sj})")
