# Base image
FROM python:3.10-alpine AS builder

ARG POETRY_VERSION=2.0.0
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN apk update && apk add --update --no-cache curl build-base \
    && pip install --no-cache-dir --upgrade pip pipx \
    && pipx install poetry==${POETRY_VERSION}

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY chatbot/ chatbot/
COPY helpers/ helpers/
COPY poetry.lock pyproject.toml README.md ./
RUN poetry build

# Final image
FROM python:3.10-alpine

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
