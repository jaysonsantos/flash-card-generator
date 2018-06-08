FROM python:3.6

RUN pip install -U pip pipenv

RUN mkdir /learning
WORKDIR /learning

COPY Pipfile Pipfile.lock /learning/

RUN pipenv install
RUN pipenv run python -m spacy download en
RUN pipenv run python -m spacy download de
RUN pipenv run python -m spacy download fr

COPY learning/ /learning/learning

ENTRYPOINT [ "pipenv", "run", "python", "-m", "learning" ]
