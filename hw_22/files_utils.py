import json
import csv
import yaml

from typing import Any



# Функции для работы с JSON файлами

def read_json(file_path: str, encoding: str = 'utf-8') -> list[dict[Any, Any]]:
    """
    Функция для чтения json файла
    :param file_path: Путь к файлу
    :param encoding: Кодировка файла (по умолчанию "utf-8")
    :return: Данные в виде словаря, считанные из файла
    """
    try:
        with open(file_path, encoding=encoding) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'Файл {file_path} не найден')
        return []


def write_json(*data: dict, file_path: str, encoding: str = 'utf-8') -> None:
    """
    Функция для записи данных в json файл
    :param data: Данные для записи
    :param file_path: Путь к файлу
    :param encoding: Кодировка файла (по умолчанию "utf-8")
    :return: None
    """
    with open(file_path, 'w', encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=False)


def append_json(*data: dict, file_path: str, encoding: str = 'utf-8') -> None:
    """
    Функция для добавления данных в json файл
    :param data: Данные для записи
    :param file_path: Путь к файлу
    :param encoding: Кодировка файла (по умолчанию "utf-8")
    :return: None
    """
    try:
        with open(file_path, encoding=encoding) as f:
            old_data = json.load(f)
    except FileNotFoundError:
        return write_json(*data, file_path=file_path, encoding=encoding)

    new_data = [*old_data, *data]
    write_json(*new_data, file_path=file_path, encoding=encoding)


