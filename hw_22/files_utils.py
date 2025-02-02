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


# Функции для работы с CSV файлами

def read_csv(file_path: str, delimiter=';', encoding: str = 'utf-8') -> list[dict[Any, Any]]:
    """
    Функция для чтения csv файла
    :param file_path: Путь к файлу
    :param delimiter: Разделитель (по умолчанию ";")
    :param encoding: Кодировка файла (по умолчанию "utf-8")
    :return: Данные в виде списка, считанные из файла
    """
    try:
        with open(file_path, encoding=encoding) as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            return list(reader)
    except FileNotFoundError:
        print(f'Файл {file_path} не найден')
        return []


def write_csv(*data: dict, file_path: str, delimiter=';', encoding: str = 'utf-8') -> None:
    """
    Функция для записи данных в csv файл
    :param data: Данные для записи
    :param file_path: Путь к файлу
    :param delimiter: Разделитель (по умолчанию ";")
    :param encoding: Кодировка файла (по умолчанию "utf-8")
    :return: None
    """
    with (open(file_path, 'w', encoding=encoding) as f):
        writer = csv.DictWriter(
            f,
            delimiter=delimiter,
            fieldnames=data[0].keys(),
        )
        writer.writeheader()
        writer.writerows(data)


def append_csv(*data: dict, file_path: str, delimiter=';', encoding: str = 'utf-8') -> None:
    """
    Функция для добавления данных в csv файл
    :param data: Данные для записи
    :param file_path: Путь к файлу
    :param delimiter: Разделитель (по умолчанию ";")
    :param encoding: Кодировка файла (по умолчанию "utf-8")
    :return: None
    """
    with open(file_path, mode='a', encoding=encoding) as f:
        csv.DictWriter(
            f,
            delimiter=delimiter,
            fieldnames=data[0].keys(),
        ).writerows(data)

# Функции для работы с TXT файлами

def read_txt(file_path: str, encoding: str = 'utf-8') -> list[str]:
    """
    Функция для чтения txt файла
    :param file_path:
    :param encoding:
    :return:
    """
    try:
        with open(file_path, encoding=encoding) as f:
            return f.readlines()
    except FileNotFoundError:
        print(f'Файл {file_path} не найден')
        return []


def write_txt(*data: str, file_path: str, encoding: str = 'utf-8') -> None:
    """
    Функция для записи данных в txt файл
    :param data:
    :param file_path:
    :param encoding:
    :return:
    """
    with open(file_path, 'w', encoding=encoding) as f:
        f.write('\n'.join(data))


def append_txt(*data: str, file_path: str, encoding: str = 'utf-8') -> None:
    """
    Функция для добавления данных в txt файл
    :param data:
    :param file_path:
    :param encoding:
    :return:
    """
    try:
        with open(file_path, 'a', encoding=encoding) as f:
            f.write('\n' + '\n'.join(data))
    except FileNotFoundError:
        write_txt(*data, file_path=file_path, encoding=encoding)

# Функция для работы с YAML

def read_yaml(file_path: str) -> list[dict[str, Any]]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f'Файл {file_path} не найден')
        return []
