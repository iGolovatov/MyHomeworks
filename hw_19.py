from marvel import small_dict

# Задача № 1
movie_name = input('Введите название фильма или его часть: ').lower()
movie_list = []
for name in small_dict:
    if name.lower().find(movie_name) != -1:
        movie_list.append(name)
if movie_list:
    print(movie_list)
else:
    print('Фильмов с таким названием не найдено.')

# Задача № 2
list_of_movie_names = []
dict_of_movies = {}
list_of_dicts_of_movies = []
for name, year in small_dict.items():
    if year is None:
        continue
    if year > 2024:
        print(name)
        list_of_movie_names.append(name)
        dict_of_movies[name] = year
        list_of_dicts_of_movies.append({name: year})
dict_of_movies = dict(sorted(dict_of_movies.items(), key=lambda d: d[1], reverse=True))
print(dict_of_movies)
print(list_of_dicts_of_movies)
