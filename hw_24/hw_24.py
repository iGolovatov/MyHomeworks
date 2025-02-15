"""
Домашнее задание № 24
Выполнил студент 413 группы - Головатов Андрей

В этом задании буду работать с дата-сетом Marvel, применяя различные функции Python для обработки данных
"""

from pprint import pprint
from typing import Callable

from marvel import full_dict

user_input: str = input("Введите цифры: ")


def safe_int(digit: str) -> int | None:
    try:
        return int(digit)
    except ValueError:
        return None


list_ids: list[int | None] = list(map(safe_int, user_input.split()))
print('Пользовательские индексы:')
pprint(list_ids)

list_of_movies: list[dict[str, int | str | None]] = [{"id": film_id, **film} for film_id, film in full_dict.items()]
print('Список фильмов:}')
pprint(list_of_movies)

expression: Callable[[dict[str, int | str | None]], bool] = lambda film: film['id'] in list_ids

filtered_list: list[dict[str, int | str | None]] = list(filter(expression, list_of_movies))
print('Список фильмов по индексам:')
pprint(filtered_list)

unique_directors: set[str] = {film['director'] for film in full_dict.values()}
print('Уникальные режиссеры:')
pprint(unique_directors)

converted_full_dict: dict[int, dict[str, str | None]] = {
    key: {**value, 'year': str(value['year'])}
    for key, value in full_dict.items()
}

expression = lambda film: str(film['title']).startswith('Ч')
filtered_list_ch: list[dict[str, int | str | None]] = list(filter(expression, list_of_movies))
print('Фильмы, начинающиеся с буквы "Ч"')
pprint(filtered_list_ch)

sorted_dict_by_year: dict[int, dict[str, int | str | None]] = dict(
    sorted(
        full_dict.items(),
        key=lambda item: item[1]['year'] if isinstance(item[1]['year'], int) else 0,
        reverse=True,
    ),
)
print('Сортировка по году по убыванию:')
pprint(sorted_dict_by_year, sort_dicts=False)

sorted_dict_by_stage: dict[int, dict[str, int | str | None]] = dict(
    sorted(
        full_dict.items(),
        key=lambda item: item[1]['director'] or "",
    ),
)
print('Сортировка по директору:')
pprint(sorted_dict_by_stage, sort_dicts=False)

# Однострочник, который фильтрует и сортирует словарь по году выпуска фильма (с соблюдением PEP-8)
filtered_and_sorted_dict: dict[int, dict[str, int | str | None]] = dict(
    sorted(
        filter(
            lambda item: isinstance(item[1]['year'], int),
            full_dict.items(),
        ),
        key=lambda item: item[1]['year'] or 0,
        reverse=True,
    ),
)

print('Однострочник, который фильтрует и сортирует словарь по году выпуска фильма:')
pprint(filtered_and_sorted_dict)

# (.venv) PS C:\Users\New\PycharmProjects\MyHomeworks> mypy .\hw_24\hw_24.py
# Success: no issues found in 1 source file

