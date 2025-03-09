import os
from PIL import Image
from pillow_heif import register_heif_opener


class ImageCompressor:

    supported_formats = ('.jpg', '.jpeg', '.png')

    def __init__(self, quality: int = 50):
        """
        Конструктор класса.

        Args:
            quality (int): Качество сжатия изображения (от 1 до 100).

        Raises:
            ValueError: Если значение выходит за пределы допустимого диапазона (1-100).
            TypeError: Если значение не целочисленное.
        """
        if not isinstance(quality, int):
            raise TypeError("Качество сжатия должно быть целым числом.")
        if not 1 <= quality <= 100:
            raise ValueError("Качество сжатия должно быть в диапазоне от 1 до 100.")
        self.__quality = quality

    @property
    def quality(self) -> int:
        """
        Геттер для свойства quality.

        Returns:
            int: Текущее значение качества сжатия.
        """
        return self.__quality

    @quality.setter
    def quality(self, quality: int) -> None:
        """
        Сеттер для свойства quality.

        Args:
            quality (int): Новое значение качества сжатия.

        Raises:
            ValueError: Если значение выходит за пределы допустимого диапазона (1-100).
            TypeError: Если значение не целочисленное.
        """
        if not isinstance(quality, int):
            raise TypeError("Качество сжатия должно быть целым числом.")
        if not 1 <= quality <= 100:
            raise ValueError("Качество сжатия должно быть в диапазоне от 1 до 100.")
        self.__quality = quality

    def compress_image(self, input_path: str, output_path: str) -> None:
        """
        Сжимает изображение и сохраняет его в формате HEIF.

        Args:
            input_path (str): Путь к исходному изображению.
            output_path (str): Путь для сохранения сжатого изображения.

        Returns:
            None
        """
        with Image.open(input_path) as img:
            img.save(output_path, "HEIF", quality=self.__quality)
        print(f"Сжато: {input_path} -> {output_path}")

    def process_directory(self, directory: str) -> None:
        """
        Обрабатывает все изображения в указанной директории и её поддиректориях.

        Args:
            directory (str): Путь к директории для обработки.

        Returns:
            None
        """
        for root, _, files in os.walk(directory):
            for file in files:
                # Проверяем расширение файла
                if file.lower().endswith(self.supported_formats):
                    input_path = os.path.join(root, file)
                    output_path = os.path.splitext(input_path)[0] + '.heic'
                    self.compress_image(input_path, output_path)


def main() -> None:
    """
    Основная функция программы. Обрабатывает входной путь и запускает сжатие изображений.

    Returns:
        None
    """
    register_heif_opener()

    user_input: str = input("Введите путь к файлу или директории: ").strip('"')

    if not os.path.exists(user_input):
        print("Указанный путь не существует")
        return

    compressor = ImageCompressor(quality=50)

    if os.path.isfile(user_input):
        # Если указан путь к файлу, обрабатываем только этот файл
        print(f"Обрабатываем файл: {user_input}")
        output_path = os.path.splitext(user_input)[0] + '.heic'
        compressor.compress_image(user_input, output_path)
    elif os.path.isdir(user_input):
        # Если указан путь к директории, обрабатываем все файлы в ней
        print(f"Обрабатываем директорию: {user_input}")
        compressor.process_directory(user_input)


if __name__ == "__main__":
    main()