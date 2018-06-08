import os
import sys

import click
from learning.clients import CommandLineClient
from learning.flash_card import FlashCardGenerator
from learning.processors import BaseProcessor
from learning.reader import TextReader


@click.group()
def group():
    pass


@group.command()
@click.argument("file_name", nargs=1, required=True)
@click.option("--language", type=click.Choice(BaseProcessor.supported_languages()), required=True)
@click.option("--output", required=True)
def process_file(output, language, file_name) -> None:
    reader = TextReader(open(file_name).read(), language)

    client = CommandLineClient(reader, os.path.join(os.path.expanduser("~"), ".learning_flash_cards"))
    client.ask_user()

    generator = FlashCardGenerator(reader)
    with open(output, "w") as f:
        f.write(generator.export_flash_cards())


if __name__ == "__main__":
    group()
