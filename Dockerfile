FROM python:3.6-slim

RUN apt-get update && \
    apt-get install build-essential libxml2-dev libxslt-dev -y && \
    apt-get clean && \
    rm -rf /var/cache/apt/* &&\
    pip install -U pip pipenv && \
    groupadd learning -g 1000 && \
    useradd learning -m -u 1000 -g learning && \
    mkdir /learning && chown learning:learning /learning

WORKDIR /learning

COPY --chown=learning:learning Pipfile Pipfile.lock /learning/

USER learning

RUN pipenv install && \
    pipenv run python -m spacy download en && \
    pipenv run python -m spacy download de && \
    pipenv run python -m spacy download fr && \
    pipenv run pip install -U gunicorn

ENV PYTHONPATH=/learning
COPY --chown=learning:learning learning/ /learning/learning

ENTRYPOINT [ "pipenv", "run", "python", "-m", "learning" ]
EXPOSE 8000
