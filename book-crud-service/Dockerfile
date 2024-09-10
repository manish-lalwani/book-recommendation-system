
FROM python:3.10-slim


WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


RUN pip install poetry


COPY pyproject.toml poetry.lock /app/


RUN poetry config virtualenvs.create false


RUN poetry install --no-dev --no-interaction --no-ansi


COPY . /app


ENV DB_DRIVER=postgresql+asyncpg \
    DB_USERNAME=postgres \
    DB_PASSWORD=secretpassword \
    DB_HOST=192.168.49.2 \
    DB_PORT=31150 \
    DB_NAME=postgres


ENV PYTHONPATH=/app/src


EXPOSE 5000


#RUN python src/book_crud_service/db.py


CMD ["uvicorn", "book_crud_service.main:app", "--host", "0.0.0.0", "--port", "5000"]
