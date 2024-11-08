# syntax=docker/dockerfile:1
# Base image
FROM python:3.10-alpine3.16 as builder

ARG POETRY_VERSION=1.5.1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apk update && apk add --update --no-cache curl build-base \
    && pip install --no-cache-dir --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python3 - -y --version $POETRY_VERSION

WORKDIR /app

COPY chatbot/ chatbot/
COPY helpers/ helpers/
COPY poetry.lock pyproject.toml README.md ./
RUN poetry build

# Final image
FROM python:3.10-alpine3.16

ENV TZ=Europe/Paris \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app"

WORKDIR /app

COPY --from=builder /app/dist ./chatbot/

RUN apk update && apk add --update --no-cache build-base \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --find-links ./chatbot chatbot \
    && mkdir logs

CMD ["chatbot"]
