FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root

COPY src/ ./src/

#RUN poetry install --only-root

EXPOSE 8000

CMD ["uvicorn", "src.presentation.api:app", "--host", "0.0.0.0", "--port", "8000"]