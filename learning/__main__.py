import os
import subprocess
import sys

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
    "-p",
    type=click.Choice(BasePreProcessor.get_pre_processors()),
    help="Use one of the pre processors to extract text from things like subtitles for example.",
)
@click.option(
    "--language",
    "-l",
    type=click.Choice(BaseProcessor.supported_languages()),
    required=True,
    help="Language of the origin text.",
)
@click.option("--output", "-o", required=True, help="Output file of the flash card.")
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
    "-p",
    type=click.Choice(BasePreProcessor.get_pre_processors()),
    help="The pre processor to run.",
    required=True,
)
def run_pre_processor(pre_processor, file_name):
    pre_processor_ = BasePreProcessor.get_pre_processor(pre_processor)
    with open(file_name) as f:
        print(pre_processor_(f.read()).get_output_text())


@group.command(help="Run the API")
@click.option("--port", "-p", type=int, help="Port to listen to", default=8000)
@click.option("--host", "-h", help="Host to listen to", default="127.0.0.1")
@click.option("--production", is_flag=True, help="Run with gunicorn for production", default=False)
@click.argument("extra_args", nargs=-1)
def run_server(port, host, production, extra_args):
    if production:
        address = f"{host}:{port}"
        process = subprocess.Popen(
            ["gunicorn", "-b", address] + list(extra_args) + ["learning.clients.web:create_app()"]
        )
        sys.exit(process.wait())

    from learning.clients.web import create_app

    app = create_app()
    app.run(host, port, debug=True)


if __name__ == "__main__":
    group()
