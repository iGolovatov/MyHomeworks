# Работа с TXT файлами
from file_classes import TxtFileHandler, CSVFileHandler, JSONFileHandler


def test_txt_file_handler():
    txt_handler = TxtFileHandler("example.txt")
    txt_handler.write("Начало файла.\n")
    txt_handler.append("Добавляем строку.\n")
    content_txt = txt_handler.read()
    print("Содержимое TXT:\n", content_txt)

def test_csv_file_handler():
    csv_handler = CSVFileHandler("example.csv")
    data_csv = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    csv_handler.write(data_csv)
    csv_handler.append([{'name': 'Charlie', 'age': '35'}])
    content_csv = csv_handler.read()
    print("Содержимое CSV:\n", content_csv)

def test_json_file_handler():
    json_handler = JSONFileHandler("example.json")
    data_json = [{'product': 'Laptop', 'price': 1500}, {'product': 'Phone', 'price': 800}]
    json_handler.write(data_json)
    json_handler.append([{'product': 'Tablet', 'price': 600}])
    content_json = json_handler.read()
    print("Содержимое JSON:\n", content_json)

if __name__ == '__main__':
    test_txt_file_handler()
    test_csv_file_handler()
    test_json_file_handler()
