from docutils.writers import html4css1, Writer
from .translators import TextTranslator
# from flask_rstpages.parsers import HTMLTranslator
from typing import Iterable, cast


# class HTMLWriter(html4css1.Writer):
#     """Subclass the html4css1.Writer to redefine the translator_class"""
#
#     def __init__(self):
#         # html4css1.writers.Writer.__init__(self)
#         super().__init__()
#         self.translator_class = HTMLTranslator


class TextWriter(Writer):
    supported = ("text",)
    settings_spec = ("No options here.", "", ())
    settings_defaults = {}  # type: Dict

    output = None  # type: str

    def __init__(self):
        # type: # (TextBuilder) -> None
        super().__init__()
        # self.document = document
        self.translator_class = TextTranslator

    def translate(self):
        # type: () -> None
        visitor = TextTranslator(self.document)
        self.document.walkabout(visitor)
        self.output = cast(TextTranslator, visitor).body
