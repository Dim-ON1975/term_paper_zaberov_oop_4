# Тестирование модуля utilities.py
import os

import pytest

from src.utils.utilities import loading_regions_hh, loading_regions_sj, user_name, exit_program, service_selection


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


@pytest.mark.parametrize("name, num_vak, result", [
    ('Василий', '1', 1),
    ('Василий', '2', 2),
    ('Василий', '0', "Работа программы завершена."),
])
def test_service_selection_1(name, num_vak, result, capsys, monkeypatch):
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
    else:
        with pytest.raises(ValueError) as exif:
            # inputs
            user_inputs = iter(['1', '2', '0'])
            # expected
            prompt_expected = "\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: \n" + \
                              "\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: \n" + \
                              "\n❗{name}, Вы ввели некорректную команду. Попробуйте ещё раз: "
            # Monkey patching
            monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))
            service_selection(name, num_vak)
            out, err = capsys.readouterr()
            print(f'out: {out}')
        assert out == prompt_expected


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
    print(f'out: {out}')
    print(f'err: {err}')
    assert out == prompt_expected
