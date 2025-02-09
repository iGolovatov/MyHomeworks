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


print('Part 2')

def password_validator(
    min_length: int = 8,
    min_uppercase: int = 1,
    min_digits: int = 1,
    min_lowercase: int = 1,
    min_special_chars: int = 1,
):
    """
    Функция-декоратор для валидации пароля пользователя
    :param min_length:
    :param min_uppercase:
    :param min_digits:
    :param min_lowercase:
    :param min_special_chars:
    :return:
    """
    def decorator(func: Callable[[str, str], None]) -> Callable[[str, str], None]:
        def wrapper(username: str, password: str) -> None:
            if len(password) < min_length:
                raise ValueError(f'Пароль менее {min_length} символов!')
            if len(re.findall(r'([0-9])', password)) < min_digits:
                raise ValueError(f'Пароль должен содержать не менее {min_digits} цифр!')
            if len(re.findall(r'([A-Z])', password)) < min_uppercase:
                raise ValueError(f'Пароль должен содержать не менее {min_uppercase} заглавных букв!')
            if len(re.findall(r'([a-z])', password)) < min_lowercase:
                raise ValueError(f'Пароль должен содержать не менее {min_lowercase} строчных букв!')
            if len(re.findall(r'[!@#$%^&]', password)) < min_special_chars:
                raise ValueError(f'Пароль должен содержать не менее {min_special_chars} специальных символов!')

            return func(username, password)

        return wrapper

    return decorator

def username_validator(func: Callable[[str, str], None]) -> Callable[[str, str], None]:
    """
    Функция-декоратор для проверки логина пользователя
    :param func:
    :return:
    """
    def wrapper(username: str, password: str) -> None:
        if username.find(' ') != -1:
            raise ValueError('Имя пользователя не должно содержать пробелы')

        return func(username, password)

    return wrapper

file_path = 'Login&Password.csv'


