from pelican import signals
import pelican
from .writers import TextWriter
from pelican.readers import Readers, RstReader
from docutils.writers.html5_polyglot import HTMLTranslator, Writer
import docutils.core
import docutils.nodes
import json
from pathlib import Path

text_articles = {}
events = []


class PelicanHTMLTranslator(HTMLTranslator):

    def visit_abbreviation(self, node):
        attrs = {}
        if node.hasattr('explanation'):
            attrs['title'] = node['explanation']
        self.body.append(self.starttag(node, 'abbr', '', **attrs))

    def depart_abbreviation(self, node):
        self.body.append('</abbr>')

    def visit_image(self, node):
        # set an empty alt if alt is not specified
        # avoids that alt is taken from src
        node['alt'] = node.get('alt', '')
        return HTMLTranslator.visit_image(self, node)


class PelicanHTMLWriter(Writer):

    def __init__(self):
        Writer.__init__(self)
        self.translator_class = PelicanHTMLTranslator


class _FieldBodyTranslator(HTMLTranslator):

    def __init__(self, document):
        HTMLTranslator.__init__(self, document)
        self.compact_p = None

    def astext(self):
        return ''.join(self.body)

    def visit_field_body(self, node):
        pass

    def depart_field_body(self, node):
        pass


class ModifiedRstReader(RstReader):

    # writer_class = PelicanHTMLWriter
    # field_body_translator_class = _FieldBodyTranslator

    def read(self, source_path):
        """Parses restructured text"""
        pub = self._get_publisher(source_path)
        parts = pub.writer.parts
        content = parts.get('body')

        metadata = self._parse_metadata(pub.document, source_path)
        metadata.setdefault('title', parts.get('title'))

        # TextWriter -> global object of article Content [a1, a2, a3]
        # Then during generator save objects from Content
        if self.settings['GENERATE_TXT']:
            output = docutils.core.publish_from_doctree(
                document=pub.document,
                writer=TextWriter(),
                settings_overrides=self.settings['DOCUTILS_SETTINGS']
            )
            text_articles[source_path] = output

        return content, metadata


# class MyGenerator(Generator):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         print("initialized my generator")
#
#     def generate_context(self):
#         print('con', Path(self.settings['THEME_STATIC_DIR']).joinpath('js').exists())
#         # self._update_context('xxx')
#         pass
#
#     def generate_output(self, writer):
#         # print("opt run")
#         print('out', Path(self.settings['THEME_STATIC_DIR']).joinpath('js').exists())
#         pass
#         # send signal my gen done
#
#
# def get_generators(obj):
#     # print(obj)
#     return MyGenerator


def add_reader(readers):
    readers.reader_classes['rst'] = ModifiedRstReader


def write_calendar_js(file_name: Path, content):
    file_name.write_text(
        (
            "document.addEventListener('DOMContentLoaded', function () {"
            f"const eventList = {content};"
            "let calendarEl = document.getElementById('calendar');"
            "let calendar = new FullCalendar.Calendar(calendarEl, {"
            "locale: 'en-gb',"
            "height: 'auto',"
            "plugins: ['dayGrid'],"
            # "defaultDate: '2020-02-12',"
            "editable: true,"
            "eventLimit: true,"
            "events: eventList"
            "});"
            "calendar.render();"
            "});"
        )
    )


def write_events(*args, **kwargs):
    """Write events into TXT and generate calendar list"""

    try:
        if type(args[0]) == pelican.ArticlesGenerator:
            article_generator = args[0]
        else:
            raise TypeError(f"{args[0]} is not pelican.ArticleGenerator but {type(args[0])}")
    except IndexError:
        pelican.logger.warning('Exiting, unsupported arguments: %s, %s', args, kwargs)
        return

    output_path = Path(article_generator.output_path)
    # article_generator.settings
    for article in article_generator.articles:
        # write txt file
        txt_path = output_path.joinpath(
            article.save_as.replace('.html', '.txt')
        )
        txt_path.parent.mkdir(parents=True, exist_ok=True)
        txt_path.write_bytes(text_articles[article.source_path])

        events.append(
            {
                'title': article.metadata.get('event_type', article.title),
                'url': article.metadata.get('external_url', article.url),
                'start': article.date.strftime('%Y-%m-%d')

            }
        )

    write_calendar_js(
        Path(article_generator.theme.joinpath('static', 'js', 'calendar.js')),
        json.dumps(events)
    )


def register():
    # signals.readers_init.connect(add_reader)
    # signals.finalized.connect(create_calendar)
    # signals.get_writer.connect(bubu)
    signals.readers_init.connect(add_reader)
    # signals.content_object_init.connect(bubu)
    # signals.article_writer_finalized.connect(write_events)
    signals.article_generator_finalized.connect(write_events)
    # signals.content_written.connect(bubu)
    # signals.get_generators.connect(get_generators)
