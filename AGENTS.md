# AGENTS.md

Async Python client (`aiohttp`) for the KEBA KeEnergy Web HMI API (heat pump controllers).
Published on PyPI and used by the Home Assistant integration.

## Commands

- Use `uv`, always via `uv run`
- Setup: `./scripts/setup.sh`

```bash
uv run ruff format              # format (lint.sh only checks)
./scripts/lint.sh               # ruff, ty, yamllint, rumdl
uv run pytest                   # tests + coverage
uv run mkdocs build --strict    # docs
```

Before finishing a change, run:

- `uv run ruff format`
- `./scripts/lint.sh`
- `uv run pytest`

## Rules

- **No breaking changes** to anything usable externally:
  - public methods, signatures, return values
  - constants, exceptions
  - enum members (including `_`-prefixed ones)
  - behaviour that worked before
- Allowed:
  - renames, if the old name stays as an alias (note it in the changelog)
  - new parameters, if they are optional and the default keeps the old behaviour
  - turning a crash (`KeyError`, ...) into an `APIError`
  - changing `_`-prefixed internals and `Endpoint.extra_writes()`
- **Python 3.11 minimum**, so no:
  - `type` statements
  - PEP 695 generics
  - `typing.Self` / `override` without a fallback
- Every `.py` file starts with:

  ```python
  # Copyright 2023 Michael Hacker
  # SPDX-License-Identifier: Apache-2.0
  ```

- NumPy-style docstrings (not required in tests)
- No `# noqa`, no `# type: ignore`, no new `ruff.toml` ignores. Fix the code instead
- `git add` new files, CI only checks tracked files
- Never edit:
  - `keba_keenergy_api/version.py` (generated)
  - `coverage-badge.svg` (updated by CI)

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

## Adding an endpoint

1. `constants.py`: add it to the section enum (plus a `BaseEnum` subclass for named values)
2. `endpoints.py`: add `get_*` / `set_*` to the `*Endpoints` class
3. `tests/test_endpoints/test_<section>_section.py`: add tests (see [Tests](#tests))
4. New section only:
   - page in `docs/keba-keenergy/api/endpoints/`
   - `mkdocs.yml` nav entry
   - mkdocstrings `filters` entry

## Tests

- **100% test coverage** (lines and branches) is enforced
- Endpoint tests live in `tests/test_endpoints/test_<section>_section.py`:
  - mock HTTP with `aioresponses`
  - assert the payload via `assert_called_once_with`
  - cover invalid input for setters
  - put large payloads in a `*_data.py` module (e.g. `test_heat_circuit_section_data.py`)
- Never test or patch internal methods or attributes (e.g. `BaseEndpoints._read_float()`, `_post()`):
  - call the public API (`KebaKeEnergyAPI`, `*Endpoints` methods)
  - assert return values, raised exceptions or the sent payload

## Changelog and git

- `CHANGELOG.md`:
  - every user-visible change gets an entry under `## [Unreleased]`
  - Keep a Changelog format, past tense
  - identifiers in backticks
  - issues as `([Issue #67][issue-67])`
- Branches:
  - work on `develop`
  - `main` is the release branch
  - `v*` tags publish to PyPI
- Only commit or push when asked
