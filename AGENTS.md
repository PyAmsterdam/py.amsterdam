# Repository Guidelines

## Project Structure & Module Organization
- `content/` stores Pelican sources; events live in year folders, pages in `content/pages/`, and shared assets in `content/images/`.
- Site configuration resides in `pelicanconf.py` with environment-specific variants (`conf_prod.py`, `conf_preview.py`, `conf_gh_pages.py`); automation lives in `tasks.py` and the `Makefile`.
- The custom theme is under `theme/` (templates plus static files). Update assets here and keep compiled output out of version control.
- `docs/` holds authoring aids such as `event_template.rst`; `output/` is generated HTML and should be rebuilt rather than edited.

## Build, Test, and Development Commands
- `source .venv/bin/activate` reuses the shared project virtualenv; run `python3 -m venv .venv` first if you need to recreate it locally.
- `pip install -r requirements.txt` installs Pelican, plugins, and deployment helpers.
- `make html` builds the site into `output/`; `make serve` hosts it at `http://localhost:8000` for manual review.
- `invoke livereload` watches content, theme, and config files and rebuilds as you edit.
- `invoke gh-pages` publishes a preview build to `gh-pages`; run from a clean tree.

## Coding Style & Naming Conventions
- Follow PEP 8 with four-space indentation for Python helpers; annotate only non-obvious behaviour.
- Write content in reStructuredText. Name events `YYYY/event-name.rst`, include `:event_type:` and `:date:` (YYYY-MM-DD), and add RSVP or external URLs when relevant.
- Store shared imagery in `content/images/`; keep year folders text-only unless the asset is event-specific.

## Testing Guidelines
- Run `make html` (or `invoke build`) before pushing; fix any Pelican warnings.
- Spot-check pages in `output/` or via `make serve`, confirming events render and metadata appears in listings.
- When editing theme templates or JS, use `invoke livereload` and test key breakpoints for layout changes.

## Commit & Pull Request Guidelines
- Write short, present-tense imperative commits (`update who we are`, `add mastodon link`) to match existing history; keep related edits together.
- Reference the affected content in the body if context is needed (e.g., meetup slug, page path).
- PRs should summarise changes, link related events or issues, list verification steps (`make html`, manual checks), and add screenshots for layout updates.
- Confirm the branch merges cleanly and previews (if triggered) match expectations before requesting review.

## Content Contribution Tips
- Start from `docs/event_template.rst`, update titles, slugs, and schedule fields, then move the file into the correct year directory.
- For recurring updates, duplicate the prior event file and adjust metadata to keep formatting consistent.
