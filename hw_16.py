name = input('Введите свое имя: ')
raw_grade  = input('Введите свою оценку: ')

if not raw_grade.isdigit():
    print('Введено некорректное значение. Пожалуйста, введите число!')
else: 
    grade = int(raw_grade)
    if 1 <= grade <= 3:
        result = 'Начальный'
    elif 4 <= grade <= 6:
        result = 'Средний'
    elif 7 <= grade <= 9:
        result = 'Достаточный'
    elif 10 <= grade <= 12:
        result = 'Высокий'
    else:
        result = None

    if result is None:
        print(f'{name}, Оценка введена некорректно. Введите значение от 1 до 12')
    else:
        print(f'{name}, Ваш уровень знаний - "{result}"')
