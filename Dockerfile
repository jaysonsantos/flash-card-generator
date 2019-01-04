FROM python:3.7-slim

RUN apt-get update && \
    apt-get install build-essential libxml2-dev libxslt-dev -y && \
    apt-get clean && \
    rm -rf /var/cache/apt/* &&\
    pip install -U pip poetry && \
    groupadd learning -g 1000 && \
    useradd learning -m -u 1000 -g learning && \
    mkdir /learning && chown learning:learning /learning

WORKDIR /learning

COPY --chown=learning:learning pyproject.toml poetry.lock /learning/

USER learning

RUN poetry install && \
    poetry run python -m spacy download en && \
    poetry run python -m spacy download de && \
    poetry run python -m spacy download fr && \
    poetry run pip install -U gunicorn

ENV PYTHONPATH=/learning
COPY --chown=learning:learning learning/ /learning/learning

ENTRYPOINT [ "poetry", "run", "python", "-m", "learning" ]
EXPOSE 8000
