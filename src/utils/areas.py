import json
import os
from abc import ABC, abstractmethod
import requests
from src.utils.constants import PATH_ARE_HH, PATH_VAK_DIR_HH


class Areas(ABC):
    """
    Абстрактный класс выполнения и обработки запросов по api
    для поиска регионов.
    """

    @abstractmethod
    def request_to_api(self) -> str:
        pass

    @abstractmethod
    def extract_area_id(self):
        pass


class AreasHH(Areas):
    def __init__(self, area: str = 'Россия') -> None:
        self.__url = 'https://api.hh.ru/areas/113'  # Поиск регионов в России
        self.id = 113  # По-умолчанию id = 113 - Россия
        self.area = area.lower()

    def request_to_api(self) -> None:
        """
        Получение запроса о регионах в России по api.
        :return: Сохраняет данные о регионах в json-файл.
        """
        # Удаляем старый файл с данными о регионах areas.json
        self.delete_files_in_folder(PATH_VAK_DIR_HH)
        try:
            # Посылаем запрос к API, преобразуем его в словарь
            data_prof = json.loads(requests.get(url=self.__url).text)
            # Сохраняем данные в json-файл
            self.save_to_json(data_prof, PATH_ARE_HH)
        except Exception as e:
            raise Exception(f'Ошибка при получении данных с {self.__url}. {e}')

    def extract_area_id(self):
        """Получение id региона (города)"""
        areas = self.load_json(PATH_ARE_HH)
        # areas = areas['areas']
        # Ищем id указанного региона/населённого пункта.
        for area in areas['areas']:
            if str(area['name']).lower() == self.area:
                self.id = int(area['id'])
            else:
                for city in area['areas']:
                    if city['name'].lower() == self.area:
                        self.id = int(city['id'])
        return self.id

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
        Чтение данных из файла json и возвращение структуры,
        содержащейся в файле.
        :param path_json: Путь к файлу, str
        :return: Структура файла (список, словарь, список словарей...)
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
        # Определяем полные имена файлов в директории (путь + имя файла)
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Удаляем файл
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f'Ошибка при удалении файла {file_path}. {e}')
