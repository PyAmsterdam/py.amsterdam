#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import hashlib
import math
import os
from itertools import chain
from pathlib import Path
from urllib.parse import quote_plus


def raise_helper(msg):
    """Raise exception in jinja as a filter."""
    raise Exception(msg)


def cachebust(url, file):
    """Count blake2b of a file to bust cache."""
    with open(file, "rb") as f:
        file_hash = hashlib.blake2b()
        chunk = f.read(8192)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(8192)
    return f"{url}?{file_hash.hexdigest()[:10]}"


JINJA_FILTERS = {
    'raise': raise_helper,
    'quoteplus': quote_plus,
    'count_to_font_size': lambda c: '{p:.1f}%'.format(p=100 + 25 * math.log(c, 2)),
    'chain': lambda ch: list(chain(*ch)),
    'cachebust': cachebust

}

CUR_DIR = Path(__file__).parent.absolute()
AUTHOR = 'PyAmsterdam'
SITENAME = 'PyAmsterdam'
SITEPORT = os.environ.get("SITEPORT", "8000")
SITEURL = os.environ.get("SITEURL", f"http://localhost:{SITEPORT}")

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'
DEFAULT_DATE = "fs"
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False
DELETE_OUTPUT_DIRECTORY = False
# THEME = CUR_DIR.joinpath("themes", "jan-blog")
# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

PLUGINS = [
    # 'minchin.pelican.plugins.nojekyll',
    # 'sitemap',
    'text_generator'
]
PLUGIN_PATHS = [
    str(CUR_DIR.joinpath("plugins", "pelican-plugins")),
    str(CUR_DIR.joinpath("plugins", "my-plugins"))
]
USE_FOLDER_AS_CATEGORY = True

FILENAME_METADATA = "(?P<date>\\d{4}-\\d{2}-\\d{2}).*"
DEFAULT_DATE_FORMAT = "%-d %B %Y"

DATE_FORMATS = {
    'a': '%A %-d %B %Y %-H:%M',
    'b': '%-d %B %Y'
}

ARTICLE_SAVE_AS = "{date:%Y}/{date:%m}/{date:%d}/{slug}.html"
ARTICLE_URL = "{date:%Y}/{date:%m}/{date:%d}/{slug}.html"
THEME = CUR_DIR.joinpath("theme")

GENERATE_TXT = True  # render articles also as TXT

DIRECT_TEMPLATES = [
    "index",
    # "tags",
    # "categories",
    # "archives",
    # "search",
]

DOCUTILS_SETTINGS = {
    # 'debug': True,
    # 'dump_transforms': True,
    # 'expose_internals': 'b:c:d'  # nevim co dela
    # 'footnote-backlinks': False,
    # 'auto_id_prefix': '%',
    # 'table-style': 'borderless',
    # "table_style": 'colwidths-auto',
    # 'table_style': 'borderless',
    # 'html4css1 writer': {
    #     'table-style': 'borderless',
    # }
    # 'report_level': 1,
    # 'strip_classes': 'docutils',
    # 'dump_pseudo_xml': True,

}
