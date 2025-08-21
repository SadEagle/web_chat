FROM docker.io/library/ubuntu:25.10

RUN apt update && apt install -y python3.13 curl nginx
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /backend
COPY ./uv.lock ./pyproject.toml ./
RUN uv sync --frozen --no-cache

COPY ./app ./app
CMD [ "./.venv/bin/fastapi", "run", "./app/main.py" ]

EXPOSE 8000

