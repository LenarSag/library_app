from datetime import datetime
import json
import os
from uuid import UUID, uuid4

from library_manager.book_model import Book


class Library:
    """Клас управления библиотекой."""

    def __init__(self, storage_file: str = 'storage/library.json') -> None:
        self.books: dict[UUID, Book] = {}
        self.storage_file: str = storage_file
        self.create_storage_directory()  # Ensure the directory exists
        self.load_books()

    def create_storage_directory(self) -> None:
        """Создает директорию для хранения книг если не создана."""
        storage_dir = os.path.dirname(self.storage_file)
        if storage_dir and not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def validate_book(self, title: str, author: str, year: int) -> None:
        """Проверяет данные книги до добавления в библиотеку."""
        if not title:
            raise ValueError('Название книги не может быть пустым')
        if not author:
            raise ValueError('Имя автора не может быть пустым')
        if year < 0 or year > datetime.now().year:
            raise ValueError('Некорректный год издания')

    def load_books(self):
        """Загружает книги из файла в словарь."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.books = {
                    UUID(book_data['id']): Book.from_dict(book_data)
                    for book_data in data
                }

    def save_books(self) -> None:
        """Сохраненяет книги в файл."""
        with open(self.storage_file, 'w', encoding='utf-8') as file:
            json.dump(
                [book.to_dict() for book in self.books.values()],
                file,
                ensure_ascii=False,
                indent=4,
            )

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавляет книгу в библиотеку."""
        book_id = uuid4()
        new_book = Book(book_id, title, author, year)
        self.books[book_id] = new_book
        self.save_books()
        print(f"Книга '{title}' успешно добавлена с ID {book_id}.")

    def update_status(self, book_id: UUID, new_status: str) -> None:
        """Обновляет статус книги."""
        book = self.books.get(book_id)
        if book:
            book.status = new_status
            self.save_books()
            print(f'Статус книги {book.id} обновлён!')
        else:
            print(f'Книга с id {book_id} не найдена.')

    def remove_book(self, book_id: UUID) -> None:
        """Удаляет книгу из библиотеки."""
        book = self.books.get(book_id)
        if book:
            del self.books[book_id]
            self.save_books()
            print(f'Книга с id {book_id} успешно удалена.')
        else:
            print(f'Книга с id {book_id} не найдена.')

    def get_all_books(self) -> None:
        if not self.books:
            print('Библиотека пуста.')
        for book in self.books.values():
            print(book)
            print()

    def search_book(self) -> None:
        pass
