from typing import Iterator, Dict, Type, Any
from spacy.tokens import Span, Token
import spacy
from spacy.language import Language


class BaseProcessor:
    language: str
    _processors: Dict[str, Type["BaseProcessor"]] = {}
    ignored_symbols = set("[]{}()")

    _spacy: Any = None

    def __init__(self, text):
        self.text = text
        spacy_instance = self.spacy_instance  # Assigned to make mypy stop complaining
        self.doc = spacy_instance(self.text)

    @property
    def spacy_instance(self) -> Language:
        return self._get_or_cache_spacy()

    @classmethod
    def _get_or_cache_spacy(cls) -> Language:
        if cls._spacy:
            return cls._spacy

        cls._spacy = spacy.load(cls.language)
        return cls._spacy

    def is_token_verb(self, token: Token) -> bool:
        return token.pos_ == "VERB"

    def is_token_particle(self, token: Token) -> bool:
        return token.pos_ == "PART"

    def is_token_punctuation(self, token: Token) -> bool:
        return token.pos_ == "PUNCT"

    def iterate_sentences(self) -> Iterator[Span]:
        for sentence in self.doc.sents:
            yield sentence

    def iterate_words(self, sentence: Span) -> Iterator[Token]:
        for word in sentence:
            if not self.is_token_punctuation(word) and word.text not in self.ignored_symbols and word.text.strip():
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


import learning.processors.english  # noqa
import learning.processors.german  # noqa
import learning.processors.french  # noqa
