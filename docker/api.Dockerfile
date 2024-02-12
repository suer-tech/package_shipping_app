FROM python:3.12

WORKDIR /code/app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

COPY . .

COPY ./docker/prestart.sh prestart.sh

RUN chmod +x prestart.sh

ENTRYPOINT ["./prestart.sh"]


COPY ./docker/run_server.sh run_server.sh

RUN chmod +x run_server.sh


CMD ["./run_server.sh"]

