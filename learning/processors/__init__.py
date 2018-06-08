from typing import Iterator, Dict, Type
from spacy.tokens import Span, Token
import spacy


class BaseProcessor:
    language: str
    _processors: Dict[str, Type["BaseProcessor"]] = {}

    def __init__(self, text):
        self.text = text
        self.spacy = spacy.load(self.language)
        self.doc = self.spacy(self.text)

    def is_token_verb(self, token: Token) -> bool:
        return token.pos_ == "VERB"

    def is_token_particle(self, token: Token) -> bool:
        return token.pos_ == "PART"

    def iterate_sentences(self) -> Iterator[Span]:
        for sentence in self.doc.sents:
            yield sentence

    def iterate_words(self, sentence: Span) -> Iterator[Token]:
        for word in sentence:
            if word.text.strip():
                yield word

    @classmethod
    def supported_languages(cls):
        return list(cls.get_processors().keys())

    @classmethod
    def get_processor(cls, language):
        return cls.get_processors()[language]

    @classmethod
    def get_processors(cls):
        if cls._processors:
            return cls._processors

        for klass in cls.__subclasses__():
            cls._processors[klass.language] = klass

        return cls._processors


import learning.processors.english
import learning.processors.german
import learning.processors.french
