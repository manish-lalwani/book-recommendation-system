from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from book_crud_service.rest.api.common_error import common_error_responses
from book_crud_service.service.book_service import BookService
from book_crud_service.models.pydantic_.book import (
    BookResponseModel,
    BookCreateModel,
    BookUpdateModel,
    BookPatchModel,
)
from book_crud_service.db import get_db

# Create a FastAPI router
router = APIRouter()


# Create a new book
@router.post(
    "/books",
    response_model=BookResponseModel,
    status_code=201,
    response_model_exclude_none=True,
    responses=common_error_responses(),
)
async def create_book(book: BookCreateModel, session: AsyncSession = Depends(get_db)):
    """
    API endpoint to create a new book.

    This endpoint accepts a Pydantic model `BookCreateModel` which contains details for creating
    a new book, such as title, author, genre, year published, and summary. The book data is then passed
    to the `BookService` for processing and storage.

    :param book: Pydantic model (BookCreateModel) containing book details.
    :param session: Database session, automatically injected via FastAPI's dependency injection.
    :return: The created book data.
    """
    book_service = BookService(session)
    # Pass the Pydantic model directly to the service layer
    created_book = await book_service.create_book(book)
    return created_book


# Get all books
@router.get(
    "/books", response_model=List[BookResponseModel], response_model_exclude_none=True
)
async def get_all_books(session: AsyncSession = Depends(get_db)):
    """
    API endpoint to retrieve all books.

    This endpoint returns a list of all books stored in the database. The data is fetched
    using the `BookService`.

    :param session: Database session.
    :return: A list of all book records.
    """
    book_service = BookService(session)
    books = await book_service.get_all_books()
    return books


# Get a book by ID
@router.get(
    "/books/{id}", response_model=BookResponseModel, response_model_exclude_none=True
)
async def get_book_by_id(id: int, session: AsyncSession = Depends(get_db)):
    """
    API endpoint to retrieve a book by its ID.

    This endpoint retrieves a specific book from the database based on its unique ID. If the book
    is not found, a 404 error is raised.

    :param id: The unique ID of the book to retrieve.
    :param session: Database session.
    :return: The book record if found, otherwise 404 error.
    """
    book_service = BookService(session)
    book = await book_service.get_book_by_id(id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# Full update of a book via PUT
@router.put(
    "/books/{id}", response_model=BookResponseModel, response_model_exclude_none=True
)
async def update_book(
    id: int, book_data: BookUpdateModel, session: AsyncSession = Depends(get_db)
):
    """
    API endpoint to fully update a book.

    This endpoint performs a full update on a book record, meaning all fields of the book will be replaced
    with the new data provided in the `BookUpdateModel`. If the book is not found, a 404 error is raised.

    :param id: The unique ID of the book to update.
    :param book_data: Pydantic model (BookUpdateModel) containing updated book details.
    :param session: Database session.
    :return: The updated book record, or a 404 error if the book is not found.
    """
    book_service = BookService(session)
    updated_book = await book_service.update_book(id, book_data)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


# Partial update of a book via PATCH
@router.patch(
    "/books/{id}", response_model=BookResponseModel, response_model_exclude_none=True
)
async def patch_book(
    id: int, book_data: BookPatchModel, session: AsyncSession = Depends(get_db)
):
    """
    API endpoint to partially update a book.

    This endpoint allows for a partial update of a book's fields. Only the provided fields in the
    `BookPatchModel` will be updated. If the book is not found, a 404 error is raised.

    :param id: The unique ID of the book to patch.
    :param book_data: Pydantic model (BookPatchModel) containing fields to be updated.
    :param session: Database session.
    :return: The updated book record, or a 404 error if the book is not found.
    """
    book_service = BookService(session)
    updated_book = await book_service.patch_book(id, book_data)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


# Delete a book by ID
@router.delete("/books/{id}", status_code=204, response_model_exclude_none=True)
async def delete_book(id: int, session: AsyncSession = Depends(get_db)):
    """
    API endpoint to delete a book by its ID.

    This endpoint deletes a specific book from the database based on its unique ID. If the book is not found,
    the deletion will still return a 204 status (no content).

    :param id: The unique ID of the book to delete.
    :param session: Database session.
    :return: None
    """
    book_service = BookService(session)
    await book_service.delete_book(id)
    return
