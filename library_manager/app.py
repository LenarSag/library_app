from uuid import UUID

from library_manager.library import Library


BOOK_STATUS: dict[int, str] = {1: 'в наличии', 2: 'выдана'}


class LibraryApp:
    """Класс консольного приложения."""

    def __init__(self) -> None:
        self.library = Library()

    def start(self) -> None:
        """Запуск консольного приложения."""
        print('Приветствую в приложении Библиотека!')

        while True:
            print()
            print('Список команд:')
            print('1: добавить книгу')
            print('2: удалить книгу')
            print('3: поиск книги')
            print('4: отображение всех книг')
            print('5: изменение статуса книги')
            print('0: выход (или нажмите CTRL + C)\n')

            command = input('Введите команду:')

            if command == '1':
                title = input('Введите название книги:').strip()
                author = input('Введите автора книги:').strip()
                try:
                    year = int(input('Введите год издания:').strip())
                    self.library.validate_book(title, author, year)
                    self.library.add_book(title, author, year)

                except ValueError as e:
                    print(f'Ошибка: {e}')

            elif command == '2':
                try:
                    book_id = UUID(input('Введите id книги: ').strip())
                    self.library.remove_book(book_id)
                except ValueError:
                    print('Введите корректный id')

            elif command == '3':
                try:
                    print(
                        'Введите критерии поиска (оставьте пустым, чтобы пропустить):'
                    )
                    title = input('Введите название книги:').strip() or None
                    author = input('Введите автора книги:').strip() or None
                    year_input = input('Введите год издания:\n').strip()
                    year = int(year_input) if year_input else None
                    self.library.search_book(title=title, author=author, year=year)

                except ValueError:
                    print('Введите корректный год издания')

            elif command == '4':
                self.library.get_all_books()

            elif command == '5':
                try:
                    book_id = UUID(input('Введите id книги:').strip())
                    print('Выберите статус книги:')
                    for num, status in BOOK_STATUS.items():
                        print(f'{num}. {status}')

                    status_key = int(input('Введите номер статуса:'))
                    if status_key not in BOOK_STATUS:
                        raise ValueError('Неверный выбор статуса.')

                    new_status = BOOK_STATUS.get(status_key)
                    self.library.update_status(book_id, new_status)

                except ValueError as e:
                    print(f'Ошибка: {e}')

            elif command == '0':
                print('Выход из приложения.')
                break

            else:
                print('Некорректная команда. Попробуйте снова.')