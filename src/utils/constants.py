import os
from dotenv import load_dotenv, find_dotenv

# Путь к папке, в которой хранятся файлы с данными о вакансиях, полученных с HH.ru
PATH_VAK_HH = os.path.join('..', 'src', 'data', 'hh')
# Путь к файлу, в котором хранятся данные о регионах в России, полученных с HH.ru
PATH_ARE_HH = os.path.join('..', 'src', 'data', 'hh', 'areas', 'areas.json')
# Путь к папке, в которой хранятся данные о регионах в России, полученных с HH.ru
PATH_VAK_DIR_HH = os.path.join('..', 'src', 'data', 'hh', 'areas')
# id России для поиска вакансий
ID_RUSSIA_HH = 113


# Секретный ключ
load_dotenv(find_dotenv())
SUPERJOB_API_KEY = os.getenv('TOKEN_SJ')
# Путь к файлу данных с вакансиями SuperJob.ru
PATH_VAK_SJ = os.path.join('..', 'src', 'data', 'sj')
# Путь к файлу, в котором хранятся данные о регионах в России, полученных с HH.ru
PATH_ARE_SJ = os.path.join('..', 'src', 'data', 'sj', 'areas', 'areas.json')
# Путь к папке, в которой хранятся данные о регионах в России, полученных с HH.ru
PATH_VAK_DIR_SJ = os.path.join('..', 'src', 'data', 'sj', 'areas')
# id России для поиска вакансий
ID_RUSSIA_SJ = 1
