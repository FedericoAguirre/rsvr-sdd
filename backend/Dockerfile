FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    libpango-1.0-0 libcairo2 libgdk-pixbuf2.0-0 \
    fonts-dejavu fonts-liberation && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock .
RUN pip install uv && uv sync --system --no-dev

COPY . .

EXPOSE 8000

CMD python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000
