FROM python:3.10-alpine

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.14

RUN apk add --no-cache gcc libffi-dev musl-dev postgresql-dev libxml2-dev libxslt-dev git pcre pcre-dev
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY . /app

RUN poetry install
RUN poetry run pip install uvicorn

CMD ["poetry", "run", "uvicorn", "nfeweb.config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]



