import json
from dataclasses import dataclass, field
from typing import Any, List, Dict

JSON_DATA = 'cities.json'


class JsonHandler:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path

    def read(self) -> List[Dict[str, Any]]:
        """
        Читает данные из json файла. Ensure_ascii=False - сохраняет русские символы
        Encoding='utf-8' - кодировка файла

        Returns:
            List[Dict[str, Any]]: Список словарей с данными о городах
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)


@dataclass
class City:
    name: str = field(compare=False)
    population: int
    subject: str = field(compare=False)
    district: str = field(compare=False)
    latitude: float = field(compare=False)
    longitude: float = field(compare=False)
    is_used: bool = field(compare=False, default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        self.__validate_name()
        self.__validate_population()

    def __validate_name(self) -> None:
        """
        Проверяет корректность имени города

        Raises:
            ValueError: Если имя не является строкой или пустое
        """
        if not isinstance(self.name, str) or not self.name:
            raise ValueError(f'Name должен быть строкой и не пустым')

    def __validate_population(self) -> None:
        """
        Проверяет корректность значения населения

        Raises:
            ValueError: Если население не является положительным числом
        """
        if not isinstance(self.population, int) or self.population <= 0:
            raise ValueError(f'Population должен быть положительным числом')


class CitiesSerializer:
    def __init__(self, city_data: List[Dict[str, Any]]) -> None:
        self.city_data: List[Dict[str, Any]] = city_data
        self.cities: List[City] = self.__create_cities()

    def __deserialize_city(self, city_dict: Dict[str, Any]) -> City:
        """
        Создает объект City из словаря с данными

        Args:
            city_dict: Словарь с данными о городе

        Returns:
            City: Объект класса City
        """
        instance = City(
            name=city_dict['name'],
            population=city_dict['population'],
            subject=city_dict['subject'],
            district=city_dict['district'],
            latitude=city_dict['coords']['lat'],
            longitude=city_dict['coords']['lon'],
        )

        return instance

    def __create_cities(self) -> List[City]:
        """
        Создает список объектов City из списка словарей

        Returns:
            List[City]: Список объектов класса City
        """
        return [self.__deserialize_city(city) for city in self.city_data]

    def get_cities(self) -> List[City]:
        """
        Возвращает список городов

        Returns:
            List[City]: Список объектов класса City
        """
        return self.cities


# Реализуем тест на работоспособность кода
def main() -> None:
    """
    Основная функция для тестирования работы кода
    """
    json_handler = JsonHandler(JSON_DATA)
    city_data = json_handler.read()
    cities_serializer = CitiesSerializer(city_data)
    cities = cities_serializer.get_cities()
    print(cities[2])
    print(cities[99])


if __name__ == "__main__":
    main()
