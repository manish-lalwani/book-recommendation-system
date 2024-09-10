from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from book_crud_service.repositories.book_repository import BookRepository
from book_crud_service.models.sqlalchemy.book import Book
from book_crud_service.models.pydantic_.book import (
    BookCreateModel,
    BookUpdateModel,
    BookPatchModel,
)


class BookService:
    """
    Service class to handle business logic related to book operations.

    This class acts as an intermediary between the repository layer and the API layer,
    handling the creation, retrieval, updating, and deletion of book records.

    Attributes:
    - book_repo (BookRepository): An instance of `BookRepository` for interacting with the database.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the BookService with a session and create an instance of `BookRepository`.

        :param session: The asynchronous session used to interact with the database.
        """
        self.book_repo = BookRepository(session)

    async def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Fetch a single book by its ID from the repository.

        This method interacts with the `BookRepository` to retrieve a book based on its unique ID.

        :param book_id: The ID of the book to retrieve.
        :return: The book record if found, otherwise None.
        """
        return await self.book_repo.get(book_id)

    async def get_all_books(self) -> List[Book]:
        """
        Fetch all books from the repository.

        This method retrieves all the books from the database using the `BookRepository`.

        :return: A list of all book records.
        """
        return await self.book_repo.get_all()

    async def create_book(self, book_data: BookCreateModel) -> Book:
        """
        Create a new book in the repository.

        This method converts the Pydantic `BookCreateModel` into a SQLAlchemy `Book` object
        and saves it to the database.

        :param book_data: The Pydantic model (BookCreateModel) containing the book data.
        :return: The newly created book record.
        """
        # Convert the Pydantic model to a SQLAlchemy Book object
        new_book = Book(
            **book_data.model_dump()
        )  # Convert Pydantic model to SQLAlchemy model
        created_book = await self.book_repo.create(new_book)  # Save to DB
        return created_book

    async def update_book(
        self, book_id: int, book_data: BookUpdateModel
    ) -> Optional[Book]:
        """
        Update an existing book in the repository.

        This method performs a full update of a book's data, replacing all fields with the data
        provided in the `BookUpdateModel`.

        :param book_id: The ID of the book to update.
        :param book_data: The Pydantic model (BookUpdateModel) containing the updated data.
        :return: The updated book record if successful, otherwise None.
        """
        updated_book = await self.book_repo.update(
            book_id, book_data.model_dump(exclude_unset=True)
        )  # Convert Pydantic model to dict
        return updated_book

    async def patch_book(
        self, book_id: int, book_data: BookPatchModel
    ) -> Optional[Book]:
        """
        Partially update an existing book in the repository.

        This method updates only the provided fields of a book using the `BookPatchModel`.

        :param book_id: The ID of the book to patch.
        :param book_data: The Pydantic model (BookPatchModel) containing the fields to be updated.
        :return: The patched book record if successful, otherwise None.
        """
        patched_book = await self.book_repo.patch(
            book_id, book_data.model_dump(exclude_unset=True)
        )  # Exclude unset fields
        return patched_book

    async def delete_book(self, book_id: int) -> None:
        """
        Delete a book by its ID from the repository.

        This method removes a specific book from the database using its unique ID.

        :param book_id: The ID of the book to delete.
        :return: None
        """
        await self.book_repo.delete(book_id)
