from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from book_crud_service.models.sqlalchemy.base import Base
from book_crud_service.models.sqlalchemy.audit_mixin import AuditMixin


class Book(Base, AuditMixin):
    """
    SQLAlchemy model for the 'books' table.

    This model represents the `books` table in the database and contains fields such as
    the book's title, author, genre, publication year, and summary. It also includes audit
    fields from the `AuditMixin` to track creation and modification details.

    Attributes:
    - id (Column): The primary key and unique identifier for each book.
    - title (Column): The title of the book (non-nullable).
    - author (Column): The author of the book (non-nullable).
    - genre (Column): The genre of the book (optional).
    - year_published (Column): The year the book was published (optional).
    - summary (Column): A brief summary of the book's content (optional).

    Relationships:
    - reviews (relationship): A one-to-many relationship to the `Review` model.
      Deleting a book also deletes all associated reviews (via cascade delete).
    """

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String)
    year_published = Column(Integer)
    summary = Column(Text)

    # One-to-Many relationship
    reviews = relationship(
        "Review", back_populates="book", cascade="all, delete-orphan"
    )
