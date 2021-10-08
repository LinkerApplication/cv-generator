FROM python:3.9 as base

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip setuptools poetry
COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt --output requirements.txt

RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt --no-cache-dir


FROM python:3.9-slim

RUN apt-get -y update && apt-get install -y --no-install-recommends libpq-dev && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV DEBUG=0

COPY --from=base /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /backend
COPY generator .

ENV WORKERS=2
ENV THREADS=2
ENV PORT=8000

# Written in a shell format to let variables be evaluated,
# thus container can be stopped only with "docker stop <container-name>" command
ENTRYPOINT gunicorn core.wsgi -w ${WORKERS} --threads ${THREADS} -b 0.0.0.0:${PORT}
