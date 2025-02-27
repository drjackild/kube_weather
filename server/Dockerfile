FROM python:3.13.2-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --frozen

EXPOSE 8000

COPY run.py .
COPY ./weather_api ./weather_api

CMD ["uv", "run", "run.py"]
