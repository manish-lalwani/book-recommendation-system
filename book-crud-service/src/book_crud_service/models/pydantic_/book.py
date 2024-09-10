from typing import Optional
from pydantic import ConfigDict
from book_crud_service.models.pydantic_.base import (
    AuditResponseModel,
    AuditUpdateModel,
    AuditCreateModel,
)


# Model for Output (response)
class BookResponseModel(AuditResponseModel):
    """
    Pydantic model for the response containing book data.

    This model is used when returning book data to the client. It includes audit-related fields
    (created_by, created_on, etc.) from the `AuditResponseModel`.

    Attributes:
    - id (int): The unique identifier for the book.
    - title (str): The title of the book.
    - author (str): The author of the book.
    - genre (Optional[str]): The genre of the book (optional).
    - year_published (Optional[int]): The year the book was published (optional).
    - summary (Optional[str]): A brief summary of the book (optional).

    Example:
    {
        "created_by": "admin",
        "created_on": "2024-09-07T12:31:37.056382Z",
        "id": 1,
        "title": "The Great Adventure",
        "author": "John Doe",
        "genre": "Fiction",
        "year_published": 2020,
        "summary": "An epic journey of self-discovery and adventure."
    }
    """

    id: int
    title: str
    author: str
    genre: Optional[str] = None
    year_published: Optional[int] = None
    summary: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "created_by": "admin",
                "created_on": "2024-09-07T12:31:37.056382Z",
                "id": 1,
                "title": "The Great Adventure",
                "author": "John Doe",
                "genre": "Fiction",
                "year_published": 2020,
                "summary": "An epic journey of self-discovery and adventure.",
            }
        }
    )


# Model for Input (create)
class BookCreateModel(AuditCreateModel):
    """
    Pydantic model for creating a new book.

    This model is used for input when creating a new book. It extends the `AuditCreateModel`,
    which handles audit fields (created_by, etc.).

    Attributes:
    - title (str): The title of the book.
    - author (str): The author of the book.
    - genre (Optional[str]): The genre of the book (optional).
    - year_published (Optional[int]): The year the book was published (optional).
    - summary (Optional[str]): A brief summary of the book (optional).

    Example:
    {
        "title": "The Great Adventure",
        "author": "John Doe",
        "genre": "Fiction",
        "year_published": 2020,
        "summary": "An epic journey of self-discovery and adventure.",
        "created_by": "admin"
    }
    """

    title: str
    author: str
    genre: Optional[str] = None
    year_published: Optional[int] = None
    summary: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "The Great Adventure",
                "author": "John Doe",
                "genre": "Fiction",
                "year_published": 2020,
                "summary": "An epic journey of self-discovery and adventure.",
                "created_by": "admin",
            }
        }
    )


# Model for Input (full update via PUT)
class BookUpdateModel(AuditUpdateModel):
    """
    Pydantic model for updating a book via a full PUT request.

    This model is used for input when updating all the fields of an existing book. It extends
    the `AuditUpdateModel`, which handles audit fields (last_modified_by, etc.).

    Attributes:
    - title (str): The title of the book.
    - author (str): The author of the book.
    - genre (Optional[str]): The genre of the book (optional).
    - year_published (Optional[int]): The year the book was published (optional).
    - summary (Optional[str]): A brief summary of the book (optional).

    Example:
    {
        "title": "The Great Adventure: Updated Edition",
        "author": "John Doe",
        "genre": "Adventure",
        "year_published": 2021,
        "summary": "An updated edition of the epic journey of self-discovery.",
        "last_modified_by": "admin"
    }
    """

    title: str
    author: str
    genre: Optional[str] = None
    year_published: Optional[int] = None
    summary: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "The Great Adventure: Updated Edition",
                "author": "John Doe",
                "genre": "Adventure",
                "year_published": 2021,
                "summary": "An updated edition of the epic journey of self-discovery.",
                "last_modified_by": "admin",
            }
        }
    )


# Model for Input (partial update via PATCH)
class BookPatchModel(AuditUpdateModel):
    """
    Pydantic model for partially updating a book via a PATCH request.

    This model is used for input when updating selected fields of an existing book. It extends
    the `AuditUpdateModel`, which handles audit fields (last_modified_by, etc.).

    Attributes:
    - title (Optional[str]): The title of the book (optional).
    - author (Optional[str]): The author of the book (optional).
    - genre (Optional[str]): The genre of the book (optional).
    - year_published (Optional[int]): The year the book was published (optional).
    - summary (Optional[str]): A brief summary of the book (optional).

    Example:
    {
        "year_published": 2021,
        "last_modified_by": "admin"
    }
    """

    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_published: Optional[int] = None
    summary: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"year_published": 2021, "last_modified_by": "admin"}
        }
    )
