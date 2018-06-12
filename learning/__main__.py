import os

import click

from learning.clients import CommandLineClient
from learning.flash_card import FlashCardGenerator
from learning.pre_processors import BasePreProcessor
from learning.processors import BaseProcessor
from learning.reader import TextReader


@click.group()
def group():
    pass


@group.command()
@click.argument("file_name", nargs=1, required=True)
@click.option(
    "--pre-processor",
    type=click.Choice(BasePreProcessor.get_pre_processors()),
    help="Use one of the pre processors to extract text from things like subtitles for example.",
)
@click.option(
    "--language",
    type=click.Choice(BaseProcessor.supported_languages()),
    required=True,
    help="Language of the origin text.",
)
@click.option("--output", required=True, help="Output file of the flash card.")
def process_file(output, language, pre_processor, file_name) -> None:
    reader = TextReader(open(file_name).read(), language, pre_processor)

    client = CommandLineClient(reader, os.path.join(os.path.expanduser("~"), ".learning_flash_cards"))
    client.ask_user()

    generator = FlashCardGenerator(reader)
    with open(output, "w") as f:
        f.write(generator.export_flash_cards())


@group.command(help="Run a pre processor to check its output")
@click.argument("file_name", nargs=1, required=True)
@click.option(
    "--pre-processor",
    type=click.Choice(BasePreProcessor.get_pre_processors()),
    help="The pre processor to run.",
    required=True,
)
def run_pre_processor(pre_processor, file_name):
    pre_processor_ = BasePreProcessor.get_pre_processor(pre_processor)
    with open(file_name) as f:
        print(pre_processor_(f.read()).get_output_text())


if __name__ == "__main__":
    group()
