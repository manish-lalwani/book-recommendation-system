from typing import List, Optional
from book_crud_service.repositories.review_repository import ReviewRepository
from book_crud_service.models.sqlalchemy.review import Review
from book_crud_service.models.pydantic_.review import (
    ReviewCreateModel,
    ReviewUpdateModel,
)
from sqlalchemy.ext.asyncio import AsyncSession


class ReviewService:
    """
    Service class to handle business logic related to review operations.

    This class acts as an intermediary between the repository layer and the API layer,
    handling the creation, retrieval, updating, and deletion of review records.

    Attributes:
    - review_repo (ReviewRepository): An instance of `ReviewRepository` for interacting with the database.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the ReviewService with a session and create an instance of `ReviewRepository`.

        :param session: The asynchronous session used to interact with the database.
        """
        self.review_repo = ReviewRepository(session)

    async def get_review_by_id(self, review_id: int) -> Optional[Review]:
        """
        Fetch a single review by its ID from the repository.

        This method interacts with the `ReviewRepository` to retrieve a review based on its unique ID.

        :param review_id: The ID of the review to retrieve.
        :return: The review record if found, otherwise None.
        """
        return await self.review_repo.get(review_id)

    async def get_all_reviews_for_book(self, book_id: int) -> List[Review]:
        """
        Fetch all reviews for a specific book from the repository.

        This method retrieves all the reviews associated with a specific book based on its book ID.

        :param book_id: The ID of the book whose reviews are to be retrieved.
        :return: A list of reviews for the specified book.
        """
        return await self.review_repo.get_all(book_id)

    async def create_review(
        self, book_id: int, review_data: ReviewCreateModel
    ) -> Review:
        """
        Create a new review in the repository.

        This method converts the Pydantic `ReviewCreateModel` into a SQLAlchemy `Review` object and
        associates it with the specified book ID before saving it to the database.

        :param book_id: The ID of the book associated with the review.
        :param review_data: The Pydantic model (ReviewCreateModel) containing review data.
        :return: The newly created review record.
        """
        # Convert the Pydantic model to a SQLAlchemy Review object and include book_id
        new_review = Review(**review_data.model_dump(), book_id=book_id)
        return await self.review_repo.create(new_review)

    async def update_review(
        self, review_id: int, review_data: ReviewUpdateModel
    ) -> Optional[Review]:
        """
        Update an existing review in the repository.

        This method performs a full update of a review's data, replacing the relevant fields with the
        data provided in the `ReviewUpdateModel`.

        :param review_id: The ID of the review to update.
        :param review_data: The Pydantic model (ReviewUpdateModel) containing the updated data.
        :return: The updated review record if successful, otherwise None.
        """
        return await self.review_repo.update(
            review_id, review_data.model_dump(exclude_unset=True)
        )

    async def delete_review(self, review_id: int) -> None:
        """
        Delete a review by its ID from the repository.

        This method removes a specific review from the database using its unique ID.

        :param review_id: The ID of the review to delete.
        :return: None
        """
        await self.review_repo.delete(review_id)
