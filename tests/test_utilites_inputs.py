# Модуль тестирования вводов

from typing import Callable
import pytest

from src.utils.utilities import num_area_input, name_vak_word, salary_vak_input, error_input, \
    salary_input, area_vak_input, sort_method_input, program_info, service_menu_selection, reselect_position


def _create_patched_input(str_list: list[str]) -> Callable:
    """
    Создание исправленных входных данных.
    :param str_list: Список входных данных, list.
    :return: Исправленные входные данные.
    """

    str_iter = iter(str_list.copy())

    # имеет ту же сигнатуру, что и ввод
    def patched_input(prompt: str) -> str:
        val = next(str_iter)
        print(prompt + val, end="\n"),
        return val

    return patched_input


@pytest.fixture
def _mock_input(monkeypatch, inputs: list[str]) -> None:
    """
    Макет ввода.
    :param monkeypatch: Фикстура, предоставляющая методы для изменения объектов, словарей или os.environ.
    :param inputs: Словарь входных данных, str.
    """
    patched_input = _create_patched_input(inputs)
    # Временное изменение объекта, на который указыает имя, на другой.
    monkeypatch.setattr("builtins.input", patched_input)


# Объявляем использование фикстуры.

@pytest.mark.usefixtures("_mock_input")
@pytest.mark.parametrize(
    "inputs",
    (["Вася", "Петя"], ["Маша", ""]),
)
def test_program_info(inputs):
    """
    Тестирование функции program_info.
    """
    for name in inputs:
        assert program_info() == name


@pytest.mark.usefixtures("_mock_input")
@pytest.mark.parametrize(
    "inputs",
    (["1", "2"], ["0", "error"]),
)
def test_menu_selection(inputs):
    """
    Тестирование функции service_menu_selection.
    """
    for name in inputs:
        assert service_menu_selection() == name


@pytest.mark.usefixtures("_mock_input")
@pytest.mark.parametrize(
    "inputs",
    (["ростовская область", "ростов-на-дону"], ["санкт-петербург", "error"]),
)
def test_area_vak_input(inputs):
    """
    Тестирование функции num_area_word.
    """
    for name in inputs:
        assert area_vak_input() == name


@pytest.mark.usefixtures("_mock_input")
@pytest.mark.parametrize(
    "inputs",
    (["1", "2"], ["0", "error"]),
)
def test_num_area_input(inputs):
    """
    Тестирование функции num_area_word.
    """
    for name in inputs:
        assert num_area_input() == name


@pytest.mark.usefixtures("_mock_input")
@pytest.mark.parametrize(
    "inputs",
    (['е', '5', 'x'], ["b", "10", "error"]),
)
def test_error_input(inputs):
    """
    Тестирование функции ввод данных при возникновении ошибки
    при выборе пункта меню.
    Пользователь вводит некорректные данные.
    """
    for name in inputs:
        assert error_input(f'\n❗Василий, Вы ввели некорректную команду. Попробуйте ещё раз: ') == name


@pytest.mark.usefixtures("_mock_input")
@pytest.mark.parametrize(
    "inputs",
    (['ростовская область', 'краснодар', 'errors'], ["5", "10", "8"]),
)
def test_name_vak_word(inputs):
    """
    Тестирование функции ввод данных при возникновении ошибки
    при выборе номера сервиса для вывода вакансий.
    Пользователь вводит некорректные данные.
    """
    for name in inputs:
        assert name_vak_word('Василий') == name


@pytest.mark.usefixtures("_mock_input")
@pytest.mark.parametrize(
    "inputs",
    (["1", "2"], ["0", "error"]),
)
def test_salary_vak_input(inputs):
    """
    Тестирование функции выбора пункта меню
    для отображения вакансий всех или только с зарплатой.
    """
    for name in inputs:
        assert salary_vak_input() == name


@pytest.mark.usefixtures("_mock_input")
@pytest.mark.parametrize(
    "inputs",
    (["50000", "100000"], ["0", "error"]),
)
def test_salary_input(inputs):
    """
    Тестирование функции ввода ожидаемого размера заработной платы.
    """
    for name in inputs:
        assert salary_input() == name


@pytest.mark.usefixtures("_mock_input")
@pytest.mark.parametrize(
    "inputs",
    (["1", "2"], ["0", "error"]),
)
def test_sort_method_input(inputs):
    """
    Тестирование функции num_area_word.
    """
    for name in inputs:
        assert sort_method_input() == name


@pytest.mark.usefixtures("_mock_input")
@pytest.mark.parametrize(
    "inputs",
    (["1", "2"], ["0", "error"]),
)
def test_reselect_position(inputs):
    """
    Тестирование функции reselect_position.
    """
    for name in inputs:
        assert reselect_position() == name
