from datetime import datetime
import json
import os
from typing import Optional
from uuid import UUID, uuid4

from config import WORKING_FILE_FOLDER
from exceptions.exceptions import BookNotFoundError
from library_manager.book_model import Book


class Library:
    """Клас управления библиотекой."""

    def __init__(self, storage_file: str = WORKING_FILE_FOLDER) -> None:
        self.books: dict[UUID, Book] = {}
        self.storage_file: str = storage_file
        self.create_storage_directory()
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

    def load_books(self) -> None:
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

    def get_book_by_id(self, book_id: UUID) -> Book:
        """Поиск книги по id."""
        book = self.books.get(book_id)
        if book:
            return book
        raise BookNotFoundError(f'Книга с id {book_id} не найдена.')

    def add_book(self, title: str, author: str, year: int) -> UUID:
        """Добавляет книгу в библиотеку."""
        book_id = uuid4()
        new_book = Book(book_id, title, author, year)
        self.books[book_id] = new_book
        self.save_books()
        return book_id

    def remove_book(self, book_id: UUID) -> None:
        """Удаляет книгу из библиотеки."""
        del self.books[book_id]
        self.save_books()

    def search_book(self, **kwargs) -> Optional[list]:
        """Ищет книгу по задданым атрибутам."""
        results = []
        for book in self.books.values():
            match = all(
                getattr(book, key, None) == value
                for key, value in kwargs.items()
                if value is not None
            )
            if match:
                results.append(book)
        return results if results else None

    def get_all_books(self) -> dict[UUID, Book]:
        """Возвращает словарь со всеми книгами."""
        return self.books

    def update_status(self, book: Book, new_status: str) -> None:
        """Обновляет статус книги."""
        book.status = new_status
        self.save_books()
