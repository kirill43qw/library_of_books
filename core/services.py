import json
from dataclasses import dataclass, field

from core.book_model import Book


@dataclass
class Storage:
    db_path: str

    def load_books(self) -> list[Book]:
        """Загружает список книг из файла."""
        try:
            with open(self.db_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_books(self, books: list[Book]) -> None:
        """Сохраняет список книг в файл."""
        with open(self.db_path, "w", encoding="utf-8") as file:
            json.dump(
                [book.to_dict() for book in books], file, ensure_ascii=False, indent=4
            )


@dataclass
class Library:
    db_path: str
    db: Storage = field(init=False)
    books: list[Book] = field(init=False)

    def __post_init__(self):
        self.storage = Storage(self.db_path)
        self.books = self.storage.load_books()

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Добавляет новую книгу в библиотеку."""
        if any(
            book.title == title and book.author == author and book.year == year
            for book in self.books
        ):
            raise ValueError("Такая книга уже существует в библиотеке.")
        book_id = max([book.book_id for book in self.books], default=0) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.storage.save_books(self.books)
        return new_book

    def remove_book(self, book_id: int) -> bool:
        """Удаляет книгу по ID."""
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.storage.save_books(self.books)
            return True
        return False

    def find_book_by_id(self, book_id: int) -> Book | None:
        """Ищет книгу по ID."""
        return next((book for book in self.books if book.book_id == book_id), None)

    def search_books(self, query: str) -> list[Book]:
        """Ищет книги по нескольким полям: title, author, year."""
        query_lower = query.lower().strip()
        return [
            book
            for book in self.books
            if query_lower in book.title.lower()
            or query_lower in book.author.lower()
            or query_lower in str(book.year)
        ]

    def update_book_status(self, book_id: int, status: bool) -> bool:
        """Обновляет статус книги."""
        book = self.find_book_by_id(book_id)
        if book:
            book.status = status
            self.storage.save_books(self.books)
            return True
        return False

    def list_books(self) -> None:
        """Выводит список всех книг в табличном формате."""
        if not self.books:
            print("В библиотеке нет книг.")
            return

        print(f"{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<6} {'Статус':<10}")
        print("-" * 75)
        for book in self.books:
            print(
                f"{book.book_id:<5} {book.title:<30} {book.author:<20} "
                f"{book.year:<6} {'в наличии' if book.status else 'выдана':<10}"
            )
