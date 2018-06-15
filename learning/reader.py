import re
from collections import defaultdict
from typing import Dict, Iterator, List, Set, Tuple

from .pre_processors import BasePreProcessor
from .processors import BaseProcessor


class TextReader:
    RE_LINE_ONLY_NUMBER = re.compile(r"^\d+$")
    RE_LINE_TIME = re.compile(r"^\d+:\d+:\d+")
    RE_CLEAN_WORD = re.compile(r"([\.,?! \"\(\)'“”…„:`-]|<.[^>]*>)")

    sentences: List[str]

    def __init__(self, text, language, pre_processor_name=None, sorted_flash_cards=True):
        self.text = self.clean_text(text, pre_processor_name)
        self.sorted_flash_cards = sorted_flash_cards

        self.language = language
        processor = BaseProcessor.get_processor(language)
        self.processor = processor(self.text)

        self.known_words = set()
        self.unknown_words = set()
        self.word_tree_sorted = dict()

    def clean_text(self, text, pre_processor_name) -> str:
        if not pre_processor_name:
            return text
        pre_processor = BasePreProcessor.get_pre_processor(pre_processor_name)
        return pre_processor(text).get_output_text()

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

    def iterate_unseen_words_with_examples(self) -> Iterator[Tuple[str, List[str]]]:
        for word in self.get_unseen_words():
            examples = self.word_tree_sorted[word]
            yield word, [str(example).strip() for example in examples]

    def get_unseen_words(self) -> Set[str]:
        return self.word_tree_sorted.keys() - self.known_words - self.unknown_words

    def iterate_unknown_words(self):
        unknown_words = sorted(self.unknown_words) if self.sorted_flash_cards else self.unknown_words
        for word in unknown_words:
            if word not in self.word_tree_sorted:
                continue
            yield word

    def get_phrases(self, word):
        return self.word_tree_sorted[word]

    def dump_word_tree(self) -> Dict[str, List[str]]:
        tree = {}
        for word, phrases in self.word_tree_sorted.items():
            tree[word] = [phrase.text for phrase in phrases]
        return tree
