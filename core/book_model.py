from dataclasses import dataclass


@dataclass
class Book:
    book_id: int
    title: str
    author: str
    year: int
    status: bool = True  # True = "в наличии", False = "выдана"

    def to_dict(self) -> dict:
        """Возвращает словарь для сохранения в JSON."""
        return {
            "id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": "в наличии" if self.status else "выдана",
        }

    @staticmethod
    def from_dict(book_data: dict) -> "Book":
        """Создает объект книги из словаря."""
        return Book(
            book_data["id"],
            book_data["title"],
            book_data["author"],
            book_data["year"],
            book_data["status"] == "в наличии",
        )
