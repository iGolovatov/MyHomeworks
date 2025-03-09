import csv
import json


class TxtFileHandler:
    """
        Класс для работы с текстовыми файлами.
    """
    def read_file(self, filepath: str) -> str:
        """
        Метод для чтения текстового файла.

        :param filepath: Путь к файлу.
        :return: Содержимое файла в виде строки.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()

        except FileNotFoundError:
            print('Файл не найден')
            return ''
        except Exception as e:
            print(f'Ошибка при чтении файла: {e}')
            return ''

    def write_file(self, filepath: str, *data: str) -> None:
        """
        Метод для записи данных в текстовый файл.

        :param filepath: Путь к файлу
        :param data: Данные для записи в файл (строки)

        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(''.join(data))
        except Exception as e:
            print(f'Ошибка при записи файла: {e}')

    def append_file(self, filepath: str, *data: str) -> None:
        """
        Метод для добавления данных в текстовый файл.

        :param filepath: Путь к файлу
        :param data: Данные для добавления в файл (строки)
        """
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(''.join(data))
        except Exception as e:
            print(f'Ошибка при добавлении данных в файл: {e}')


class CSVFileHandler:
    """
    Класс для работы с CSV-файлами.
    """
    def read_file(self, filepath: str) -> list[dict]:
        """
        Метод для чтения CSV-файла.

        :param filepath: Путь к файлу.
        :return: Список словарей с данными из файла.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            print('Файл не найден')
            return []
        except Exception as e:
            print(f'Ошибка при чтении файла: {e}')
            return []


    def write_file(self, filepath: str, data: list[dict]) -> None:
        """
        Метод для записи данных в CSV-файл.

        :param filepath: Путь к файлу.
        :param data: Данные для записи в файл (список словарей).
        """
        if not data:
            print('Обязательный параметр data не может быть пустым')
            return
        try:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            print(f'Ошибка при записи файла: {e}')

    def append_file(self, filepath: str, data: list[dict]) -> None:
        """
        Метод для добавления данных в CSV-файл.

        :param filepath: Путь к файлу.
        :param data: Данные для добавления в файл (список словарей).
        """
        if not data:
            print('Обязательный параметр data не может быть пустым')
            return

        try:
            existing_data = self.read_file(filepath)
            combined_data = existing_data + data
            self.write_file(filepath, combined_data)
        except Exception as e:
            print(f'Ошибка при добавлении данных в файл: {e}')


class JSONFileHandler:
    """
    Класс для работы с JSON-файлами.
    """

    def read_file(self, filepath: str) -> list[dict]:
        """
        Метод для чтения JSON-файла.

        :param filepath: Путь к файлу
        :return: Список словарей с данными из файла
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
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

    def write_file(self, filepath: str, data: list[dict]) -> None:
        """
        Метод для записи данных в JSON-файл.

        :param filepath: Путь к файлу
        :param data: Данные для записи в файл (список словарей)
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f'Ошибка при записи файла: {e}')

    def append_file(self, filepath: str, data: list[dict]) -> None:
        """
        Метод для добавления данных в JSON-файл.

        :param filepath: Путь к файлу
        :param data: Данные для добавления в файл (список словарей)
        """
        try:
            existing_data = self.read_file(filepath)
            combined_data = existing_data + data
            self.write_file(filepath, combined_data)
        except Exception as e:
            print(f'Ошибка при добавлении данных в файл: {e}')

# Работа с TXT файлами
txt_handler = TxtFileHandler()
txt_handler.write_file("example.txt", "Начало файла.\n")
txt_handler.append_file("example.txt", "Добавляем строку.\n")
content_txt = txt_handler.read_file("example.txt")
print("Содержимое TXT:\n", content_txt)

# Работа с CSV файлами
csv_handler = CSVFileHandler()
data_csv = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
csv_handler.write_file("example.csv", data_csv)
csv_handler.append_file("example.csv", [{'name': 'Charlie', 'age': '35'}])
content_csv = csv_handler.read_file("example.csv")
print("Содержимое CSV:\n", content_csv)

# Работа с JSON файлами
json_handler = JSONFileHandler()
data_json = [{'product': 'Laptop', 'price': 1500}, {'product': 'Phone', 'price': 800}]
json_handler.write_file("example.json", data_json)
json_handler.append_file("example.json", [{'product': 'Tablet', 'price': 600}])
content_json = json_handler.read_file("example.json")
print("Содержимое JSON:\n", content_json)
