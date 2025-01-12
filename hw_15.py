# Запрашиваем количество секунд у пользователя
user_seconds = int(input('Введите количество секунд: '))
# Переводим полученное значение в часы
hours = user_seconds //3600
# Переводим полученное значение в минуты
minutes = (user_seconds % 3600) // 60
# Переводим полученное значение в секунды
seconds = user_seconds % 60
# Выводим информацию
print(f'В указанном количестве секунд {user_seconds}:\n{hours} час.\n{minutes} мин.\n{seconds} сек.')

# Запрашиваем у пользователя температуру в Цельсиях
user_temperature = float(input('Введите температуру в Цельсиях: '))
# Переводим из Цельсий в Кельвин
temperature_k = user_temperature + 273.15
# Переводим из Цельсий в Фаренгейт
temperature_f = (user_temperature * (9/5)) + 32
# Переводим из Цельсий в Реомюр
temperature_r = (user_temperature * (4/5))
# Выводим информацию
print(f'Кельвин: {temperature_k} K\nФаренгейт: {temperature_f:.2f} °F\nРеомюр: {temperature_r:.2f} °Re')

