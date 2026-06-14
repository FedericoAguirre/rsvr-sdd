FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    libpango-1.0-0 libcairo2 libgdk-pixbuf2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install uv && uv pip install --system -r pyproject.toml

COPY . .

EXPOSE 8000

CMD python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000
