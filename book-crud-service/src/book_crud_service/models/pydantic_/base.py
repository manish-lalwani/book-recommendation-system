from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class AuditBase(BaseModel):
    """
    Base Pydantic model for audit-related fields.

    This model serves as a foundation for models that require audit information,
    such as tracking the creator, creation time, last modifier, and last modification time.

    Attributes:
    - created_by (Optional[str]): The user who created the record. Optional during creation.
    - created_on (Optional[datetime]): The timestamp of when the record was created. Optional during creation.
    - last_modified_by (Optional[str]): The user who last modified the record. Optional during updates.
    - last_modified_on (Optional[datetime]): The timestamp of the last modification. Optional during updates.
    """

    created_by: Optional[str] = None  # Optional, required only during creation
    created_on: Optional[datetime] = (
        None  # Optional during creation, set by DB, mandatory in response
    )
    last_modified_by: Optional[str] = None  # Optional, set during updates
    last_modified_on: Optional[datetime] = None  # Optional, set during updates

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class AuditCreateModel(AuditBase):
    """
    Pydantic model for audit fields used during record creation.

    This model extends the `AuditBase` model and enforces that the `created_by` field
    is mandatory when creating a new record. Fields like `created_on` and
    `last_modified_by` are excluded since they are not relevant during creation.

    Attributes:
    - created_by (str): The user who created the record. Mandatory during creation.

    Example Config:
    - Excludes `created_on`, `last_modified_by`, and `last_modified_on` during creation.
    """

    created_by: str

    class Config:
        exclude = {
            "created_on",
            "last_modified_by",
            "last_modified_on",
        }  # Exclude unnecessary fields during creation


class AuditUpdateModel(AuditBase):
    """
    Pydantic model for audit fields used during record updates.

    This model extends the `AuditBase` model and enforces that the `last_modified_by`
    field is mandatory when updating a record. Fields like `created_by` and
    `created_on` remain unchanged during updates.

    Attributes:
    - last_modified_by (str): The user who last modified the record. Mandatory during updates.

    Example Config:
    - Excludes `created_by` and `created_on` during updates.
    """

    last_modified_by: str  # Mandatory during updates

    class Config:
        exclude = {
            "created_by",
            "created_on",
        }  # These fields remain unchanged during updates


class AuditResponseModel(AuditBase):
    """
    Pydantic model for audit fields used in API responses.

    This model extends the `AuditBase` model and ensures that the `created_on` field
    is mandatory when returning data in an API response.

    Attributes:
    - created_on (datetime): The timestamp of when the record was created. Mandatory in API responses.

    Example Config:
    - Includes all fields by default in the response.
    """

    created_on: datetime  # Ensure 'created_on' is mandatory in responses

    class Config:
        pass  # All fields are included in the response
