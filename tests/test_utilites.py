# Тестирование модуля utilites.py
import os

import pytest

from src.utils.utilites import loading_regions_hh, loading_regions_sj, user_name, exit_program


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
