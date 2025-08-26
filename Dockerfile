FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main

COPY ./app ./app

EXPOSE 8000

CMD ["poetry", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
