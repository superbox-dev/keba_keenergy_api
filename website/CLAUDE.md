# Website

- Never edit `website/docs/`, `scripts/generate-docs.py` generates it:
  - API reference from the docstrings (griffe), the constants page from the `constants` module
  - home, donation, contributing and changelog from the markers in `README.md`, `CONTRIBUTING.md` and `CHANGELOG.md`
  - hand-written pages from `website/content/`
- Pages in `website/content/`: `sidebar_position` but no `title` in the front matter, the title comes from the `#`
  heading
- New section clients get their API reference page from the `KebaKeEnergyAPI` property, no hand-written page
- Design after home-assistant.io:
  - `website/src/css/custom.css` and the wrapped `website/src/theme/TOC/`
  - the project card in `website/src/components/ProjectInfo/`
