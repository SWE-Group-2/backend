# Lifted from https://github.com/orgs/python-poetry/discussions/1879#discussioncomment-216865
FROM python:3.12.1-slim AS python-base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=500 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_REQUESTS_TIMEOUT=500 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Add poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# `builder-base` stage is used to build deps + create our virtual environment
FROM python-base AS builder-base

# Install dependencies
RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential libpq-dev python3-dev && apt-get clean

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python

# Copy project requirement files
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml README.md ./

# Install main dependencies
RUN poetry install --only main --no-root


# `development` image is used during development / testing
FROM python-base AS development
WORKDIR $PYSETUP_PATH


# Copy poetry and venv from previous stage
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# Quicker install as runtime deps are already installed
RUN poetry install
RUN pip install psycopg2-binary

# Copy the app
WORKDIR /app

COPY config.py ./
COPY src ./src/

WORKDIR /app/src

# Expose port for Flask
EXPOSE 5000

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]
