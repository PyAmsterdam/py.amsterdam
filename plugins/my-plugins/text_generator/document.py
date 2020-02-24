
from pathlib import Path

from docutils.core import publish_parts, publish_doctree, publish_string
from .writers import TextWriter
import docutils
from docutils.io import FileOutput

class RstDocument:
    def __init__(self, file_name, settings=None):
        self.input_file = Path(file_name)

        self._config = None
        self._rst = None
        self._output = None
        self._document = None

        # self.settings = {'initial_header_level': 2}
        self.settings = settings or {'debug': True}

        with open(self.input_file) as inf:
            self.raw = inf.read()

        # with open('DEST.txt', 'w') as outf:
        #     o = docutils.core.publish_string(
        #         source=self.raw,
        #         writer=TextWriter(),
        #         settings_overrides=self.settings,
        #         destination
        #         destination_path=outf
        #     )
        #     print(o)

    # @property
    # def rst(self):
    #     if not isinstance(self._rst, dict):
    #         htmlrst = publish_parts(
    #             source=self.raw, writer=HTMLWriter(), settings_overrides=self.settings
    #         )
    #         self._rst = htmlrst
    #     return self._rst

    @property
    def document(self):

        if not isinstance(self._document, docutils.nodes.document):
            self._document = publish_doctree(
                source=self.raw,
                settings_overrides=self.settings
            )
        return self._document

    @property
    def myrst(self):
        # generate doctree

        # for dinfo in dtr.traverse - vzit metadata see pelica.readers.py,
        # RstReader._parse_metadata, _FieldBodyTranslator
        # for docinfo in dtr.traverse(docutils.nodes.docinfo):
        #     print(docinfo)
        # # when doctree ready, and metadata ready, publish
        # docutils.core.publish_from_doctree()
        if not isinstance(self._output, bytes):
            self._output = docutils.core.publish_from_doctree(
                self.document,
                writer=TextWriter(),
                settings_overrides=self.settings

            )

            #     publish_parts(
            #     source=self.raw, writer=TextWriter(), settings_overrides=self.settings
            # )

        # doctree = publish_doctree(
        #     source=self.raw,
        #     settings_overrides=self.settings
        # )
        return self._output
