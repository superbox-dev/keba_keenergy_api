# AGENTS.md

Async Python client (`aiohttp`) for the KEBA KeEnergy Web HMI API (heat pump controllers).
Published on PyPI and used by the Home Assistant integration.

## Commands

Use `uv`, always via `uv run`. Setup: `./scripts/setup.sh`.

```bash
uv run ruff format              # format (lint.sh only checks)
./scripts/lint.sh               # ruff, ty, yamllint, rumdl
uv run pytest                   # tests + coverage
uv run mkdocs build --strict    # docs
```

Run `uv run ruff format`, `./scripts/lint.sh` and `uv run pytest` before finishing a change.

## Rules

- **No breaking changes** to anything usable externally: public methods, signatures, return values, constants,
  enum members (including `_`-prefixed ones), exceptions and behaviour that worked before. Renames keep the old name
  as an alias (noted in the changelog). A crash (`KeyError`, ...) may become an `APIError`. `_`-prefixed internals
  and `Endpoint.extra_writes()` may change.
- **100% test coverage** is enforced.
- **Python 3.11 minimum**: no `type` statements, PEP 695 generics, or `typing.Self`/`override` without a fallback.
- NumPy-style docstrings (not required in tests). Fix lint errors instead of adding `# noqa`; if unavoidable,
  name the rule code.
- Never edit `keba_keenergy_api/version.py` (generated) or `coverage-badge.svg` (CI updates it).

## Architecture

- `constants.py`: one `Enum` per section (`System`, `HeatPump`, ...) of `FloatEndpoint` / `IntegerEndpoint` /
  `StringEndpoint`. In paths, `%s` is the zero-based device index. Paths containing `.param.` are writable.
  Paths ending in `.values.actValue` need `has_message_id=True` (checked by `tests/test_constants.py`).
- `endpoints.py`: `BaseEndpoints` (payloads, POST to `/var/readWriteVars`, conversion) and one `*Endpoints` class
  per section. Getters use `_read_float` / `_read_int` / `_read_str` / `_read_int_or_str`; enum getters take a
  keyword-only `human_readable: bool = True`. Setters use `_parse_enum_value` and copy the flash-memory warning
  into their docstring.
- `api.py`: `KebaKeEnergyAPI` with the section clients and `read_data`, `read_message_ids`, `write_data`.
- `error.py`: exceptions.

## Adding an endpoint

1. Add it to the section enum in `constants.py` (plus a `BaseEnum` subclass for named values).
2. Add `get_*` / `set_*` to the `*Endpoints` class in `endpoints.py`.
3. Test in `tests/test_endpoints/test_<section>_section.py` with `aioresponses`, asserting the payload via
   `assert_called_once_with`. Cover invalid input for setters.
4. New section: add a page in `docs/keba-keenergy/api/endpoints/`, the `mkdocs.yml` nav entry and the
   mkdocstrings `filters` entry.

## Changelog and git

- Every user-visible change gets an entry under `## [Unreleased]` in `CHANGELOG.md` (Keep a Changelog, past tense,
  identifiers in backticks, issues as `([Issue #67][issue-67])`).
- Work on `develop`; `main` is the release branch, `v*` tags publish to PyPI.
- Only commit or push when asked.
