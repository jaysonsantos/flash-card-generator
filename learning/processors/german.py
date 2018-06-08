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
            elif self.is_token_particle(token):
                continue  # ignore because someone took care of it
            else:
                yield token.lemma_

    def get_verb_particle(self, token: Token) -> Optional[Token]:
        if self.is_token_verb(token):
            particle = [
                particle for particle in token.children if self.is_token_particle(particle) and particle.head == token
            ]
            if particle:
                return particle[0]
        return None
