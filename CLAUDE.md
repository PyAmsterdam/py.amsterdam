# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the PyAmsterdam community website built with Pelican, a Python-based static site generator. The site showcases meetup events, hosts information, and community pages using reStructuredText content and custom Jinja2 templates.

## Development Environment Setup

**Prerequisites**: Python 3.8+, pip

```bash
# Create virtual environment (if needed)
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Alternative with uv** (if using uv package manager):
```bash
uv sync
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

# Build preview version for PR preview (requires PR_NUMBER env var)
# Example: PR_NUMBER=123 make preview
make preview

# Publish to GitHub Pages (gh-pages branch)
invoke gh-pages
```

**Deployment Targets**:
- **Production**: `https://py.amsterdam` (via `make prod` or `conf_prod.py`)
  - Automatically deployed via GitHub Actions on push to `master` branch
  - Workflow: `.github/workflows/pelican-gh-pages.yml`
- **GitHub Pages**: `https://py.amsterdam` (via `invoke gh-pages` or `conf_gh_pages.py`)
  - Manual deployment option for development previews

## Architecture Overview

### Configuration Files

- **pelicanconf.py**: Base configuration with site metadata, Jinja2 filters, plugin settings, and content organization rules
- **conf_prod.py**: Production configuration for https://py.amsterdam (enables CDN, feeds)
- **conf_gh_pages.py**: GitHub Pages configuration for preview deployments
- **conf_preview.py**: PR preview configuration for https://pr-{PR_NUMBER}.dev.py.amsterdam
- **tasks.py**: Invoke-based task automation for building, serving, and deploying
- **.github/workflows/pelican-gh-pages.yml**: CI build and deploy to GitHub Pages

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

2. **text_generator**: Renders articles as plain text format (controlled by `GENERATE_TXT = True` in config). This generates a `.txt` version of each event article that can be copied directly into meetup.com event descriptions. Access via the "Plain text version" link at the bottom of each event page.

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

**Complete workflow for creating a new event**:

1. Create a draft event on meetup.com (to get the RSVP URL)
2. Copy `docs/event_template.rst` to `content/{YEAR}/YYYY-MM-DD-event-slug.rst`
3. Fill in required metadata:
   - `:event_type:` (e.g., "Meetup")
   - `:date:` (YYYY-MM-DD HH:MM format)
   - `:rsvp_url:` (from meetup.com draft event)
   - `:cover:` (relative path to cover image for SEO)
4. Write event description, schedule table, speaker bios, and abstracts
5. Add cover image to `content/images/` and update `:cover:` field
6. Test locally: `make html && make serve`
7. Push/merge the code and wait for deployment
8. Navigate to `https://py.amsterdam/{YYYY}/{MM}/{DD}/{event-slug}.html`
9. Get the plain text version for meetup.com:
   - Scroll down on the event page and click "Plain text version"
   - Copy the content and paste into the meetup.com draft event
10. Publish the event on meetup.com

**Note**: All event updates should follow the same process to keep both sites in sync.

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

## Commit Guidelines

- Write short, present-tense imperative commits (e.g., "update who we are", "add mastodon link") to match existing history
- Keep related edits together in a single commit
- Reference the affected content in the commit body if context is needed (e.g., meetup slug, page path)
- For PRs:
  - Summarize changes clearly
  - Link related events or issues
  - List verification steps performed (`make html`, manual checks)
  - Add screenshots for layout/visual updates
  - Confirm the branch merges cleanly and previews match expectations before requesting review
