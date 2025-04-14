import json
import random
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional

JSON_DATA = 'cities.json'


class JsonHandler:
    def __init__(self, file_path: str) -> None:
        """
        Инициализация обработчика JSON.

        Args:
            file_path (str): Путь к файлу JSON.
        """
        self.file_path: str = file_path

    def read(self) -> List[Dict[str, Any]]:
        """
        Читает данные из JSON файла.

        Returns:
            List[Dict[str, Any]]: Список словарей с данными о городах.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл '{self.file_path}' не найден.")
        except json.JSONDecodeError:
            raise ValueError(f"Ошибка декодирования JSON в файле '{self.file_path}'.")


@dataclass
class City:
    name: str = field(compare=False)
    population: int
    subject: str = field(compare=False)
    district: str = field(compare=False)
    latitude: float = field(compare=False)
    longitude: float = field(compare=False)
    is_used: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        """
        Проверяет корректность данных города после инициализации.
        """
        self.__validate_name()
        self.__validate_population()

    def __validate_name(self) -> None:
        """
        Проверяет корректность имени города.

        Raises:
            ValueError: Если имя не является строкой или пустое.
        """
        if not isinstance(self.name, str) or not self.name:
            raise ValueError('Name должен быть строкой и не пустым')

    def __validate_population(self) -> None:
        """
        Проверяет корректность значения населения.

        Raises:
            ValueError: Если население не является положительным числом.
        """
        if not isinstance(self.population, int) or self.population <= 0:
            raise ValueError('Population должен быть положительным числом')


class CitiesSerializer:
    def __init__(self, city_data: List[Dict[str, Any]]) -> None:
        """
        Инициализация сериализатора городов.

        Args:
            city_data (List[Dict[str, Any]]): Данные о городах в виде списка словарей.
        """
        self.city_data: List[Dict[str, Any]] = city_data
        self.cities: List[City] = self.__create_cities()

    def __deserialize_city(self, city_dict: Dict[str, Any]) -> City:
        """
        Создает объект City из словаря с данными.

        Args:
            city_dict (Dict[str, Any]): Словарь с данными о городе.

        Returns:
            City: Объект класса City.
        """
        return City(
            name=city_dict['name'],
            population=city_dict['population'],
            subject=city_dict['subject'],
            district=city_dict['district'],
            latitude=city_dict['coords']['lat'],
            longitude=city_dict['coords']['lon'],
        )

    def __create_cities(self) -> List[City]:
        """
        Создает список объектов City из списка словарей.

        Returns:
            List[City]: Список объектов класса City.
        """
        return [self.__deserialize_city(city) for city in self.city_data]

    def get_cities(self) -> List[City]:
        """
        Возвращает список городов.

        Returns:
            List[City]: Список объектов класса City.
        """
        return self.cities


class CityGame:
    def __init__(self, cities_serializer: CitiesSerializer) -> None:
        """
        Инициализация игры "Города".

        Args:
            cities_serializer (CitiesSerializer): Объект класса CitiesSerializer с данными о городах.
        """
        self.cities: List[City] = cities_serializer.get_cities()
        self.available_cities: List[City] = self.cities.copy()
        self.used_cities: List[City] = []
        self.last_city: Optional[City] = None
        self.last_letter: Optional[str] = None
        self.game_over: bool = False
        self.winner: Optional[str] = None

    def start_game(self, computer_first: bool = False) -> None:
        """
        Запускает игровой цикл.

        Args:
            computer_first (bool): Флаг, определяющий, кто ходит первым (True - компьютер, False - человек).
        """
        print("Добро пожаловать в игру 'Города'!")
        print("Правила: назовите город, начинающийся на последнюю букву предыдущего города.")
        print("Для выхода введите 'выход' или 'exit'.")

        if computer_first:
            self.computer_turn()

        while not self.game_over:
            city_input = input("\nВаш ход (введите название города): ").strip()
            if city_input.lower() in ['выход', 'exit']:
                print("Игра завершена по вашему запросу.")
                return

            if self.human_turn(city_input):
                print(f"Вы назвали город: {city_input}")
                self.computer_turn()

    def human_turn(self, city_input: str) -> bool:
        """
        Обрабатывает ход человека.

        Args:
            city_input (str): Название города, введенное игроком.

        Returns:
            bool: True, если ход корректен, False в противном случае.
        """
        city_obj = self.__find_city(city_input)

        if not city_obj:
            print(f"Город '{city_input}' не найден в базе или уже был использован.")
            self.game_over = True
            self.winner = "Компьютер"
            print("Вы ввели несуществующий или уже использованный город. Компьютер победил!")
            return False

        if self.last_letter and city_input[0].lower() != self.last_letter.lower():
            print(f"Город должен начинаться на букву '{self.last_letter.upper()}'.")
            self.game_over = True
            self.winner = "Компьютер"
            print("Вы ввели город, начинающийся с неправильной буквы. Компьютер победил!")
            return False

        self.__update_game_state(city_obj)
        return True

    def computer_turn(self) -> Optional[str]:
        """
        Выполняет ход компьютера.

        Returns:
            Optional[str]: Название города, выбранного компьютером, или None, если ход невозможен.
        """
        if not self.last_letter:
            # Если это первый ход, выбираем случайный город
            if self.available_cities:
                chosen_city = random.choice(self.available_cities)
                self.__update_game_state(chosen_city)
                print(f"Компьютер называет город: {chosen_city.name}")
                return chosen_city.name
            return None

        suitable_cities = [city for city in self.available_cities if city.name[0].lower() == self.last_letter.lower()]

        if not suitable_cities:
            self.game_over = True
            self.winner = "Человек"
            print("Компьютер не может найти подходящий город. Вы победили!")
            return None

        chosen_city = random.choice(suitable_cities)
        self.__update_game_state(chosen_city)
        print(f"Компьютер называет город: {chosen_city.name}")
        return chosen_city.name

    def __find_city(self, city_input: str) -> Optional[City]:
        """
        Находит город по названию.

        Args:
            city_input (str): Название города.

        Returns:
            Optional[City]: Объект класса City, если найден, иначе None.
        """
        for city in self.available_cities:
            if city.name.lower() == city_input.lower():
                return city
        return None

    def __update_game_state(self, city_obj: City) -> None:
        """
        Обновляет состояние игры после хода.

        Args:
            city_obj (City): Объект класса City, который был назван.
        """
        self.available_cities.remove(city_obj)
        self.used_cities.append(city_obj)
        city_obj.is_used = True
        self.last_city = city_obj
        self.last_letter = self.__get_last_letter(city_obj.name)

    def __get_last_letter(self, city_name: str) -> str:
        """
        Получает последнюю букву названия города, исключая "ь", "ъ", "ы".

        Args:
            city_name (str): Название города.

        Returns:
            str: Последняя буква.
        """
        for char in reversed(city_name.lower()):
            if char not in ['ь', 'ъ', 'ы']:
                return char
        return ""

    def check_game_over(self) -> bool:
        """
        Проверяет, завершена ли игра.

        Returns:
            bool: True, если игра завершена, False в противном случае.
        """
        if not self.last_letter:
            return False

        has_suitable_cities = any(city.name[0].lower() == self.last_letter.lower() for city in self.available_cities)

        if not has_suitable_cities:
            self.game_over = True
            self.winner = "Компьютер" if self.last_city and self.last_city.is_used else "Человек"
            print(f"{self.winner} победил!")
            return True

        return False


class GameManager:
    def __init__(self, json_handler: JsonHandler, cities_serializer: CitiesSerializer, city_game: CityGame) -> None:
        """
        Инициализация менеджера игры.

        Args:
            json_handler (JsonHandler): Объект класса JsonHandler для работы с JSON.
            cities_serializer (CitiesSerializer): Объект класса CitiesSerializer с данными о городах.
            city_game (CityGame): Объект класса CityGame, реализующий логику игры.
        """
        self.json_handler: JsonHandler = json_handler
        self.cities_serializer: CitiesSerializer = cities_serializer
        self.city_game: CityGame = city_game

    def __call__(self) -> None:
        """
        Запускает игровой процесс при вызове объекта класса.
        """
        self.run_game()

    def run_game(self) -> None:
        """
        Координирует запуск всех методов для старта, хода и завершения игры.
        """
        print("=" * 50)
        print("Игра 'Города' запущена!")
        print("=" * 50)

        first_turn = input("Кто ходит первым? (1 - компьютер, 2 - вы): ").strip()
        computer_first = first_turn == "1"

        self.city_game.start_game(computer_first)
        self.display_game_result()

    def display_game_result(self) -> None:
        """
        Выводит итоговый результат игры.
        """
        if self.city_game.game_over:
            print("\n" + "=" * 50)
            print("Игра завершена!")
            if self.city_game.winner == "Человек":
                print("Поздравляем! Вы победили!")
            elif self.city_game.winner == "Компьютер":
                print("К сожалению, вы проиграли. Компьютер победил.")


def main() -> None:
    """
    Основная функция для запуска игры.
    """
    json_handler = JsonHandler(JSON_DATA)
    cities_data = json_handler.read()
    cities_serializer = CitiesSerializer(cities_data)
    city_game = CityGame(cities_serializer)
    game_manager = GameManager(json_handler, cities_serializer, city_game)
    game_manager()  # Запуск игрового процесса


if __name__ == "__main__":
    main()
