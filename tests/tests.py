import unittest
import os
from core.services import Library, Storage
from core.book_model import Book


class TestBook(unittest.TestCase):
    def test_to_dict(self):
        book = Book(1, "1984", "Джорож Оруэлл", 1949, True)
        expected = {
            "id": 1,
            "title": "1984",
            "author": "Джорож Оруэлл",
            "year": 1949,
            "status": "в наличии",
        }
        self.assertEqual(book.to_dict(), expected)

    def test_from_dict(self):
        data = {
            "id": 1,
            "title": "1984",
            "author": "Джорож Оруэлл",
            "year": 1949,
            "status": "в наличии",
        }
        book = Book.from_dict(data)
        self.assertEqual(book.book_id, 1)
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "Джорож Оруэлл")
        self.assertEqual(book.year, 1949)
        self.assertTrue(book.status)


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.test_path = "test_books.json"
        self.storage = Storage(self.test_path)

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_save_and_load_books(self):
        books = [
            Book(1, "1984", "Джорож Оруэлл", 1949, True),
            Book(2, "Шантарам", "Грегори Дэвид Робертс", 2003, False),
        ]
        self.storage.save_books(books)
        loaded_books = self.storage.load_books()
        self.assertEqual(len(loaded_books), 2)
        self.assertEqual(loaded_books[0].title, "1984")
        self.assertFalse(loaded_books[1].status)


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.test_path = "test_books.json"
        self.library = Library(self.test_path)

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_add_book(self):
        book = self.library.add_book("1984", "Джорож Оруэлл", 1949)
        self.assertIsNotNone(book)
        self.assertEqual(book.title, "1984")
        self.assertEqual(len(self.library.books), 1)

    def test_add_duplicate_book(self):
        self.library.add_book("1984", "Джорож Оруэлл", 1949)
        with self.assertRaises(ValueError):
            self.library.add_book("1984", "Джорож Оруэлл", 1949)

    def test_remove_book(self):
        book = self.library.add_book("1984", "Джорож Оруэлл", 1949)
        self.assertTrue(self.library.remove_book(book.book_id))
        self.assertFalse(self.library.remove_book(999))
        self.assertEqual(len(self.library.books), 0)

    def test_find_book_by_id(self):
        book = self.library.add_book("1984", "Джорож Оруэлл", 1949)
        found = self.library.find_book_by_id(book.book_id)
        self.assertIsNotNone(found)
        self.assertEqual(found.title, "1984")
        self.assertIsNone(self.library.find_book_by_id(999))

    def test_search_books(self):
        self.library.add_book("1984", "Джорож Оруэлл", 1949)
        self.library.add_book("Шантарам", "Грегори Дэвид Робертс", 2003)
        results = self.library.search_books("1949")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Джорож Оруэлл")

        results = self.library.search_books("Робертс")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Шантарам")

    def test_update_book_status(self):
        book = self.library.add_book("1984", "Джорож Оруэлл", 1949)
        self.assertTrue(self.library.update_book_status(book.book_id, False))
        self.assertFalse(book.status)
        self.assertFalse(self.library.update_book_status(999, True))

    def test_list_books(self):
        self.library.add_book("1984", "Джорож Оруэлл", 1949)
        self.library.add_book("Шантарам", "Грегори Дэвид Робертс", 2003)
        self.library.list_books()


if __name__ == "__main__":
    unittest.main()
