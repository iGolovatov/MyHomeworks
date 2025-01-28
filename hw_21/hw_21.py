"""
Домашнее задание № 21
Выполнил студент 413 группы - Головатов Андрей
"""
import os
import pillow_avif
from PIL import Image
from pillow_heif import register_heif_opener, from_pillow as heif_from_pillow

my_image = r'C:\Users\New\PycharmProjects\MyHomeworks\hw_21\Input.jpg'

# Регистрируем форматы
register_heif_opener()

# Пример 1: Обход файловой системы

source_path = r"C:\Users\New\PycharmProjects\MyHomeworks"  # Путь к папке с изображениями

# Вариант 1: Простой обход через listdir
files = os.listdir(source_path)  # Получаем список файлов в директории
for file in files:
    full_path = os.path.join(source_path, file)  # Формируем полный путь
    if os.path.isfile(full_path):  # Проверяем что это файл
        print(f"Найден файл: {full_path}")

# Вариант 2: Рекурсивный обход через walk
for root, dirs, files in os.walk(source_path):  # root - текущая директория, dirs - папки, files - файлы
    for file in files:
        full_path = os.path.join(root, file)  # Формируем полный путь
        print(f"Найден файл: {full_path}")

# Открываем изображение
# Исходное изображение
source_image = Image.open('Input.jpg')

# Сжатие в WEBP
source_image.save(
    "output.webp",
    format='WEBP',
    quality=33
)

# Сжатие в HEIC
heif_file = heif_from_pillow(source_image)
heif_file.save(
    "output.heic",
    quality=33
)

# Сжатие в AVIF
source_image.save(
    "output.avif",
    quality=33
)


def compress_image(file_path, quality:int = 40, format: str ="avif"):
    # Поддерживаемые форматы
    supported_formats = ["webp", "avif", "heic"]
    # Проверяем формат
    if format not in supported_formats:
        raise ValueError(f"Формат {format} не поддерживается")
    # Открываем изображение
    image = Image.open(file_path)
    # Проверяем на avif webp
    if format in ["webp", "avif"]:
        image.save(f"{file_path}.{format}", format=format, quality=quality)
        return
    if format == "heic":
        heif_file = heif_from_pillow(image)
        heif_file.save(f"{file_path}.{format}", quality=quality)
        return

# Тестируем функцию на heic
compress_image(my_image, format="heic")
