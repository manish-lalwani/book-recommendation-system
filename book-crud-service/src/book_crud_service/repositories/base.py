from typing import Type, TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy.exc import NoResultFound

T = TypeVar("T")  # Generic type for models


class BaseRepository(Generic[T]):
    """
    A generic repository class for handling common database operations.

    This class provides basic CRUD (Create, Read, Update, Delete) functionality for any model.
    It operates asynchronously with SQLAlchemy's `AsyncSession` to perform database operations.

    Attributes:
    - model (Type[T]): The SQLAlchemy model type this repository is operating on.
    - session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.

    Methods:
    - get(id): Fetch a single record by its ID.
    - get_all(): Fetch all records of the model.
    - create(obj_in): Add a new record to the database.
    - update(id, obj_in): Perform a full update of an existing record by replacing all fields.
    - patch(id, obj_in): Perform a partial update of an existing record by updating only the provided fields.
    - delete(id): Delete a record by its ID.
    """

    def __init__(self, model: Type[T], session: AsyncSession):
        """
        Initialize the repository with a model and a database session.

        :param model: The SQLAlchemy model class.
        :param session: The asynchronous session used to interact with the database.
        """
        self.model = model
        self.session = session

    async def get(self, id: int) -> Optional[T]:
        """
        Fetch a single record by its ID.

        :param id: The primary key of the record to fetch.
        :return: The record if found, otherwise None.
        """
        return await self.session.get(self.model, id)

    async def get_all(self) -> List[T]:
        """
        Fetch all records for the model.

        :return: A list of all records in the table.
        """
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, obj_in: T) -> T:
        """
        Add a new record to the database.

        :param obj_in: The model instance to be added.
        :return: The newly created record, after the transaction is committed and refreshed.
        """
        self.session.add(obj_in)
        await self.session.commit()
        await self.session.refresh(obj_in)
        return obj_in

    async def update(self, id: int, obj_in: Dict[str, Any]) -> Optional[T]:
        """
        Perform a full update of an existing record by replacing all fields.

        :param id: The primary key of the record to update.
        :param obj_in: A dictionary containing the updated field values.
        :return: The updated record, or None if no record was found.
        """

        stmt = (
            sqlalchemy_update(self.model)
            .where(self.model.id == id)
            .values(**obj_in)
            .execution_options(synchronize_session="fetch")
        )

        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            return None  # No record found to update

        await self.session.commit()
        return await self.get(id)

    async def patch(self, id: int, obj_in: Dict[str, Any]) -> Optional[T]:
        """
        Perform a partial update of an existing record by updating only the provided fields.

        :param id: The primary key of the record to patch.
        :param obj_in: A dictionary containing the fields to be updated.
        :return: The updated record, or None if no record was found.
        """
        stmt = (
            sqlalchemy_update(self.model)
            .where(self.model.id == id)
            .values(**obj_in)
            .execution_options(synchronize_session="fetch")
        )

        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            return None  # No record found to patch

        await self.session.commit()
        return await self.get(id)

    async def delete(self, id: int) -> None:
        """
        Delete a record by its ID.

        :param id: The primary key of the record to delete.
        :return: None
        """
        stmt = sqlalchemy_delete(self.model).where(self.model.id == id)

        result = await self.session.execute(stmt)
        if result.rowcount > 0:
            await self.session.commit()
