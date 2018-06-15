from collections import defaultdict

from flask import Blueprint, Flask, abort, jsonify, request
from flask.views import View
from marshmallow import Schema, fields

from ..flash_card import FlashCardGenerator
from ..processors import BaseProcessor
from ..reader import TextReader

main_blueprint = Blueprint("main", __name__, url_prefix="/v1")


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)

    return app


class WordTreeSchema(Schema):
    text = fields.String(required=True)


class FlashCardSchema(Schema):
    known_words = fields.List(fields.String(required=True), required=True)
    unknown_words = fields.List(fields.String(required=True), missing=list)
    text = fields.String(required=True)


class BaseApiMixin:
    language: str
    reader: TextReader

    def validate_language(self, language):
        supported_languages = BaseProcessor.supported_languages()
        if language not in supported_languages:
            response = jsonify(
                {
                    "error": f"{language} is not a supported language, "
                    f'choose between one of these {", ".join(supported_languages)}.'
                }
            )
            response.status_code = 404
            abort(response)
        self.language = language

    def validate_payload(self):
        request_payload = request.get_json()
        if not request_payload:
            response = jsonify({"error": "Invalid payload sent."})
            response.status_code = 400
            abort(response)
        result = self.schema.load(request.json)
        if result.errors:
            response = jsonify({"errors": result.errors})
            response.status_code = 400
            abort(response)
        self.payload = result.data

    def initialize_reader(self):
        self.reader = TextReader(self.payload["text"], self.language)
        self.reader.build_tree()


class WebFlashCardGenerator(BaseApiMixin, View):
    methods = ["POST"]

    def __init__(self):
        self.schema = FlashCardSchema()

    def dispatch_request(self, language):
        self.validate_language(language)
        self.validate_payload()
        self.initialize_reader()
        self.parse_words("known_words", self.reader.add_known_word)
        self.parse_words("unknown_words", self.reader.add_unknown_word)
        return self.get_output_flash_card()

    def parse_words(self, field_name, add_word_function):
        for word in self.payload[field_name]:
            add_word_function(word)

    def get_output_flash_card(self):
        generator = FlashCardGenerator(self.reader)
        return jsonify({"text": generator.export_flash_cards()})


class WordTreeGenerator(BaseApiMixin, View):
    methods = ["POST"]

    def __init__(self):
        self.schema = WordTreeSchema()

    def dispatch_request(self, language):
        self.validate_language(language)
        self.validate_payload()
        self.initialize_reader()
        return jsonify({"word_tree": self.reader.dump_word_tree()})


main_blueprint.add_url_rule(
    "/generate-flash-card/<language>", view_func=WebFlashCardGenerator.as_view("generate_flash_card")
)

main_blueprint.add_url_rule("/build-word-tree/<language>", view_func=WordTreeGenerator.as_view("build_word_tree"))