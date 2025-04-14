from abc import ABC, abstractmethod

class PalindromeStrategy(ABC):
    @abstractmethod
    def is_palindrome(self, text: str) -> bool:
        pass

class SingleWordPalindrome(PalindromeStrategy):
    def is_palindrome(self, text: str) -> bool:
        text = text.lower()
        return text == text[::-1]

class MultiWordPalindrome(PalindromeStrategy):
    def is_palindrome(self, text: str) -> bool:
        text = ''.join(text.lower().split())
        return text == text[::-1]

class PalindromeContext:
    def __init__(self, strategy: PalindromeStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: PalindromeStrategy) -> None:
        self.strategy = strategy

    def check(self, text: str) -> bool:
        return self.strategy.is_palindrome(text)

class PalindromeFacade:
    def __init__(self):
        self.context = PalindromeContext(SingleWordPalindrome())

    def check_palindrome(self, text: str) -> bool:
        if ' ' in text:
            self.context.set_strategy(MultiWordPalindrome())
        else:
            self.context.set_strategy(SingleWordPalindrome())
        return self.context.check(text)

if __name__ == "__main__":
    facade = PalindromeFacade()

    # Тест 1: Одиночное слово-палиндром
    word = "Racecar"
    print(f"'{word}' — палиндром? {facade.check_palindrome(word)}")  # True

    # Тест 2: Одиночное слово не палиндром
    word = "Python"
    print(f"'{word}' — палиндром? {facade.check_palindrome(word)}")  # False

    # Тест 3: Многословное выражение-палиндром
    phrase = "A man a plan a canal Panama"
    print(f"'{phrase}' — палиндром? {facade.check_palindrome(phrase)}")  # True

    # Тест 4: Многословное выражение не палиндром
    phrase = "Hello World"
    print(f"'{phrase}' — палиндром? {facade.check_palindrome(phrase)}")  # False

    # Тест 5: Одно слово с разными регистрами
    word = "Deified"
    print(f"'{word}' — палиндром? {facade.check_palindrome(word)}")  # True

    # Тест 6: Сложная фраза с пробелами
    phrase = "Was it a car or a cat I saw"
    print(f"'{phrase}' — палиндром? {facade.check_palindrome(phrase)}")  # True
