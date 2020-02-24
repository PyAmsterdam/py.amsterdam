#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import math
from urllib.parse import quote_plus
from itertools import chain
import os
import hashlib
from pathlib import Path

CUR_DIR = Path(__file__).parent.absolute()


def raise_helper(msg):
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

DEFAULT_DATE = "fs"

# DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# THEME = "themes/pelican-themes/pelican-bootstrap3"
# THEME = "themes/pelican-themes/bootstrap"
# THEME = "themes/pelican-theme-bootstrap4"

# PYGMENTS_STYLE = 'solarizeddark'


# PYGMENTS_STYLE = 'monokai'
# PYGMENTS_STYLE = 'paraiso-dark'
# PYGMENTS_STYLE = 'native'
# PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

MENUITEMS = (
    ('title', 'url'),
)

# ##### PELICAN BASIC SETTINGS #####

# --- Main stuff
SITENAME = "Johnny's blog"
SITESUBTITLE = "Learn, apply and share."
SITEDESCRIPTION = SITESUBTITLE
# SITEURL = "http://localhost:63342/pelican/output"
SITEPORT = os.environ.get("SITEPORT", "8000")
SITEURL = os.environ.get("SITEURL", f"http://localhost:{SITEPORT}")
RELATIVE_URLS = False

# --- Default atom feeds
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
# CATEGORY_FEED_ATOM = None
# FEED_ALL_ATOM = None
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
TRANSLATION_FEED_ATOM = None

# --- Article settings
# ARTICLE_EXCLUDES = ["pages"]
# ARTICLE_LANG_SAVE_AS = "{slug}-{lang}.html"
# ARTICLE_LANG_URL = "{slug}-{lang}.html"
# ARTICLE_ORDER_BY = "reversed-date"
# ARTICLE_PATHS = [""]
# ARTICLE_PERMALINK_STRUCTURE = ""
ARTICLE_SAVE_AS = "{date:%Y}/{date:%M}/{date:%d}/{slug}.html"
# ARTICLE_TRANSLATION_ID = "slug"
ARTICLE_URL = "{date:%Y}/{date:%M}/{date:%d}/{slug}.html"

# --- Author settings
AUTHOR = "Jan Gazda"
# theme custom
AUTHOR_BYLINE = {
    'avatar_url': 'https://avatars1.githubusercontent.com/u/7480694',
    'bio': "Hello how are you? I love python🐍 and pies!"
}

# AUTHOR_SAVE_AS = "author/{slug}.html"
# AUTHOR_URL = "author/{slug}.html"
# BIND = ""
# CACHE_CONTENT = False
# CACHE_PATH = "cache"

