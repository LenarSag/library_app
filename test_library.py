import os

import pytest

from config import TEST_FILE_FOLDER
from exceptions.exceptions import BookNotFoundError
from library_manager.library import Library
from library_manager.app import LibraryApp


@pytest.fixture
def default_book():
    return {'title': 'test book', 'author': 'test author', 'year': '2022'}


@pytest.fixture
def default_book_to_delete():
    return {'title': 'delete book', 'author': 'delete author', 'year': '2022'}


@pytest.fixture
def default_book_to_change_status():
    return {'title': 'status book', 'author': 'test author', 'year': '2022'}


@pytest.fixture
def library_app():
    """Фикстура для создания экземпляра LibraryApp с временным файлом для теста."""

    test_file = TEST_FILE_FOLDER
    try:
        library = Library(storage_file=test_file)
        app = LibraryApp()
        app.library = library
        yield app
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_add_book(library_app, default_book):
    """Проверяет создание книги."""

    app = library_app
    book_id = app.library.add_book(**default_book)
    book = app.library.get_book_by_id(book_id)

    assert book.title == default_book['title']
    assert book.author == default_book['author']
    assert book.year == default_book['year']


def test_add_nameless_book(library_app, default_book):
    """Проверяет создание книги без названия."""

    app = library_app
    default_book['title'] = ''

    with pytest.raises(ValueError, match='Название книги не может быть пустым'):
        app.library.validate_book(**default_book)


def test_add_not_coorect_year_book(library_app, default_book):
    """Проверяет создание книги с неправильной датой."""

    app = library_app
    default_book['year'] = -30

    with pytest.raises(ValueError, match='Некорректный год издания'):
        app.library.validate_book(**default_book)


def test_remove_book(library_app, default_book_to_delete):
    """Проверяет удаление книги."""

    app = library_app
    book_id = app.library.add_book(**default_book_to_delete)
    book = app.library.get_book_by_id(book_id)

    assert book.title == default_book_to_delete['title']
    assert book.author == default_book_to_delete['author']
    assert book.year == default_book_to_delete['year']

    app.library.remove_book(book_id)

    with pytest.raises(BookNotFoundError, match=f'Книга с id {book_id} не найдена.'):
        app.library.get_book_by_id(book_id)


def test_search_book(library_app, default_book):
    """Проверяет поиск книги."""

    app = library_app
    search_book_title = 'seach book'
    default_book['title'] = search_book_title
    app.library.add_book(**default_book)
    results = app.library.search_book(title=search_book_title)

    assert len(results) == 1
    assert results[0].title == search_book_title


def test_search_not_existing_book(library_app, default_book):
    """Проверяет поиск несуществующей книги."""

    app = library_app
    search_book_title = 'not existing book'
    app.library.add_book(**default_book)
    results = app.library.search_book(title=search_book_title)

    assert results is None


def test_get_all_books(library_app, default_book, default_book_to_delete):
    """Проверяет список всех книг."""

    app = library_app
    books = app.library.get_all_books()
    assert len(books) == 0

    book1_id = app.library.add_book(**default_book)
    book2_id = app.library.add_book(**default_book_to_delete)
    books = app.library.get_all_books()

    assert book1_id in books
    assert book2_id in books


def test_update_status(library_app, default_book_to_change_status):
    """Проверяет обновление статуса книги."""

    app = library_app
    book_id = app.library.add_book(**default_book_to_change_status)

    new_status = 'выдана'
    book = app.library.get_book_by_id(book_id)
    app.library.update_status(book, new_status)
    updated_book = app.library.get_book_by_id(book_id)

    assert updated_book.title == default_book_to_change_status['title']
    assert updated_book.status == new_status
