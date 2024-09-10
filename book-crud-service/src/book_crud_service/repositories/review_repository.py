from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from book_crud_service.models.sqlalchemy.review import Review
from book_crud_service.repositories.base import BaseRepository


class ReviewRepository(BaseRepository[Review]):
    """
    Repository class for managing review-related database operations.

    This class extends the generic `BaseRepository` and is specific to the `Review` model. It provides
    CRUD functionality and additional methods tailored for handling reviews.

    Attributes:
    - session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.

    Methods:
    - Inherits all CRUD methods from `BaseRepository`, including:
      - get(id): Fetch a review by its ID.
      - get_all(): Fetch all reviews.
      - create(obj_in): Add a new review to the database.
      - update(id, obj_in): Update an existing review's details.
      - patch(id, obj_in): Partially update an existing review's details.
      - delete(id): Delete a review by its ID.
    - get_all(book_id): Fetch all reviews for a specific book by filtering on the book_id.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the ReviewRepository with the session and bind it to the Review model.

        :param session: The asynchronous session used to interact with the database.
        """
        super().__init__(Review, session)

    async def get_all(self, book_id: int) -> List[Review]:
        """
        Fetch all reviews for a specific book by filtering on the book_id.

        :param book_id: The ID of the book whose reviews are to be fetched.
        :return: A list of `Review` objects associated with the given book.
        """
        result = await self.session.execute(
            select(self.model).where(self.model.book_id == book_id)
        )
        return result.scalars().all()
