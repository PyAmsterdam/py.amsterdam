# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the PyAmsterdam community website built with Pelican, a Python-based static site generator. The site showcases meetup events, hosts information, and community pages using reStructuredText content and custom Jinja2 templates.

## Development Environment Setup

**Prerequisites**: Python 3.14+, uv package manager

```bash
# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate
```

## Common Development Commands

### Building and Serving

```bash
# Build site for local development
make html
# or
invoke build

# Serve site locally at http://localhost:8000
make serve

# Build and serve together
invoke reserve

# Auto-rebuild on file changes with live reload
invoke livereload
# or
make devserver

# Rebuild with delete flag (clean build)
invoke rebuild
```

### Testing and Validation

```bash
# Build the site and check for Pelican warnings
make html

# Preview production build locally
invoke preview

# Clean generated output
make clean
```

### Deployment

```bash
# Build production version (for py.amsterdam domain)
make prod

# Build for GitHub Pages and deploy
invoke gh-pages

# Build preview version (requires PR_NUMBER env var)
make preview
```

## Architecture Overview

### Configuration Files

- **pelicanconf.py**: Base configuration with site metadata, Jinja2 filters, plugin settings, and content organization rules
- **conf_prod.py**: Production configuration for https://py.amsterdam (enables CDN, feeds)
- **conf_gh_pages.py**: GitHub Pages configuration for preview deployments
- **tasks.py**: Invoke-based task automation for building, serving, and deploying

### Content Organization

```
content/
├── 2019/...2023/          # Event articles organized by year
│   └── YYYY-MM-DD-*.rst   # Events named with ISO date prefix
├── pages/                 # Static pages (e.g., Code of Conduct)
└── images/                # Shared assets (logos, banners)
```

**Event Article Structure**: Events use reStructuredText with required metadata fields:
- `:event_type:` (e.g., "Meetup")
- `:rsvp_url:` (Meetup.com or external link)
- `:date:` (YYYY-MM-DD HH:MM format)
- `:cover:` (relative path to cover image for SEO)

Use `docs/event_template.rst` as the starting template for new events.

### Custom Jinja2 Filters (pelicanconf.py)

- **cachebust**: Appends blake2b hash to asset URLs for cache busting
- **by_year**: Groups articles by year for archive pages
- **quoteplus**: URL-encodes strings
- **count_to_font_size**: Logarithmic font sizing for tag clouds
- **chain**: Flattens iterables

### Custom Plugins

Located in `plugins/my-plugins/`:

1. **summary**: Extracts article summaries using `SUMMARY_USE_FIRST_PARAGRAPH` setting (enabled in base config). Automatically uses first `<p>` tag as summary if no explicit markers found.

2. **text_generator**: Renders articles as plain text format (controlled by `GENERATE_TXT = True` in config).

### Theme Structure

```
theme/
├── templates/           # Jinja2 templates for pages and articles
│   ├── index.html      # Homepage
│   ├── events.html     # Events archive (custom direct template)
│   └── article.html    # Individual event pages
└── static/             # CSS, JavaScript, images
```

The theme is custom-built for PyAmsterdam. When modifying templates or static assets, test with `invoke livereload` for instant feedback.

### URL and Path Conventions

- **Article URLs**: `/{YYYY}/{MM}/{DD}/{slug}.html` (defined by `ARTICLE_SAVE_AS` and `ARTICLE_URL`)
- **Filename metadata extraction**: Date parsed from `YYYY-MM-DD-*` filename pattern via `FILENAME_METADATA` regex
- **Date formatting**: Uses strftime format `%-d %B %Y` (day without leading zero, full month name, year)

### Environment Variables

- `SITEURL`: Site base URL (default: http://localhost:8000)
- `SITEPORT`: Development server port (default: 8000)
- `TELEGRAM_URL`: PyAmsterdam Telegram group link
- `CDN`: Enable/disable CDN in production
- `PR_NUMBER`: Required for preview builds

## Development Guidelines

### Adding New Events

1. Copy `docs/event_template.rst` to `content/{YEAR}/YYYY-MM-DD-event-slug.rst`
2. Fill in required metadata (`:event_type:`, `:date:`, `:rsvp_url:`, `:cover:`)
3. Write event description, schedule table, speaker bios, and abstracts
4. Add cover image to `content/images/` and update `:cover:` field
5. Test with `make html` and `make serve`

### Editing Theme or Templates

1. Run `invoke livereload` for automatic rebuilds
2. Template changes appear in `theme/templates/*.html`
3. Static asset changes go in `theme/static/`
4. Test responsive breakpoints manually

### Plugin Development

Custom plugins in `plugins/my-plugins/` must:
- Register via `signals` in `register()` function
- Be added to `PLUGINS` list in `pelicanconf.py`
- Have `__init__.py` importing the plugin module

### Content Style

- Use reStructuredText syntax
- Include schedule tables with `:class: schedule-table`
- Add LinkedIn/website links in `Links` section with `.. _Name: URL` syntax
- End with `.. target-notes::` for automatic link footnotes
- Images use `.. figure::` directive with `{static}` prefix