# CATEGORY_SAVE_AS = "category/{slug}.html"
# CATEGORY_URL = "category/{slug}.html"
# CHECK_MODIFIED_METHOD = "mtime"
# CONTENT_CACHING_LAYER = "reader"
# CSS_FILE = "main.css"
# DATE_FORMATS = {
#     'en': '%Y',
# }
# DAY_ARCHIVE_SAVE_AS = ""
# DAY_ARCHIVE_URL = ""
# DEBUG = False
DEFAULT_CATEGORY = "other"
# DEFAULT_DATE_FORMAT = "%d"
DEFAULT_DATE_FORMAT = "%-d %B %Y"
DEFAULT_LANG = "en"
# DEFAULT_METADATA = {}
# DEFAULT_ORPHANS = 0
DEFAULT_PAGINATION = False
DELETE_OUTPUT_DIRECTORY = False
DIRECT_TEMPLATES = [
    "index",
    "tags",
    # "categories",
    # "archives",
    # "search",
]
# DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_PAGES_ON_MENU = True
DOCUTILS_SETTINGS = {}
# DRAFT_LANG_SAVE_AS = "drafts/{slug}-{lang}.html"
# DRAFT_LANG_URL = "drafts/{slug}-{lang}.html"
# DRAFT_PAGE_LANG_SAVE_AS = "drafts/pages/{slug}-{lang}.html"
# DRAFT_PAGE_LANG_URL = "drafts/pages/{slug}-{lang}.html"
# DRAFT_PAGE_SAVE_AS = "drafts/pages/{slug}.html"
# DRAFT_PAGE_URL = "drafts/pages/{slug}.html"
# DRAFT_SAVE_AS = "drafts/{slug}.html"
# DRAFT_URL = "drafts/{slug}.html"
# EXTRA_PATH_METADATA = {}
# FEED_DOMAIN = ""
# FEED_MAX_ITEMS = ""
FILENAME_METADATA = "(?P<date>\\d{4}-\\d{2}-\\d{2}).*"  # was '(?P<slug>.*)'
# FORMATTED_FIELDS = ["summary"]
# GZIP_CACHE = True
# IGNORE_FILES = ["ign/.*"]
# INDEX_SAVE_AS = "index.html"
# INTRASITE_LINK_REGEX = "[{|](?P<what>.*?)[|}]"
JINJA_ENVIRONMENT = {
    "extensions": ["jinja2.ext.i18n"],
    "lstrip_blocks": True,
    "trim_blocks": True,
}
# JINJA_FILTERS = {}
LINKS = (
    ("Pelican", "http://getpelican.com/"),
    ("Python.org", "http://python.org/"),
    ("Jinja2", "http://jinja.pocoo.org/"),
    ("You can modify those links in your config file", "#"),
)
# LOAD_CONTENT_CACHE = False
# LOCALE = [""]
# LOG_FILTER = []
# MARKDOWN = {
#     "extension_configs": {
#         "markdown.extensions.codehilite": {"css_class": "highlight"},
#         "markdown.extensions.extra": {},
#         "markdown.extensions.meta": {},
#     },
#     "output_format": "html5",
# }
# MONTH_ARCHIVE_SAVE_AS = ""
# MONTH_ARCHIVE_URL = ""
# NEWEST_FIRST_ARCHIVES = True
OUTPUT_PATH = "public/www"
# OUTPUT_RETENTION = []
# OUTPUT_SOURCES = False
# OUTPUT_SOURCES_EXTENSION = ".text"
# PAGE_EXCLUDES = [""]
# PAGE_LANG_SAVE_AS = "pages/{slug}-{lang}.html"
# PAGE_LANG_URL = "pages/{slug}-{lang}.html"
# PAGE_ORDER_BY = "basename"
# PAGE_PATHS = ["pages"]
# PAGE_SAVE_AS = "pages/{slug}.html"
# PAGE_TRANSLATION_ID = "slug"
# PAGE_URL = "pages/{slug}.html"
# PAGINATED_TEMPLATES = ({"author": None, "category": None, "index": None, "tag": None},)
# PAGINATION_PATTERNS = [
#     PaginationRule(min_page=1, URL="{name}{extension}", SAVE_AS="{name}{extension}"),
#     PaginationRule(
#         min_page=2, URL="{name}{number}{extension}", SAVE_AS="{name}{number}{extension}"
#     ),
# ]
PATH = "content"
# PATH_METADATA = ""
# PELICAN_CLASS = "pelican.Pelican"
PLUGINS = [
    "assets",
    'summary',
    'series',
    'minchin.pelican.plugins.nojekyll',
    'sitemap',
    'my_whoosh',
    'html_rst_directive',
]
PLUGIN_PATHS = [
    str(CUR_DIR.joinpath("plugins", "pelican-plugins")),
    str(CUR_DIR.joinpath("plugins", "my-plugins"))
]
# PORT = 8000
PYGMENTS_RST_OPTIONS = {'classprefix': 'pgcss-', 'linenos': 'table'}
# READERS = {}

# REVERSE_CATEGORY_ORDER = False
# RSS_FEED_SUMMARY_ONLY = True

ROBOTS = 'index, follow'

