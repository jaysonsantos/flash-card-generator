import json
import os
import re
import sys
from collections import defaultdict
from typing import Dict, Iterator, List, Set, Tuple

from .processors import BaseProcessor


class TextReader:
    RE_LINE_ONLY_NUMBER = re.compile(r"^\d+$")
    RE_LINE_TIME = re.compile(r"^\d+:\d+:\d+")
    RE_CLEAN_WORD = re.compile(r"([\.,?! \"\(\)'“”…„:`-]|<.[^>]*>)")

    sentences: List[str]

    def __init__(self, text, language, sorted_flash_cards=True):
        self.text = text
        self.sorted_flash_cards = sorted_flash_cards

        self.language = language
        processor = BaseProcessor.get_processor(language)
        self.processor = processor(text)

        self.known_words = set()
        self.unknown_words = set()
        self.word_tree_sorted = dict()

    def build_tree(self) -> None:
        self._read_sentences()
        word_tree: Dict[str, List[str]] = defaultdict(list)
        for _, word, phrase in self._read_word_phrase():
            word_tree[word.lower()].append(phrase)
        self.word_tree_sorted = dict(sorted(word_tree.items(), key=lambda x: len(x[1]), reverse=True))

    def add_known_word(self, word) -> None:
        self.known_words.add(word)

    def add_unknown_word(self, word) -> None:
        self.unknown_words.add(word)

    def _read_sentences(self) -> None:
        self.sentences = list(self.processor.iterate_sentences())

    def _read_word_phrase(self) -> Iterator[Tuple[int, str, str]]:
        for line_number, line in enumerate(self.sentences):
            for word in self._read_words(line):
                yield line_number, word, line

    def _read_words(self, line) -> Iterator[str]:
        for word in self.processor.iterate_words(line):
            clean_word = self.RE_CLEAN_WORD.sub("", word)
            if not clean_word or clean_word.isnumeric():
                continue
            yield clean_word

    def iterate_unseen_words(self) -> Iterator[Tuple[str, List[str]]]:
        for word, examples in self.word_tree_sorted.items():
            if word in self.known_words or word in self.unknown_words:
                continue

            yield word, [str(example).strip() for example in examples]

    def iterate_unknown_words(self):
        unknown_words = sorted(self.unknown_words) if self.sorted_flash_cards else self.unknown_words
        for word in unknown_words:
            if word not in self.word_tree_sorted:
                continue
            yield word

    def get_phrases(self, word):
        return self.word_tree_sorted[word]
