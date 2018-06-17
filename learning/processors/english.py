import spacy

from . import BaseProcessor


class EnglishProcessor(BaseProcessor):
    language = "en"

    spacy = spacy.load(language)
