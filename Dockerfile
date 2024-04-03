
FROM python:3.11-slim


WORKDIR /app


COPY pyproject.toml poetry.lock /app/


RUN pip install poetry


RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируйте исходный код в контейнер
COPY ./app /app/app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
