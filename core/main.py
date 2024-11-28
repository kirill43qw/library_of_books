from core.services import Library


def main():
    library = Library("books.json")

    while True:
        print("\nДоступные команды:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("0. Выйти")

        command = input("Введите номер команды: ")

        if command == "1":
            title = input("Введите название: ")
            author = input("Введите автора: ")
            try:
                year = int(input("Введите год издания: "))
            except ValueError:
                print("Ошибка: год издания должен быть числом.")
                continue
            try:
                book = library.add_book(title, author, year)
                print(f"Книга добавлена: {book.to_dict()}")
            except ValueError as e:
                print(e)

        elif command == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            if library.remove_book(book_id):
                print("Книга удалена.")
            else:
                print("Книга не найдена.")

        elif command == "3":
            query = input("Введите значение для поиска: ")
            results = library.search_books(query)
            if results:
                print(f"Найдено книг: {len(results)}")
                for book in results:
                    print(book.to_dict())
            else:
                print("Книги по вашему запросу не найдены.")

        elif command == "4":
            library.list_books()

        elif command == "5":
            book_id = int(input("Введите ID книги: "))
            status_input = input("Введите новый статус [в наличии/выдана]: ")
            status = status_input == "в наличии"
            if library.update_book_status(book_id, status):
                print("Статус обновлен.")
            else:
                print("Ошибка обновления статуса.")

        elif command == "0":
            break
        else:
            print("Некорректная команда.")


if __name__ == "__main__":
    main()
