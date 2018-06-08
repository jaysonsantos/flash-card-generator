import io

from .reader import TextReader


class FlashCardGenerator:
    def __init__(self, reader: TextReader) -> None:
        self.reader = reader

    def export_flash_cards(self) -> str:
        # TODO: Change this maybe to use a proper API, i don't know if it is ok to use google like that
        # TODO: Refactor this method
        from googletrans import Translator

        translator = Translator()
        with io.StringIO() as f:
            for word in self.reader.iterate_unknown_words():
                f.write(f"{word}")

                phrases = self.reader.get_phrases(word)
                for phrase in phrases:
                    clean_phrase = phrase.text.strip().replace("\n", "")
                    f.write(f"<br />{clean_phrase}")

                f.write("\t")
                for i, phrase in enumerate(
                    translator.translate([phrase.text.strip().replace("\n", " ") for phrase in phrases])
                ):
                    if i != 0:
                        f.write("<br />")
                    f.write(phrase.text)
                f.write("\n")

            f.seek(0)
            return f.read()
