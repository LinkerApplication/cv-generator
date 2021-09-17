# Pull base image
FROM python:3.9

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
# Turn on pip version checking
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
# Set required poetry version
ENV POETRY_VERSION=1.1.8

# Update pip setuptools and download poetry
RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Set work directory
WORKDIR /backend
# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml /backend/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . /backend/