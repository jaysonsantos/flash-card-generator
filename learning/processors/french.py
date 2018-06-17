import spacy

from . import BaseProcessor


class FrenchProcessor(BaseProcessor):
    language = "fr"

    spacy = spacy.load("fr")
