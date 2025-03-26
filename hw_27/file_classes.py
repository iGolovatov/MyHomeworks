import csv
import json
from abc import ABC, abstractmethod
from typing import Any


class AbstractFile(ABC):
    """
    Интерфейс к FileHandlers
    """
    filepath: str

    @abstractmethod
    def read(self):
        """
        Метод для чтения

        :return:
        """
        pass

    @abstractmethod
    def write(self, data: Any):
        """
        Метод для записи данных в файл

        :param data: данные для записи
        :return:
        """
        pass

    @abstractmethod
    def append(self, data: Any):
        """
        Метод для добавления данных в файл

        :param data: данные для добавления
        :return:
        """
        pass


class TxtFileHandler(AbstractFile):
    """
        Класс для работы с текстовыми файлами.
    """

    def __init__(self, file_path:str):
        self.file_path = file_path

    def read(self) -> str:
        """
        Метод для чтения текстового файла.

        :return: Содержимое файла в виде строки.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()

        except FileNotFoundError:
            print('Файл не найден')
            return ''
        except Exception as e:
            print(f'Ошибка при чтении файла: {e}')
            return ''

    def write(self, *data: str) -> None:
        """
        Метод для записи данных в текстовый файл.

        :param data: Данные для записи в файл (строки)

        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(''.join(data))
        except Exception as e:
            print(f'Ошибка при записи файла: {e}')

    def append(self, *data: str) -> None:
        """
        Метод для добавления данных в текстовый файл.

        :param data: Данные для добавления в файл (строки)
        """
        try:
            with open(self.file_path, 'a', encoding='utf-8') as f:
                f.write(''.join(data))
        except Exception as e:
            print(f'Ошибка при добавлении данных в файл: {e}')


class CSVFileHandler(AbstractFile):
    """
    Класс для работы с CSV-файлами.
    """

    def __init__(self, file_path:str):
        self.file_path = file_path

    def read(self) -> list[dict]:
        """
        Метод для чтения CSV-файла.

        :return: Список словарей с данными из файла.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            print('Файл не найден')
            return []
        except Exception as e:
            print(f'Ошибка при чтении файла: {e}')
            return []


    def write(self, data: list[dict]) -> None:
        """
        Метод для записи данных в CSV-файл.

        :param data: Данные для записи в файл (список словарей).
        """
        if not data:
            print('Обязательный параметр data не может быть пустым')
            return
        try:
            with open(self.file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            print(f'Ошибка при записи файла: {e}')

    def append(self, data: list[dict]) -> None:
        """
        Метод для добавления данных в CSV-файл.

        :param data: Данные для добавления в файл (список словарей).
        """
        if not data:
            print('Обязательный параметр data не может быть пустым')
            return

        try:
            existing_data = self.read()
            combined_data = existing_data + data
            self.write(combined_data)
        except Exception as e:
            print(f'Ошибка при добавлении данных в файл: {e}')


class JSONFileHandler(AbstractFile):
    """
    Класс для работы с JSON-файлами.
    """

    def __init__(self, file_path:str):
        self.file_path = file_path

    def read(self) -> list[dict]:
        """
        Метод для чтения JSON-файла.

        :return: Список словарей с данными из файла
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print('Файл не найден')
            return []
        except json.JSONDecodeError:
            print('Не удалось декодировать данные')
            return []
        except Exception as e:
            print(f'Ошибка при чтении файла: {e}')
            return []

    def write(self, data: list[dict]) -> None:
        """
        Метод для записи данных в JSON-файл.

        :param data: Данные для записи в файл (список словарей)
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f'Ошибка при записи файла: {e}')

    def append(self, data: list[dict]) -> None:
        """
        Метод для добавления данных в JSON-файл.

        :param data: Данные для добавления в файл (список словарей)
        """
        try:
            existing_data = self.read()
            combined_data = existing_data + data
            self.write(combined_data)
        except Exception as e:
            print(f'Ошибка при добавлении данных в файл: {e}')
