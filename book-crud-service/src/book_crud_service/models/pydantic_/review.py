from typing import Optional
from pydantic import ConfigDict
from book_crud_service.models.pydantic_.base import (
    AuditCreateModel,
    AuditUpdateModel,
    AuditResponseModel,
)


class ReviewCreateModel(AuditCreateModel):
    """
    Pydantic model for creating a new review.

    This model is used for input when creating a review. It extends the `AuditCreateModel`,
    which handles audit fields (created_by, etc.).

    Attributes:
    - user_id (int): The ID of the user submitting the review.
    - review_text (str): The content of the review.
    - rating (int): The rating given to the book (typically on a scale of 1-5).

    Example:
    {
        "book_id": 1,
        "user_id": 42,
        "review_text": "A very thoughtful and engaging book!",
        "rating": 5,
        "created_by": "user42"
    }
    """

    # book_id: int  # Foreign key to the book table
    user_id: int
    review_text: str
    rating: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": 42,
                "review_text": "A very thoughtful and engaging book!",
                "rating": 5,
                "created_by": "user42",
            }
        }
    )


class ReviewUpdateModel(AuditUpdateModel):
    """
    Pydantic model for updating an existing review.

    This model is used for input when updating a review. It extends the `AuditUpdateModel`,
    which handles audit fields (last_modified_by, etc.).

    Attributes:
    - review_text (Optional[str]): The updated content of the review (optional).
    - rating (Optional[int]): The updated rating for the book (optional).

    Example:
    {
        "review_text": "An updated review text.",
        "rating": 4,
        "last_modified_by": "user42"
    }
    """

    review_text: Optional[str] = None
    rating: Optional[int] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "review_text": "An updated review text.",
                "rating": 4,
                "last_modified_by": "user42",
            }
        }
    )


class ReviewResponseModel(AuditResponseModel):
    """
    Pydantic model for the response containing review data.

    This model is used to return data to the client after creating or retrieving a review.
    It extends the `AuditResponseModel`, which includes audit-related fields.

    Attributes:
    - id (int): The unique identifier for the review.
    - book_id (int): The ID of the book being reviewed.
    - user_id (int): The ID of the user who wrote the review.
    - review_text (str): The content of the review.
    - rating (int): The rating given to the book.

    Example:
    {
        "id": 1,
        "book_id": 1,
        "user_id": 42,
        "review_text": "A very thoughtful and engaging book!",
        "rating": 5,
        "created_by": "user42",
        "created_on": "2024-09-08T12:31:37.056382Z"
    }
    """

    id: int
    book_id: int
    user_id: int
    review_text: str
    rating: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "book_id": 1,
                "user_id": 42,
                "review_text": "A very thoughtful and engaging book!",
                "rating": 5,
                "created_by": "user42",
                "created_on": "2024-09-08T12:31:37.056382Z",
            }
        }
    )
