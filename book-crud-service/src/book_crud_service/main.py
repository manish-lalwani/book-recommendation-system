import uvicorn
from fastapi import FastAPI

from book_crud_service.rest.api.book_controller import router as book_router
from book_crud_service.rest.api.review_controller import router as review_router
from book_crud_service.db import create_tables

app = FastAPI(title="BOOK-CRUD-SERVICE",description="This is BOOK-CRUD-SERVICE part of the Book Recommendation System it is responsible for handling CRUD Operation for Book and Reviews")

app.include_router(book_router)
app.include_router(review_router)


@app.on_event("startup")
async def on_startup():
    """
    Event handler that runs on application startup.

    This function ensures that the necessary database tables are created when
    the application starts.
    """
    await create_tables()


if __name__ == "__main__":
    """
    Run the FastAPI application using Uvicorn.

    The app will listen on all available IP addresses (0.0.0.0) on port 5000.
    """
    uvicorn.run(app, host="0.0.0.0", port=5000)
