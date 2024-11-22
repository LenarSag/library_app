from uuid import UUID


class Book:
    """Класс представляющий модель книга."""

    def __init__(
        self,
        book_id: UUID,
        title: str,
        author: str,
        year: int,
        status: str = 'в наличии',
    ) -> None:
        self.id: UUID = book_id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status,
        }

    @staticmethod
    def from_dict(data):
        return Book(
            book_id=data['id'],
            title=data['title'],
            author=data['author'],
            year=data['year'],
            status=data['status'],
        )

    def __str__(self) -> str:
        return (
            f'id: {self.id}\n'
            f'название: {self.title}\n'
            f'автор: {self.author}\n'
            f'год: {self.year}\n'
            f'статус: {self.status}'
        )
