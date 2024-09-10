from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from book_crud_service.models.sqlalchemy.base import Base
from book_crud_service.models.sqlalchemy.audit_mixin import AuditMixin


class Review(Base, AuditMixin):
    """
    SQLAlchemy model for the 'reviews' table.

    This model represents the `reviews` table in the database and contains fields such as
    the review text, rating, and references to the book and user. It also includes audit
    fields from the `AuditMixin` to track creation and modification details.

    Attributes:
    - id (Column): The primary key and unique identifier for each review.
    - book_id (Column): Foreign key that references the `books` table. Deleting a book will
      cascade the deletion of associated reviews.
    - user_id (Column): The ID of the user who wrote the review (non-nullable).
    - review_text (Column): The content of the review (non-nullable).
    - rating (Column): The rating given to the book (non-nullable).

    Relationships:
    - book (relationship): A many-to-one relationship with the `Book` model. Each review
      is associated with a single book.
    """

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(
        Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)

    # Many-to-One relationship
    book = relationship("Book", back_populates="reviews")
