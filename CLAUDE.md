# CLAUDE.md

Async Python client (`aiohttp`) for the KEBA KeEnergy Web HMI API (heat pump controllers), published on PyPI and
used by the Home Assistant integration.

## Commands

- Use `uv`, always via `uv run`
- Setup: `./scripts/setup.sh`

```bash
uv run ruff format                   # format (lint.sh only checks)
./scripts/lint.sh                    # all linters and type checks
uv run pytest                        # tests + coverage
uv run pytest --snapshot-update -n 0 # regenerate snapshots (serial only), then review the diff
./scripts/docs.sh                    # docs (Docusaurus, needs Node.js)
./scripts/docs.sh start              # docs with live reload
```

Before finishing a change, run `ruff format`, `lint.sh` and `pytest`, in this order.
`docs.sh` only when `website/`, docstrings, `constants.py`, `README.md`, `CONTRIBUTING.md` or `CHANGELOG.md` changed.

## Rules

- **No breaking changes** to anything without a `_` prefix (classes, methods, signatures, return values, constants,
  exceptions, enum members, behaviour that worked before)
  - **only** when the user explicitly allows it, then as a major release, otherwise always find a compatible way
  - allowed: renames with the old name as alias that raises a `DeprecationWarning` (note it in the changelog), new
    optional parameters whose default keeps the old behaviour, turning a crash (uncaught built-in or `aiohttp`
    exception) into an `APIError` (or a subclass)
  - `TypedDict`s: new keys only as `NotRequired`, never remove, rename or retype keys
- **Python 3.11 minimum**, no syntax or features of newer versions
- Type annotations also for local variables (not for loop, `with`, `except`, comprehension or unpacking targets)
  - union order, also in `isinstance()`: general before specific types, each alphabetical, containers after
    single types and less nested first, `None` last (`float | int | str`, `Exception | HTTPStatus`,
    `Value | list[Value] | list[list[Value]] | None`)
  - type alias for complex annotations (nested or repeated unions)
- Module-level constants with `Final` (`NAME: Final = ...`)
- Comments as complete sentences with a trailing period
- `TypedDict` only for JSON data from or to the Web HMI (optional keys as `NotRequired`), `NamedTuple` only for
  small values that are unpacked (points, pairs), otherwise `@dataclass(frozen=True, kw_only=True)`, mutable only
  when needed
  - existing public types stay as they are, `frozen` or `kw_only` would be a breaking change
- `Enum` for a fixed set of values (modes, states, types, values of the Web HMI), never loose strings or ints
  for them
  - not for open values (names, IDs, numbers) or a one-off choice in a signature (`Literal`)
- Log messages start with a capital letter, no trailing period, values as `%s` arguments
- Style rules apply to new and changed code, existing code only adapted when asked
- Every `.py` file starts with (after the shebang of an executable script, update the end year when editing a
  file, a single year while it equals the start year):

  ```python
  # Copyright 2023-<current year> Michael Hacker
  # SPDX-License-Identifier: Apache-2.0
  ```

- NumPy-style docstrings everywhere, also in tests
- No inline lint/type suppressions, no new ones in the config, no `# pragma: no cover`, fix or test the code
- No real hosts, serial numbers or customer data, use placeholders like `"mocked-host"`
- `git add` new files, the pre-commit hooks only check tracked files
- Never edit generated or CI-managed files (`version.py`, `coverage-badge.svg`)
- **Never edit `CLAUDE.md` files or `.claude/skills/` on your own**, only when asked
  - if a change conflicts with them, stop and ask

## Architecture

- `constants.py`: one `Enum` per section, members are `FloatEndpoint` / `IntegerEndpoint` / `StringEndpoint`
  - `%s` in a path = zero-based device index
  - paths containing `.param.` are writable
- `endpoints.py`: `BaseEndpoints` (payloads, POST to `/var/readWriteVars`, value conversion), one `*Endpoints` class
  per section
- `api.py`: `KebaKeEnergyAPI` with the section clients and `read_data`, `read_message_ids`, `write_data`
- Helpers in the package are `_`-prefixed methods of the class that uses them (`@staticmethod` if they need no
  `self`), not module-level functions
  - used by several classes: method of their shared base class
- Class member order: `__init__`, dunder methods, properties, public methods grouped by topic, helpers directly
  below their first caller
  - applies to new methods, existing ones only moved when asked
- New section: add the property to `KebaKeEnergyAPI`

## Documentation

- Update `website/content/` when the usage or behaviour changes, the API reference and constants are generated
- Keep the `<!--start-…-->` / `<!--end-…-->` markers in `README.md`, `CONTRIBUTING.md` and `CHANGELOG.md`
- Keep `README.md` short (install, a minimal example, the write warning), details go to `website/content/`

## Changelog, versions and git

- Every change users notice gets an entry under `## [Unreleased]` in `CHANGELOG.md` (not refactorings, tests, CI,
  `CLAUDE.md` or skills), use the `changelog` skill
- Version: comes from the git tag (`setuptools-scm`), only release when asked, use the `release` skill
- Work on `develop`
- Only commit or push when asked
- Commit message of a change for an issue starts with its number (`#67 Fix sensors that are not in use`)
