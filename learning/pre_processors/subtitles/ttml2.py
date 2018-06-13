from bs4 import BeautifulSoup
from learning.pre_processors import BasePreProcessor


class TTML2PreProcessor(BasePreProcessor):
    name = "ttml2"

    def get_output_text(self) -> str:
        parsed = BeautifulSoup(self.input_text, "lxml")
        return " ".join(parsed.find("div").strings).strip()
