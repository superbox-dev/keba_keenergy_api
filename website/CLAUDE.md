# Website

- Never edit `website/docs/`, `scripts/generate-docs.py` generates it:
  - API reference from the docstrings (griffe), the sections, enums and models pages from the modules
  - home, donation, contributing and changelog from the markers in `README.md`, `CONTRIBUTING.md` and `CHANGELOG.md`
  - hand-written pages from `website/content/`
- Pages in `website/content/`: `sidebar_position` but no `title` in the front matter, the title comes from the `#`
  heading
- New sections and enums appear on the generated pages, no hand-written page
- `website/content/usage.md` sections: read data, session, project-specific sections, errors
- Examples only with test data or placeholders, never real credentials, serial numbers or meter point numbers
- Preview image for shared links: `website/static/img/social-card.png` (1200 × 630, same layout in all projects)
- The navbar links to the website of the Home Assistant integration (`Integration`)
- Design after home-assistant.io:
  - `website/src/css/custom.css` and the wrapped `website/src/theme/TOC/`
  - only the dark theme, no switch, colors of contributors.home-assistant.io, except the links
  - `custom.css` is the same in all four projects, it has the light and the dark theme
  - the right column at least `17.5rem` wide on smaller screens
  - translucent header without blur, search as a rounded field with a `/` hint, `/` focuses it on every keyboard
    layout (`website/src/searchShortcut.ts`, the shortcut of the search plugin is off)
  - category cards with Lucide icons (`lucide-react`, `website/src/theme/DocCard/Heading/Icon/`)
  - the project card in `website/src/components/ProjectInfo/` shows the brand logo of the integration
    (`website/static/logo.png`, `dark_logo.png`), like the integration card
