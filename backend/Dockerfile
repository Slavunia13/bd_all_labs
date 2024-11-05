FROM python:3.13 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.13

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY app .

CMD ["/bin/sh", "-c", "python3 __main__.py"]