# SLUGIFY_SOURCE = "title"
# SLUG_REGEX_SUBSTITUTIONS = (
#     [("[^\\w\\s-]", ""), ("(?u)\\A\\s*", ""), ("(?u)\\s*\\Z", ""), ("[-\\s]+", "-")],
# )
SOCIAL = (
    ("https://gitlab.com/1oglop1", "gitlab"),
    ("https://github.com/1oglop1", "github"),
    ("https://linkedin.com/in/jangazda", "linkedin"),
)
# STATIC_CHECK_IF_MODIFIED = False
# STATIC_CREATE_LINKS = False
# STATIC_EXCLUDES = []
# STATIC_EXCLUDE_SOURCES = True
# STATIC_PATHS = ["imgs"]
# STATIC_SAVE_AS = "{path}"
# STATIC_URL = "{path}"
# SUMMARY_MAX_LENGTH = 4
TAGS_URL = "tags.html"  # mine
# TAG_SAVE_AS = "tag/{slug}.html"
# TAG_URL = "tag/{slug}.html"
# TEMPLATE_EXTENSIONS = [".html"]
# TEMPLATE_PAGES = {}
THEME = CUR_DIR.joinpath("themes", "jan-blog")
# THEME_STATIC_DIR = "theme"
# THEME_STATIC_PATHS = ["static"]
# THEME_TEMPLATES_OVERRIDES = []
TIMEZONE = "Europe/Amsterdam"
TWITTER_USER_NAME = '1oglop1'
# TYPOGRIFY = False
# TYPOGRIFY_IGNORE_TAGS = []
USE_FOLDER_AS_CATEGORY = True
# WITH_FUTURE_DATES = True
# WRITE_SELECTED = []
# YEAR_ARCHIVE_SAVE_AS = ""
# YEAR_ARCHIVE_URL = ""


# ###### CUSTOM SETTINGS #####
ABSOLUTE_URL = SITEURL

STATIC_CDN = {
    "CSS": (
        # 'href=https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css',
        # # BOOTSTRAP
        # (
        #     'href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" '
        #     'integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" '
        #     'crossorigin="anonymous"'
        # ),
        # FONTAWESOME
        # (
        #     'href="https://use.fontawesome.com/releases/v5.6.3/css/all.css" '
        #     'integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/" '
        #     'crossorigin="anonymous"'
        # )

    ),
    "JS": (
        # JQUERY
        # (
        #     'src="https://code.jquery.com/jquery-3.3.1.slim.min.js" '
        #     'integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" '
        #     'crossorigin="anonymous"'
        # ),
        # AJAX
        # (
        #     'src="https://code.jquery.com/jquery-3.3.1.min.js"'
        #     'integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="'
        #     'crossorigin="anonymous"'
        # ),
        # (
        #     'src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" '
        #     'integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" '
        #     'crossorigin="anonymous"'
        # ),
        # # "BOOTSTRAP": {
        # (
        #     'src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" '
        #     'integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" '
        #     'crossorigin="anonymous"'
        # ),
        # # clipboard
        # (
        #     'src="https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.4/clipboard.min.js"'
        # )
        # (
        #     'src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.2.1/js/bootstrap.bundle.min.js"'
        # )
    ),
}

# CC license
# CC_LICENSE = "CC-BY-NC-SA"
CUSTOM_LICENSE = "All rights reserved."
# CC_LICENSE = "CC-BY-NC-ND"
# CC_NC_CURRENCY = 'EU'
CREDITS = {
    'text': "Attributions &#8230;",
    'url': f'pages/credits.html'
}

# #### SUMMARY plugin ####
SUMMARY_USE_FIRST_PARAGRAPH = True

# #### PYGMENTS
PYGMENTS_STYLE = "default"

SHARIFF_SERVICES = [
    'facebook',
    'linkedin',
    'mail'
]

# #### SITEMAP Plugin ####
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'exclude': ['tag/', 'category/'],
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# #### WHOOSH Plugin ####

# WHOOSH_INDEX_DIRECTORY = os.environ.get("WHOOSH_INDEX_DIRECTORY","../api/whoosh_index")
WHOOSH_INDEX_DIRECTORY = f"{OUTPUT_PATH}/../api/whoosh_index"

# #### ASSETS Plugin ####
# ASSET_CONFIG = (
#     ('TERSER_BIN', '/Users/jangazda/Dropbox/Coding/python/blog/pelican/blog/node_modules/.bin/terser'),
# )

# import sys
#
# sys.path.append('.')
# from assetsfilters import Terser
# from webassets.filter import register_filter
#
# register_filter(Terser)
