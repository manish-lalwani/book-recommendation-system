# db.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from book_crud_service.models.sqlalchemy.base import Base
import os
import asyncio

# Database connection URL and engine setup
# Load database configuration from environment variables
url = URL.create(
    drivername=os.getenv("DB_DRIVER", "postgresql+asyncpg"),
    username=os.getenv("DB_USERNAME", "postgres"),
    password=os.getenv("DB_PASSWORD", "secretpassword"),
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "postgres"),
    port=int(os.getenv("DB_PORT", 5432)),
)

engine = create_async_engine(url, echo=True)

# Asynchronous session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Dependency to provide the database session to routes
async def get_db() -> AsyncSession:
    """
    Dependency function to provide a database session to API routes.

    This function yields an instance of `AsyncSession` which will be used to interact
    with the database. The session is automatically closed once the request is completed.

    :yield: An instance of `AsyncSession` bound to the database engine.
    """
    async with AsyncSessionLocal() as session:
        yield session


# Function to create tables
async def create_tables():
    """
    Function to create all database tables defined in the SQLAlchemy models.

    This function uses the engine to run a synchronous creation of tables, defined in
    the `Base` metadata, asynchronously.

    :return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
