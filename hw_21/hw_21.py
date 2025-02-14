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

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'dng']

# Пример 1: Обход файловой системы

source_path = r"C:\Users\New\PycharmProjects\MyHomeworks"  # Путь к папке с изображениями

# # Вариант 1: Простой обход через listdir
# files = os.listdir(source_path)  # Получаем список файлов в директории
# for file in files:
#     full_path = os.path.join(source_path, file)  # Формируем полный путь
#     if os.path.isfile(full_path):  # Проверяем что это файл
#         print(f"Найден файл: {full_path}")
#
# # Вариант 2: Рекурсивный обход через walk
# for root, dirs, files in os.walk(source_path):  # root - текущая директория, dirs - папки, files - файлы
#     for file in files:
#         full_path = os.path.join(root, file)  # Формируем полный путь
#         print(f"Найден файл: {full_path}")

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


def compress_image(file_path, quality: int = 40, format: str = "avif") -> None:
    """
    Сжимает изображение в указанный формат с заданным качеством.

    Параметры:
        file_path (str): Путь к исходному файлу изображения
        quality (int): Качество сжатия (1-100), по умолчанию 40
        format (str): Выходной формат ('webp', 'avif', или 'heic')
    """
    # Поддерживаемые форматы
    supported_formats = ["webp", "avif", "heic"]
    # Проверяем формат
    if format not in supported_formats:
        raise ValueError(f"Формат {format} не поддерживается")
    # Открываем изображение
    image = Image.open(file_path)
    # Отрезаем от file_path .расширение - чтобы на выходе не получать file.png.webp
    file_path = file_path.split(".")[-2]
    # Проверяем на avif webp
    if format in ["webp", "avif"]:
        image.save(f"{file_path}.{format}", format=format, quality=quality)
        return
    if format == "heic":
        heif_file = heif_from_pillow(image)
        heif_file.save(f"{file_path}.{format}", quality=quality)
        return


def get_images_paths(source_path: str, allowed_extensions: list[str]) -> list[str]:
    """
    Рекурсивно сканирует директорию или проверяет отдельный файл на наличие допустимых изображений.

    Параметры:
        source_path (str): Путь к директории или файлу для сканирования
        allowed_extensions (list[str]): Список разрешенных расширений файлов
    """
    # Проверяем существование пути
    if not os.path.exists(source_path):
        raise ValueError(f"Путь {source_path} не существует")

    # Проверяем, папка или файл
    if os.path.isfile(source_path):
        return [source_path]

    # Мы поняли что на входе папка и рекурсивно обходим её собирая файлы указанных расширений
    images = []
    for root, dirs, files in os.walk(source_path):
        for file in files:
            full_path = os.path.join(root, file)
            if os.path.isfile(full_path):
                if file.split(".")[-1] in allowed_extensions:
                    images.append(full_path)

    return images

def main() -> None:
    """
    Основная точка входа программы.
    """
    user_path = input('Введите путь к папке или файлу: ')

    images = get_images_paths(user_path, ALLOWED_EXTENSIONS)

    for image in images:
        compress_image(image, format="webp")

if __name__ == '__main__':
    main()


