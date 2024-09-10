from sqlalchemy.ext.asyncio import AsyncSession
from book_crud_service.models.sqlalchemy.book import Book
from book_crud_service.repositories.base import BaseRepository


class BookRepository(BaseRepository[Book]):
    """
    Repository class for managing book-related database operations.

    This class extends the generic `BaseRepository` and is specific to the `Book` model. It provides
    the same CRUD functionality as `BaseRepository` but is tailored to handle books.

    Attributes:
    - session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.

    Methods:
    - Inherits all CRUD methods from `BaseRepository`, including:
      - get(id): Fetch a book by its ID.
      - get_all(): Fetch all books.
      - create(obj_in): Add a new book to the database.
      - update(id, obj_in): Update an existing book's details.
      - patch(id, obj_in): Partially update an existing book's details.
      - delete(id): Delete a book by its ID.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the BookRepository with the session and bind it to the Book model.

        :param session: The asynchronous session used to interact with the database.
        """
        super().__init__(Book, session)
