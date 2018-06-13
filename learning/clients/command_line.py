import json
import os
import sys
from typing import List

from ..reader import TextReader


class CommandLineClient:
    def __init__(self, reader: TextReader, config_folder: str) -> None:
        self.reader = reader
        self.config_folder = config_folder
        self._setup_config_folder()

        self._add_words_to_reader(self.reader.add_known_word, self._known_words_file_name)
        self._add_words_to_reader(self.reader.add_unknown_word, self._unknown_words_file_name)

    def _setup_config_folder(self):
        if not os.path.exists(self.config_folder):
            os.makedirs(self.config_folder, 0o755)

    def _add_words_to_reader(self, reader_add, file_name):
        for word in self._read_words_file(file_name):
            reader_add(word)

    def _read_words_file(self, file_name) -> List[str]:
        if os.path.exists(file_name):
            return json.load(open(file_name))
        return []

    @property
    def _known_words_file_name(self) -> str:
        return os.path.join(self.config_folder, f"known_words_{self.reader.language}.json")

    @property
    def _unknown_words_file_name(self) -> str:
        return os.path.join(self.config_folder, f"unknown_words_{self.reader.language}.json")

    def ask_user(self) -> None:
        self.reader.build_tree()
        print(
            "Now I will ask if you know some words and show some examples "
            "you can either go until the end or you can just hit Control-C and "
            "the flash cards will be generated",
            file=sys.stderr,
        )
        try:
            self._ask_user()
        except KeyboardInterrupt:
            print("User asked to stop", file=sys.stderr)

        self._save_all_words_files()

    def _ask_user(self) -> None:
        for word, examples in self.reader.iterate_unseen_words_with_examples():
            chosen_examples = '", "'.join(examples[:3])
            self._process_word(word, chosen_examples, len(examples))

    def _process_word(self, word, chosen_examples, used_times) -> None:
        while True:
            unseen_words_number = len(self.reader.get_unseen_words())
            print(f"Number of unseen words: {unseen_words_number}")
            rv = input(
                "\n"
                f"Do you know this word {word!r}?\n"
                f"It is used {used_times} times\n"
                f'Examples: "{chosen_examples}"\n'
                f"(y/n/S): "
            )
            user_answer = rv.strip().lower()
            if user_answer in ("y"):
                self.reader.add_known_word(word)
                return
            elif user_answer == "n":
                self.reader.add_unknown_word(word)
                return
            elif user_answer in ("", "s"):
                return

    def _save_all_words_files(self) -> None:
        print(
            f"Done, saving known words {len(self.reader.known_words)} "
            f"and unknown words {len(self.reader.unknown_words)}",
            file=sys.stderr,
        )
        for words, file_name in [
            (self.reader.known_words, self._known_words_file_name),
            (self.reader.unknown_words, self._unknown_words_file_name),
        ]:
            self._save_words_file(list(words), file_name)

    def _save_words_file(self, words, file_name) -> None:
        dumped_data = json.dumps(words)
        # Use dumps instead of dump to avoid cleaning the file without a sucessful dump
        with open(file_name, "w") as f:
            f.write(dumped_data)
