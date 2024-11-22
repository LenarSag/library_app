import unittest
from unittest.mock import patch, MagicMock
from uuid import UUID


from config import STARS
from exceptions.exceptions import BookNotFoundError
from library_manager.app import LibraryApp


class TestLibraryApp(unittest.TestCase):
    def setUp(self):
        self.app = LibraryApp()
        self.app.library = MagicMock()

    @patch(
        'builtins.input',
        side_effect=['1', 'Book', 'Author', '2000', '0'],
    )
    @patch('builtins.print')
    def test_add_book_success(self, mock_print, mock_input):
        """Тестирование добавления книги."""

        fake_id = '123e4567-e89b-12d3-a456-426614174000'
        self.app.library.add_book.return_value = UUID(fake_id)
        self.app.library.validate_book.return_value = None

        self.app.start()

        self.app.library.validate_book.assert_called_once_with('Book', 'Author', 2000)
        self.app.library.add_book.assert_called_once_with('Book', 'Author', 2000)
        mock_print.assert_any_call(STARS)
        mock_print.assert_any_call(f"Книга 'Book' успешно добавлена с ID {fake_id}.")
        mock_print.assert_any_call(STARS)

    @patch('builtins.input', side_effect=['1', '', 'Author', '2000', '0'])
    @patch('builtins.print')
    def test_add_book_invalid_title(self, mock_print, mock_input):
        """Тестирование добавления книги без названия."""

        self.app.library.validate_book.side_effect = ValueError(
            'Название книги не может быть пустым'
        )

        self.app.start()

        self.app.library.validate_book.assert_called_once_with('', 'Author', 2000)
        self.app.library.add_book.assert_not_called()
        mock_print.assert_any_call(STARS)
        mock_print.assert_any_call('Ошибка: Название книги не может быть пустым')
        mock_print.assert_any_call(STARS)

    @patch(
        'builtins.input',
        side_effect=['1', 'Book', 'Author', 'invalid-year', '0'],
    )
    @patch('builtins.print')
    def test_add_book_invalid_year(self, mock_print, mock_input):
        """Тестирование добавления книги с неправильным годом."""

        self.app.start()

        self.app.library.validate_book.assert_not_called()
        self.app.library.add_book.assert_not_called()
        mock_print.assert_any_call(STARS)
        mock_print.assert_any_call(
            "Ошибка: invalid literal for int() with base 10: 'invalid-year'"
        )
        mock_print.assert_any_call(STARS)

    @patch(
        'builtins.input', side_effect=['2', '123e4567-e89b-12d3-a456-426614174000', '0']
    )
    @patch('builtins.print')
    def test_remove_book_success(self, mock_print, mock_input):
        """Тестирование на удаление книги."""

        self.app.library.get_book_by_id.return_value = MagicMock()
        self.app.library.remove_book.return_value = True

        self.app.start()

        self.app.library.get_book_by_id.assert_called_once_with(
            UUID('123e4567-e89b-12d3-a456-426614174000')
        )
        self.app.library.remove_book.assert_called_once_with(
            UUID('123e4567-e89b-12d3-a456-426614174000')
        )
        mock_print.assert_any_call(STARS)
        mock_print.assert_any_call(
            'Книга с id 123e4567-e89b-12d3-a456-426614174000 удалена'
        )
        mock_print.assert_any_call(STARS)

    @patch('builtins.input', side_effect=['2', 'invalid-uuid', '0'])
    @patch('builtins.print')
    def test_remove_book_invalid_id(self, mock_print, mock_input):
        """Тестирование на удаление книги с некорректным uuid."""

        self.app.start()

        self.app.library.get_book_by_id.assert_not_called()
        self.app.library.remove_book.assert_not_called()
        mock_print.assert_any_call(STARS)
        mock_print.assert_any_call('Введите корректный id')
        mock_print.assert_any_call(STARS)

    @patch(
        'builtins.input', side_effect=['2', '123e4567-e89b-12d3-a456-426614174001', '0']
    )
    @patch('builtins.print')
    def test_remove_book_not_found(self, mock_print, mock_input):
        """Тестирование на удаление несуществующей книги."""

        self.app.library.get_book_by_id.side_effect = BookNotFoundError(
            'Книга не найдена.'
        )

        self.app.start()

        self.app.library.get_book_by_id.assert_called_once_with(
            UUID('123e4567-e89b-12d3-a456-426614174001')
        )
        self.app.library.remove_book.assert_not_called()
        mock_print.assert_any_call(STARS)
        mock_print.assert_any_call('Ошибка: Книга не найдена.')
        mock_print.assert_any_call(STARS)
