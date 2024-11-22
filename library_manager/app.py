from uuid import UUID

from exceptions.exceptions import BookNotFoundError
from library_manager.library import Library

from config import BOOK_STATUS
from config import STARS


def print_with_stars(text: str) -> None:
    print(STARS)
    print(text)
    print(STARS)


class LibraryApp:
    """Класс консольного приложения."""

    def __init__(self) -> None:
        self.library = Library()

    def start(self) -> None:
        """Запуск консольного приложения."""
        print('Приветствую в приложении Библиотека!')
        print()

        while True:
            print('Что вы хотите сделать? Введите одну из команд:')
            print('1: добавить книгу')
            print('2: удалить книгу')
            print('3: поиск книги')
            print('4: отображение всех книг')
            print('5: изменение статуса книги')
            print('0: выход (или нажмите CTRL + C)\n')

            command = input('Введите команду:')

            if command == '1':
                try:
                    title = input('Введите название книги:').strip()
                    author = input('Введите автора книги:').strip()
                    year = int(input('Введите год издания:').strip())
                    self.library.validate_book(title, author, year)
                    book_id = self.library.add_book(title, author, year)

                    print_with_stars(
                        f"Книга '{title}' успешно добавлена с ID {book_id}."
                    )

                except ValueError as e:
                    print_with_stars(f'Ошибка: {e}')

            elif command == '2':
                try:
                    book_id = UUID(input('Введите id книги: ').strip())
                    self.library.get_book_by_id(book_id)
                    self.library.remove_book(book_id)
                    print_with_stars(f'Книга с id {book_id} удалена')

                except ValueError:
                    print_with_stars('Введите корректный id')
                except BookNotFoundError as e:
                    print_with_stars(f'Ошибка: {e}')

            elif command == '3':
                try:
                    print(
                        'Введите критерии поиска (оставьте пустым, чтобы пропустить):'
                    )
                    title = input('Введите название книги:').strip() or None
                    author = input('Введите автора книги:').strip() or None
                    year_input = input('Введите год издания:').strip()
                    year = int(year_input) if year_input else None
                    results = self.library.search_book(
                        title=title, author=author, year=year
                    )
                    if results:
                        for result in results:
                            print_with_stars(result)
                    else:
                        print_with_stars('Книга с такими данными не найдена.')

                except ValueError:
                    print('Введите корректный год издания')

            elif command == '4':
                books = self.library.get_all_books()
                if books:
                    print('На данный момент в библиотеке следующие книги:')
                    for book in books.values():
                        print_with_stars(book)
                else:
                    print_with_stars('Библиотека пуста.')

            elif command == '5':
                try:
                    book_id = UUID(input('Введите id книги:').strip())
                    book = self.library.get_book_by_id(book_id)
                    print(f'Текущий статус книги "{book.status}"')

                    print('Выберите статус книги:')
                    for num, status in BOOK_STATUS.items():
                        print(f'{num}. {status}')

                    status_key = int(input('Введите номер статуса:').strip())
                    if status_key not in BOOK_STATUS:
                        raise ValueError('Неверный выбор статуса.')

                    new_status = BOOK_STATUS.get(status_key)
                    self.library.update_status(book, new_status)
                    print_with_stars(f'Статус книги с id {book_id} обновлен.')

                except ValueError as e:
                    print_with_stars(f'Ошибка: {e}')
                except BookNotFoundError as e:
                    print_with_stars(f'Ошибка: {e}')

            elif command == '0':
                print('Выход из приложения.')
                break

            else:
                print_with_stars('Некорректная команда. Попробуйте снова.')
