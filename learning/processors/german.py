from typing import Iterator, Optional

from spacy.tokens import Token

from . import BaseProcessor


class GermanProcessor(BaseProcessor):
    language = "de"

    def __init__(self, text):
        super().__init__(text)

    def iterate_words(self, sentence) -> Iterator[str]:
        for token in super().iterate_words(sentence):
            verb_particle = self.get_verb_particle(token)
            if verb_particle:
                yield f"{verb_particle.text}{token.lemma_}"
            elif self.is_token_separable_verb_particle(token):
                continue  # ignore because someone took care of it
            else:
                yield self.get_token_lemma(token)

    def get_verb_particle(self, token: Token) -> Optional[Token]:
        if self.is_token_verb(token):
            particle = [
                particle
                for particle in token.children
                if self.is_token_separable_verb_particle(particle) and particle.head == token
            ]
            if particle:
                return particle[0]
        return None

    def is_token_separable_verb_particle(self, token):
        return self.is_token_particle(token) and token.tag_ == "PTKVZ"

    def get_token_lemma(self, token):
        if self.is_token_infititive_verb(token):
            return token.text
        return token.lemma_

    def is_token_infititive_verb(self, token):
        return token.tag_ == "VAINF"
