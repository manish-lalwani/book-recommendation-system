from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from book_crud_service.db import get_db
from book_crud_service.service.review_service import ReviewService
from book_crud_service.models.pydantic_.review import (
    ReviewCreateModel,
    ReviewUpdateModel,
    ReviewResponseModel,
)
from book_crud_service.rest.api.common_error import common_error_responses

router = APIRouter()


# Create a new review
@router.post(
    "/books/{book_id}/reviews",
    response_model=ReviewResponseModel,
    status_code=201,
    responses=common_error_responses(),
)
async def create_review(
    book_id: int, review: ReviewCreateModel, session: AsyncSession = Depends(get_db)
):
    """
    API endpoint to create a new review for a book.

    This endpoint accepts a Pydantic model `ReviewCreateModel` which contains details for creating
    a new review, such as user ID, review text, and rating. The review is associated with a specific
    book by its ID and is processed by the `ReviewService`.

    :param book_id: The ID of the book for which the review is being created.
    :param review: The Pydantic model (ReviewCreateModel) containing review details.
    :param session: Database session, automatically injected via FastAPI's dependency injection.
    :return: The created review data.
    """
    review_service = ReviewService(session)
    # Pass the Pydantic model and book_id to the service layer
    created_review = await review_service.create_review(book_id, review)
    return created_review


# Get all reviews for a specific book
@router.get(
    "/books/{book_id}/reviews",
    response_model=List[ReviewResponseModel],
    responses=common_error_responses(),
)
async def get_all_reviews(book_id: int, session: AsyncSession = Depends(get_db)):
    """
    API endpoint to retrieve all reviews for a specific book.

    This endpoint fetches all the reviews for a particular book, identified by the book's ID.
    The reviews are processed and retrieved using the `ReviewService`.

    :param book_id: The ID of the book whose reviews are being fetched.
    :param session: Database session.
    :return: A list of reviews for the given book.
    """
    review_service = ReviewService(session)
    reviews = await review_service.get_all_reviews_for_book(book_id)
    return reviews


# Update a review by ID
@router.put(
    "/reviews/{review_id}",
    response_model=ReviewResponseModel,
    responses=common_error_responses(),
)
async def update_review(
    review_id: int,
    review_data: ReviewUpdateModel,
    session: AsyncSession = Depends(get_db),
):
    """
    API endpoint to fully update a review.

    This endpoint updates a specific review based on the provided review ID and new review data.
    The review data is provided as a `ReviewUpdateModel`, which may include updated review text and rating.
    If the review is not found, a 404 error is raised.

    :param review_id: The ID of the review to update.
    :param review_data: The Pydantic model (ReviewUpdateModel) containing the updated review data.
    :param session: Database session.
    :return: The updated review data, or a 404 error if the review is not found.
    """
    review_service = ReviewService(session)
    updated_review = await review_service.update_review(review_id, review_data)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review


# Delete a review by ID
@router.delete(
    "/reviews/{review_id}", status_code=204, responses=common_error_responses()
)
async def delete_review(review_id: int, session: AsyncSession = Depends(get_db)):
    """
    API endpoint to delete a review by its ID.

    This endpoint deletes a specific review from the database based on its unique ID. If the review is not found,
    the deletion will still return a 204 status (no content).

    :param review_id: The ID of the review to delete.
    :param session: Database session.
    :return: None
    """
    review_service = ReviewService(session)
    await review_service.delete_review(review_id)
    return
