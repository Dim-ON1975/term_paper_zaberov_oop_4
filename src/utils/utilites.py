# Функции для модуля main.py

def user_name(name='') -> str:
    """
    Выводит приветствие для пользователя.
    :param name: Имя пользователя, str.
    :return: Вывод обращения к пользователю, имени пользователя, str.
    """
    match name:
        # Если name == ""
        case '':
            name = 'Пользователь'
            print(f'Хорошо, будем называть Вас {name}. 👌\n')
        # Сохранить имя в name, если оно не равно None
        case name:
            print(f'Очень приятно, {name}. 🤝\n')
    return name


def exit_program(name) -> None:
    """
    Выход из приложения.
    :return: Выводит сообщение и выходит из приложения.
    """
    print(f'\nДо свидания, {name}! 👋')
    raise SystemExit('Работа программы завершена.\n')
