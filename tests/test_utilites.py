# Тестирование модуля utilities.py
import os

import pytest

from src.utils.utilities import loading_regions_hh, loading_regions_sj, user_name, exit_program, service_selection, \
    search_area_id, selection_menu_sections_id, num_area_word, all_ok_salary, all_ok_salary_input


def test_loading_regions_hh():
    """
    Тестирование загрузки справочников регионов/населённых пунктов с сервиса hh.ru.
    """

    path_vak_dir_hh = os.path.join('..', 'tests', 'data', 'hh', 'areas')
    path_are_hh = os.path.join('..', 'tests', 'data', 'hh', 'areas', 'test_areas.json')

    loading_regions_hh(path_vak_dir_hh=path_vak_dir_hh, path_are_hh=path_are_hh)

    # Создаваемый файл существует или нет (bool).
    file_created = os.path.exists(path_are_hh)

    assert file_created is True

    # Созданный файл не пустой
    file_size = os.path.getsize(path_are_hh)

    assert file_size > 0

    # Ошибка при получении данных
    with pytest.raises(Exception) as exif:
        url = ''
        loading_regions_hh(url=url, path_vak_dir_hh=path_vak_dir_hh, path_are_hh=path_are_hh)
    assert f'Ошибка при получении данных с {url}.' in str(exif.value)

    # Ошибка при удалении файлов
    with pytest.raises(Exception) as exif:
        path_vak_dir_hh = ''
        loading_regions_hh(url=url, path_vak_dir_hh=path_vak_dir_hh, path_are_hh=path_are_hh)
    assert f'Системе не удается найти указанный путь' in str(exif.value)


def test_loading_regions_sj():
    """
    Тестирование загрузки справочников регионов/населённых пунктов с сервиса superjob.ru.
    """

    path_vak_dir_sj = os.path.join('..', 'tests', 'data', 'sj', 'areas')
    path_are_sj = os.path.join('..', 'tests', 'data', 'sj', 'areas', 'test_areas.json')

    loading_regions_sj(path_vak_dir_sj=path_vak_dir_sj, path_are_sj=path_are_sj)

    # Создаваемый файл существует или нет (bool).
    file_created = os.path.exists(path_are_sj)

    assert file_created is True

    # Созданный файл не пустой
    file_size = os.path.getsize(path_are_sj)

    assert file_size > 0

    # Ошибка при получении данных
    with pytest.raises(Exception) as exif:
        url = ''
        loading_regions_sj(url=url, path_vak_dir_sj=path_vak_dir_sj, path_are_sj=path_are_sj)
    assert f'Ошибка при получении данных с {url}.' in str(exif.value)

    # Ошибка при удалении файлов
    with pytest.raises(Exception) as exif:
        path_vak_dir_sj = ''
        loading_regions_sj(url=url, path_vak_dir_sj=path_vak_dir_sj, path_are_sj=path_are_sj)
    assert f'Системе не удается найти указанный путь' in str(exif.value)


@pytest.mark.parametrize("name, result", [
    ('Василий', 'Василий'),
    ('Mary', 'Mary'),
    ('', 'Пользователь'),
])
def test_user_name(name, result, capsys):
    """
    Тестирование функции информирования пользователя и знакомства с ним.
    """
    assert user_name(name) == result
    # Используем фикстуру pytest - capsys builtin,
    # которая обеспечивает две функциональные возможности:
    # позволяет получить stdout и stderr из некоторого кода,
    # и временно отключить захват вывода (print).
    out, err = capsys.readouterr()
    if name != '':
        assert out == f'Очень приятно, {result}. 🤝\n\n'
        assert err == ''
    else:
        assert out == f'Хорошо, будем называть Вас {result}. 👌\n\n'
        assert err == ''


@pytest.mark.parametrize("name", [
    'Василий',
    'Mary',
    'Пользователь',
])
def test_exit_program(name, capsys):
    """
    Тестирование функции выхода из приложения.
    """
    with pytest.raises(SystemExit) as exif:
        exit_program(name)
        out, err = capsys.readouterr()
        assert out == f'\nДо свидания, {name}! 👋'
        assert err == ''
    assert "Работа программы завершена." in str(exif.value)


@pytest.mark.parametrize("name, num_vak, result", [
    ('Василий', '1', 1),
    ('Василий', '2', 2),
    ('Василий', '0', "Работа программы завершена."),
])
def test_service_selection_1(name, num_vak, result, capsys):
    """
    Тестирование функции выбора номера сервиса для вывода вакансий.
    Пользователь вводит: 1, 2 или 0.
    """
    if num_vak == '1' or num_vak == '2':
        num_vak = service_selection(name, num_vak)
        assert num_vak == result
    elif num_vak == '0':
        with pytest.raises(SystemExit) as exif:
            service_selection(name, num_vak)
            out, err = capsys.readouterr()
            assert out == f'\nДо свидания, {name}! 👋'
            assert err == ''
        assert result in str(exif.value)


