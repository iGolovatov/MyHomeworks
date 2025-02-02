from files_utils import (
    read_json,
    write_json,
    append_json,
    read_csv,
    write_csv,
    append_csv,
    read_txt,
    write_txt,
    append_txt,
    read_yaml,
)


data = {'name': 'Andrew', 'age': 32, 'city': 'Novosibirsk'}
new_data = {'name': 'Maxim', 'age': 22, 'city': 'Novosibirsk'}

def test_json() -> None:
    """
    Тестирование функций для работы с JSON файлами
    :return:
    """
    read_json('test.json')

    write_json(data, file_path='test.json')
    read_data = read_json('test.json')
    print(read_data)

    append_json(new_data, file_path='test.json')
    read_data = read_json('test.json')
    print(read_data)

def test_csv() -> None:
    """
    Тестирование функций для работы с CSV файлами
    :return:
    """
    read_csv('test.csv')

    write_csv(data, file_path='test.csv')
    read_data = read_csv('test.csv')
    print(read_data)

    append_csv(new_data, file_path='test.csv')
    read_data = read_csv('test.csv')
    print(read_data)

def test_txt() -> None:
    """
    Тестирование функций для работы с TXT файлами
    :return:
    """
    read_txt('test.txt')

    write_txt(str(list(data.keys())), str(list(data.values())), file_path='test.txt')
    read_data = read_txt('test.txt')
    print(read_data)

    append_txt(str(list(new_data.values())), file_path='test.txt')
    read_data = read_txt('test.txt')
    print(read_data)

def test_yaml() -> None:
    """
    Тестирование функций для работы с YAML файлами
    :return:
    """
    print(read_yaml('test.yaml'))

test_json()
test_txt()
test_csv()
test_yaml()
