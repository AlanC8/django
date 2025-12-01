FROM python:3.12-alpine AS builder

WORKDIR /app


COPY pyproject.toml uv.lock ./


RUN pip install --no-cache-dir uv \
    && uv sync --locked 

# ------------------------
FROM python:3.12-alpine


WORKDIR /app


COPY --from=builder /app/.venv /app/.venv


ENV PATH="/app/.venv/bin:$PATH"


COPY . .


EXPOSE 8000


CMD ["sh", "-c", "python manage.py migrate && gunicorn settings.wsgi:application --workers 3 --bind 0.0.0.0:8000"]

