FROM python:3.6

RUN pip install -U pip pipenv

RUN groupadd learning -g 1000 && useradd learning -m -u 1000 -g learning

RUN mkdir /learning && chown learning:learning /learning
WORKDIR /learning

COPY --chown=learning:learning Pipfile Pipfile.lock /learning/

USER learning

RUN pipenv install
RUN pipenv run python -m spacy download en
RUN pipenv run python -m spacy download de
RUN pipenv run python -m spacy download fr

COPY --chown=learning:learning learning/ /learning/learning

ENTRYPOINT [ "pipenv", "run", "python", "-m", "learning" ]
