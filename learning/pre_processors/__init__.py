from typing import Dict, Type


class BasePreProcessor:
    name: str

    _pre_processors: Dict[str, Type["BasePreProcessor"]] = {}

    def __init__(self, input_text: bytes) -> None:
        self.input_text = input_text

    def get_output_text(self) -> str:
        raise NotImplementedError("Pre-processor is not implemented yet")

    @classmethod
    def get_pre_processor(cls, name):
        return cls.get_pre_processors()[name]

    @classmethod
    def get_pre_processors(cls):
        if cls._pre_processors:
            return cls._pre_processors

        for klass in cls.__subclasses__():
            cls._pre_processors[klass.name] = klass

        return cls._pre_processors


import learning.pre_processors.subtitles  # noqa
