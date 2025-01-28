"""
Домашнее задание № 21
Выполнил студент 413 группы - Головатов Андрей
"""

from PIL import Image
from pillow_heif import register_heif_opener, from_pillow as heif_from_pillow

my_image = r'C:\Users\New\PycharmProjects\MyHomeworks\hw_21\Input.jpg'

# Регистрируем форматы
register_heif_opener()

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
