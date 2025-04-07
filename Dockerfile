# Вибір базового образу з Python
FROM python:3.12-slim

# Встановлення poetry та залежностей для psycopg2
RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && pip install poetry

# Копіювання файлів, необхідних для poetry
WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# Конфігурація poetry та встановлення залежностей
RUN poetry config virtualenvs.create false
RUN poetry install --only main

# Копіювання всіх файлів проекту
COPY . /app

# Відкриття порту, якщо ваш додаток використовує веб-сервер
EXPOSE 5000

# Виконання міграцій і запуск додатку
CMD poetry run alembic revision --autogenerate -m "Auto-generated migration" && poetry run alembic upgrade head && python src/my_select.py

