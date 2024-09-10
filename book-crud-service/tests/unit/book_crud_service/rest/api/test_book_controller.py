import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from book_crud_service.rest.api.book_controller import router
from book_crud_service.service.book_service import BookService
from book_crud_service.models.pydantic_.book import BookCreateModel, BookUpdateModel, BookPatchModel, BookResponseModel
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from fastapi import FastAPI
from datetime import datetime

# Create a FastAPI app and include the router for testing
app = FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    return TestClient(app)


# Mock the AsyncSession and BookService
@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def mock_book_service(mock_session):
    with patch("book_crud_service.rest.api.book_controller.BookService", autospec=True) as mock:
        yield mock(mock_session)


@pytest.mark.asyncio
async def test_create_book(mock_book_service, client):
    # Prepare data
    book_data = {
        "id": 1,
        "title": "New Book",
        "author": "Author Name",
        "genre": "Fiction",
        "year_published": 2023,
        "created_by": "admin",
        "created_on": datetime.utcnow().isoformat()
    }

    # Mock book creation response
    mock_book_service.create_book.return_value = BookResponseModel(**book_data)

    # Prepare request data without 'id' and 'created_on' (as they are set by the server)
    request_data = {
        "title": "New Book",
        "author": "Author Name",
        "genre": "Fiction",
        "year_published": 2023,
        "created_by": "admin"
    }

    # Perform request
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/books", json=request_data)

    # Assertions
    assert response.status_code == 201
    assert response.json() == book_data
    mock_book_service.create_book.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_books(mock_book_service, client):
    # Mock books list
    mock_books = [
        {"id": 1, "title": "Book 1", "author": "Author 1", "genre": "Fiction", "year_published": 2020, "created_by": "admin", "created_on": datetime.utcnow().isoformat()},
        {"id": 2, "title": "Book 2", "author": "Author 2", "genre": "Non-Fiction", "year_published": 2021, "created_by": "user", "created_on": datetime.utcnow().isoformat()}
    ]
    mock_book_service.get_all_books.return_value = mock_books

    # Perform request
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/books")

    # Assertions
    assert response.status_code == 200
    assert response.json() == mock_books
    mock_book_service.get_all_books.assert_called_once()


@pytest.mark.asyncio
async def test_get_book_by_id(mock_book_service, client):
    # Mock the book retrieval by ID
    book_id = 1
    mock_book = {
        "id": book_id,
        "title": "Book 1",
        "author": "Author 1",
        "genre": "Fiction",
        "year_published": 2020,
        "created_by": "admin",
        "created_on": datetime.utcnow().isoformat()
    }
    mock_book_service.get_book_by_id.return_value = mock_book

    # Perform request
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/books/{book_id}")

    # Assertions
    assert response.status_code == 200
    assert response.json() == mock_book
    mock_book_service.get_book_by_id.assert_called_once_with(book_id)


@pytest.mark.asyncio
async def test_update_book(mock_book_service, client):
    # Mock the full update of a book
    book_id = 1
    update_data = {
        "title": "Updated Book",
        "author": "Updated Author",
        "genre": "Updated Genre",
        "year_published": 2023,
        "last_modified_by": "admin"
    }

    # Prepare a mock response
    mock_updated_book = {
        "id": book_id,
        "title": "Updated Book",
        "author": "Updated Author",
        "genre": "Updated Genre",
        "year_published": 2023,
        "last_modified_by": "admin",
        "created_on": datetime.utcnow().isoformat()
    }
    mock_book_service.update_book.return_value = mock_updated_book

    # Convert update_data to BookUpdateModel for comparison
    expected_call_data = BookUpdateModel(**update_data)

    # Perform request
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/books/{book_id}", json=update_data)

    # Assertions
    assert response.status_code == 200
    assert response.json() == mock_updated_book
    mock_book_service.update_book.assert_called_once_with(book_id, expected_call_data)

@pytest.mark.asyncio
async def test_patch_book(mock_book_service, client):
    # Mock the partial update of a book
    book_id = 1
    patch_data = {
        "title": "Partially Updated Book",
        "last_modified_by": "admin"  # Ensure last_modified_by is included
    }

    # Mock response after patch
    mock_updated_book = {
        "id": book_id,
        "title": "Partially Updated Book",
        "author": "Author 1",          # Ensure all fields exist for validation
        "genre": "Fiction",
        "year_published": 2020,
        "created_by": "admin",
        "created_on": datetime.utcnow().isoformat(),
        "last_modified_by": "admin"
    }

    # Return mock object for the patch method
    mock_book_service.patch_book.return_value = mock_updated_book

    # Perform the request
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.patch(f"/books/{book_id}", json=patch_data)

    # Assertions
    assert response.status_code == 200
    assert response.json() == mock_updated_book
    mock_book_service.patch_book.assert_called_once_with(book_id, BookPatchModel(**patch_data))



@pytest.mark.asyncio
async def test_delete_book(mock_book_service, client):
    # Mock book deletion
    book_id = 1
    mock_book_service.delete_book.return_value = None

    # Perform request
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/books/{book_id}")

    # Assertions
    assert response.status_code == 204
    mock_book_service.delete_book.assert_called_once_with(book_id)
