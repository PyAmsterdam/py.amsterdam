# PyAmsterdam LLM Guide

Guidelines for any LLM working on this repo.

## Project Overview
- Pelican-powered static site for PyAmsterdam (reStructuredText content, custom Jinja templates).
- Domains: `py.amsterdam` (CNAME shipped in build) published via GitHub Pages.

## Key Paths & Structure
- Content: `content/` (events in year folders `YYYY/`, pages in `content/pages/`, shared images in `content/images/`).
- Config: `pelicanconf.py` plus environment variants `conf_prod.py`, `conf_preview.py`, `conf_gh_pages.py`.
- Automation: `Makefile`, `tasks.py` (Invoke tasks).
- Theme: `theme/` (templates + static assets), vendors under `theme/static/vendor/`.
- Docs/helpers: `docs/` (e.g., `event_template.rst`), generated output lives in `output/` (do not commit edits there).

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# alt: uv sync && source .venv/bin/activate
```

## Common Commands
- Build local: `make html` (or `invoke build`)
- Serve: `make serve` or `invoke reserve` (build+serve), live reload: `invoke livereload` / `make devserver`
- Clean: `make clean`
- Prod build: `make prod` (uses `conf_prod.py`)
- Preview build: `PR_NUMBER=123 make preview` (uses `conf_preview.py`)
- GitHub Pages manual publish: `invoke gh-pages` (uses `conf_gh_pages.py`)

## Deployment
- GitHub Actions: `.github/workflows/pelican-gh-pages.yml` builds with Python 3.11 (`make prod`) and deploys to Pages.
- Manual: `invoke gh-pages` pushes `output/` to `gh-pages` branch.

## Content & Coding Style
- PEP 8 for Python helpers; comment only when behaviour is non-obvious.
- Events: name files `YYYY/event-name.rst`, include `:event_type:` and `:date:` (YYYY-MM-DD, add time if needed), add RSVP/external URLs when relevant.
- Use reStructuredText; start from `docs/event_template.rst` or duplicate a prior event for consistency.
- Assets: shared in `content/images/`; keep year folders text-only unless the asset is event-specific.

## Testing
- Run `make html` (or `invoke build`) before pushing; fix Pelican warnings.
- Spot-check rendered pages via `make serve` or the generated `output/`.
- When editing theme/JS, test key breakpoints; `invoke livereload` for fast feedback.

## Environment Variables
- `SITEURL`, `SITEPORT` (defaults localhost:8000)
- `TELEGRAM_URL` (link on site)
- `CDN` (toggle CDN in production configs)
- `PR_NUMBER` (needed for preview builds)

## Plugins & Theme
- Custom plugins in `plugins/my-plugins/`: `summary` (auto summaries) and `text_generator` (plain-text render). Keep them registered in `pelicanconf.py`.
- Jinja filters: `cachebust`, `by_year`, `quoteplus`, `count_to_font_size`, `chain`.
- Theme entrypoints: `theme/templates/index.html`, `theme/templates/article.html`, `theme/templates/events.html`; static JS/CSS in `theme/static/`.

## Commit & PR Guidelines
- Commits: short, present-tense imperative (`update who we are`, `add mastodon link`); keep related edits together.
- PRs: summarize changes, link related events/issues, list verification steps (e.g., `make html`), add screenshots for layout changes, ensure clean merge.
