# AGENTS.md

Async Python client (`aiohttp`) for the KEBA KeEnergy Web HMI API (heat pump controllers).
Published on PyPI and used by the Home Assistant integration.

## Commands

- Use `uv`, always via `uv run`
- Setup: `./scripts/setup.sh`

```bash
uv run ruff format                   # format (lint.sh only checks)
./scripts/lint.sh                    # ruff, ty, yamllint, rumdl
uv run pytest                        # tests + coverage
uv run pytest -n0 --snapshot-update  # regenerate snapshots (without xdist), then review the diff
./scripts/docs.sh                    # docs (Docusaurus, needs Node.js)
./scripts/docs.sh start              # docs with live reload
```

Before finishing a change, run:

- `uv run ruff format`
- `./scripts/lint.sh`
- `uv run pytest`

## Rules

- **No breaking changes** to anything usable externally, i.e. everything without a `_` prefix:
  - classes, methods, signatures, return values
  - constants, exceptions
  - enum members (including `_`-prefixed ones)
  - behaviour that worked before
- Allowed:
  - renames, if the old name stays as an alias (note it in the changelog)
  - new parameters, if they are optional and the default keeps the old behaviour
  - turning a crash (uncaught built-in or `aiohttp` exception) into an `APIError`
  - changing `_`-prefixed internals and `Endpoint.extra_writes()`
- **Python 3.11 minimum**, so no:
  - `type` statements
  - PEP 695 generics
  - `typing.override` (Python 3.12) without a fallback
  - `typing.Self` is fine (Python 3.11)
- Every `.py` file starts with (after the shebang of an executable script):

  ```python
  # Copyright 2023 Michael Hacker
  # SPDX-License-Identifier: Apache-2.0
  ```

- NumPy-style docstrings everywhere, also in tests
- No lint or type suppressions (inline or in config), except the existing ignores in `ruff.toml`. Fix the code instead
- No real hosts, serial numbers or customer data, use placeholders like `"mocked-host"`
- `git add` new files, CI only checks tracked files
- Never edit generated or CI-managed files (`version.py`, `coverage-badge.svg`)

## Architecture

- `constants.py`:
  - one `Enum` per section (`System`, `HeatPump`, ...)
  - members are `FloatEndpoint` / `IntegerEndpoint` / `StringEndpoint`
  - `%s` in a path = zero-based device index
  - paths containing `.param.` are writable
  - paths ending in `.values.actValue` need `has_message_id=True` (checked by `tests/test_constants.py`)
- `endpoints.py`:
  - `BaseEndpoints`: payloads, POST to `/var/readWriteVars`, value conversion
  - one `*Endpoints` class per section
  - getters use `_read_float` / `_read_int` / `_read_str` / `_read_int_or_str`
  - enum getters take a keyword-only `human_readable: bool = True`
  - setters use `_parse_enum_value` and copy the flash-memory warning into their docstring
- `api.py`: `KebaKeEnergyAPI` with the section clients and `read_data`, `read_message_ids`, `write_data`
- `error.py`: exceptions
- Helpers are `_`-prefixed methods of the class that uses them (`@staticmethod` if they need no `self`),
  not module-level functions

## Adding an endpoint

1. `constants.py`: add it to the section enum (plus a `BaseEnum` subclass for named values)
2. `endpoints.py`: add `get_*` / `set_*` to the `*Endpoints` class
3. `tests/test_endpoints/test_<section>_section.py`: add tests (see [Tests](#tests))
4. New section only: add the property to `KebaKeEnergyAPI`, the docs page is generated from it

## Documentation

- Docusaurus website in `website/`, deployed to GitHub Pages from `main` (`.github/workflows/page.yml`)
- `scripts/generate-docs.py` writes all pages into `website/docs/` (not tracked, run by `scripts/docs.sh`):
  - API reference from the docstrings (griffe)
  - home, donation, contributing and changelog from the `<!--start-…-->` / `<!--end-…-->` markers
    in `README.md`, `CONTRIBUTING.md` and `CHANGELOG.md`, so keep the markers
- Design after home-assistant.io: `website/src/css/custom.css`, the project card in
  `website/src/components/ProjectInfo/` and the wrapped `website/src/theme/TOC/`

## Tests

- **100% test coverage** (lines and branches) is enforced
- Endpoint tests live in `tests/test_endpoints/test_<section>_section.py`:
  - mock HTTP with `aioresponses`
  - assert the payload via `assert_called_once_with`
  - cover invalid input for setters
  - put large mock payloads in a `*_data.py` module (e.g. `test_heat_circuit_section_data.py`)
- Large expected values (e.g. `read_data()` results, multi-request payloads) are
  [syrupy](https://github.com/syrupy-project/syrupy) snapshots:
  - `assert response == snapshot(name="response")`
  - `assert sent_requests(mock_keenergy_api) == snapshot(name="requests")` (fixture in `tests/conftest.py`)
  - small values stay inline (`assert_called_once_with`, `pytest.approx`)
  - create or update them with `uv run pytest -n0 --snapshot-update`
  - review the `__snapshots__/*.ambr` diff and `git add` them
- Never call, patch or inspect `_`-prefixed methods or attributes (e.g. `BaseEndpoints._read_float()`, `_post()`):
  - call the public API (`KebaKeEnergyAPI`, `*Endpoints` methods)
  - assert return values, raised exceptions or the sent payload

## Changelog and git

- `CHANGELOG.md`:
  - every user-visible change gets an entry under `## [Unreleased]`
  - Keep a Changelog format, past tense
  - identifiers in backticks
  - issues as `([Issue #67][issue-67])`, pull requests as `([PR #19][pr-19])`
  - issue and PR links are defined at the end of their release section, not at the bottom
  - releases are linked at the bottom, before `<!--end-->`:
    - `[Unreleased]` compares the latest release tag (no pre-release) with `HEAD`
    - each release compares its tag with the previous one
    - the first release links to its release tag
- Branches:
  - work on `develop`
  - `main` is the release branch
  - `v*` tags publish to PyPI
- Only commit or push when asked