def test_service_selection_2(capsys, monkeypatch):
    """
    Тестирование функции выбора номера сервиса для вывода вакансий.
    Пользователь вводит некорректные данные.
    """

    # inputs
    user_inputs = iter(['е', '5', 'x'])
    # expected
    prompt_expected = ""
    # Monkey patching
    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))
    service_selection('Василий', next(user_inputs))
    out, err = capsys.readouterr()
    assert out == prompt_expected


@pytest.mark.parametrize("service, name, area_vak, result", [
    ('hh', 'Василий', 'Ростовская область', 1530),
    ('hh', 'Василий', 'Ростов-на-Дону', 76),
    ('hh', 'Василий', 'error', 113),
    ('sj', 'Василий', 'Ростов-на-Дону', 73),
    ('sj', 'Василий', 'Санкт-Петербург', 14),
    ('sj', 'Василий', 'error', 1),
])
def test_choosing_region(service, name, area_vak, result, capsys, monkeypatch):
    """
    Тестирование функции поиска id региона/населённого пункта
    """

    test_id = search_area_id(area_vak, service, name)

    assert test_id == result


@pytest.mark.parametrize("num_area, name, result", [
    ('1', 'Василий', (True, False)),
    ('2', 'Василий', (True, True)),
    ('0', 'Василий', 'Работа программы завершена.'),
    ('error', 'Василий', (False, False))
])
def test_selection_menu_sections_id(num_area, name, result, capsys):
    """
    Тестирование функции выбора пунктов меню для поиска id региона/населённого пункта.
    """
    if num_area == '1' or num_area == '2':
        all_ok_area, all_ok = selection_menu_sections_id(num_area, name)
        assert all_ok_area == result[0]
        assert all_ok == result[1]
    elif num_area == '0':
        with pytest.raises(SystemExit) as exif:
            selection_menu_sections_id(num_area, name)
            out, err = capsys.readouterr()
            assert out == f'\nДо свидания, {name}! 👋'
            assert err == ''
        assert result in str(exif.value)
    else:
        all_ok_area, all_ok = selection_menu_sections_id(num_area, name)
        out, err = capsys.readouterr()
        assert out == 'Введена некорректная команда.\n\n'
        assert err == ''
        assert all_ok_area is False
        assert all_ok is False


@pytest.mark.parametrize("salary_vak, name, result", [
    ('1', 'Василий', (True, True)),
    ('2', 'Василий', (False, True)),
    ('0', 'Василий', 'Работа программы завершена.'),
    ('error', 'Василий', (False, False))
])
def test_all_ok_salary(salary_vak, name, result, capsys):
    """
    Тестирование функции выбора пунктов для отображений вакансий только с зарплатой или всех имеющихся.
    """
    if salary_vak == '1' or salary_vak == '2':
        only_with_salary, all_ok = all_ok_salary(salary_vak, name)
        assert only_with_salary == result[0]
        assert all_ok == result[1]
    elif salary_vak == '0':
        with pytest.raises(SystemExit) as exif:
            all_ok_salary(salary_vak, name)
            out, err = capsys.readouterr()
            assert out == f'\nДо свидания, {name}! 👋'
            assert err == ''
        assert result in str(exif.value)
    else:
        only_with_salary, all_ok = all_ok_salary(salary_vak, name)
        out, err = capsys.readouterr()
        assert out == 'Введена некорректная команда.\n\n'
        assert err == ''
        assert only_with_salary is False
        assert all_ok is False


@pytest.mark.parametrize("salary, result", [
    ('50000', (50000, True)),
    ('100000', (100000, True)),
    ('0', (0, False)),
    ('-5', (0, False)),
    ('error', (0, False))
])
def test_all_ok_salary_input(salary, result, capsys):
    """
    Тестирование функции выбора пунктов для отображений вакансий только с зарплатой или всех имеющихся.
    """
    try:
        if isinstance(int(salary), int):
            salary, all_ok = all_ok_salary_input(salary)
            assert salary == result[0]
            assert all_ok == result[1]
    except ValueError:
        salary, all_ok = all_ok_salary_input(salary)
        out, err = capsys.readouterr()
        assert out == 'Ошибка ввода данных. Введите целое положительное число.\n'
        assert err == ''
        assert salary == result[0]
        assert all_ok == result[1]
