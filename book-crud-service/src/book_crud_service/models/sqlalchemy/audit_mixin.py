from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func


class AuditMixin:
    """
    SQLAlchemy mixin class to add audit fields to database models.

    This mixin is used to track the creation and modification details of database records.
    It adds fields for the user who created the record, the timestamp when it was created,
    the user who last modified the record, and the timestamp of the last modification.

    Attributes:
    - created_by (Column): The user who created the record. This field is non-nullable.
    - created_on (Column): The timestamp when the record was created. It defaults to the current time (server-side).
    - last_modified_by (Column): The user who last modified the record. This field is nullable.
    - last_modified_on (Column): The timestamp when the record was last modified. It updates automatically on modification.
    """

    created_by = Column(String, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    last_modified_by = Column(String, nullable=True)
    last_modified_on = Column(DateTime(timezone=True), onupdate=func.now())
