import re
import csv

from typing import Callable


def password_checker(func: Callable[[str], None]) -> Callable[[str], None]:
    """
    Функция-декоратор для проверки пароля.
    :param func: Функция принимающая пароль в виде аргумента
    :return:
    """

    def wrapper(password: str) -> None:
        if len(password) < 8:
            print('Пароль менее 8 символов!')
            return
        if not re.findall(r'([0-9])', password):
            print('Пароль не содержит цифр!')
            return
        if not re.findall(r'([A-Z])', password):
            print('Пароль не содержит заглавных букв!')
            return
        if not re.findall(r'([a-z])', password):
            print('Пароль не содержит строчных букв')
            return
        if not re.findall(r'[!@#$%^&]', password):
            print('Пароль не содержит специальных символов!')
            return

        return func(password)

    return wrapper


@password_checker
def register_user(password: str):
    print(f'Пользователь зарегистрирован! Пароль: {password}')

print('Part 1')
register_user(input('Введите пароль: '))
