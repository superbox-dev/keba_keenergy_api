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
`docs.sh` only when `website/`, docstrings, `sections.py`, `enums.py`, `models.py`, `constants.py`, `README.md`,
`CONTRIBUTING.md` or `CHANGELOG.md` changed.

## Rules

- **No breaking changes** to anything without a `_` prefix (classes, methods, signatures, return values, constants,
  exceptions, enum members, behavior that worked before)
  - **only** when the user explicitly allows it, then as a major release, otherwise always find a compatible way
  - allowed: renames with the old name as alias that raises a `DeprecationWarning` (note it in the changelog), new
    optional parameters whose default keeps the old behavior, turning a crash (uncaught built-in or `aiohttp`
    exception) into an `APIError` (or a subclass)
  - `TypedDict`s: new keys only as `NotRequired`, never remove, rename or retype keys
- **Python 3.14.2 minimum** (same as the Home Assistant integration)
  - `type` aliases, PEP 695 generics and deferred annotations, no `TypeAlias`, `TypeVar` or string annotations
- Type annotations also for local variables (not for loop, `with`, `except`, comprehension or unpacking targets)
  - union order, also in `isinstance()`: general before specific types, each alphabetical, containers after
    single types and less nested first, `None` last (`float | int | str`, `Exception | HTTPStatus`,
    `Value | list[Value] | list[list[Value]] | None`)
  - type alias for complex annotations (nested or repeated unions)
- Module-level constants with `Final` (`NAME: Final = ...`)
  - containers read-only: `Final[Mapping[...]]`, `Final[Sequence[...]]` or a `tuple`
- Comments as complete sentences with a trailing period
- US English everywhere (names, docstrings, comments, docs, changelog), e.g. `behavior`, `tank`
- `TypedDict` only for JSON data from or to the Web HMI (optional keys as `NotRequired`), `NamedTuple` only for
  small values that are unpacked (points, pairs), otherwise `@dataclass(frozen=True, kw_only=True)`, mutable only
  when needed
  - existing public types stay as they are, `frozen` or `kw_only` would be a breaking change
- `Enum` for a fixed set of values (modes, states, types, values of the Web HMI), never loose strings or ints
  for them
  - not for open values (names, IDs, numbers) or a one-off choice in a signature (`Literal`)
- Parameters: options keyword-only (after `*`), `/` only for `_`-prefixed helpers, never in public methods
  - new code only, adding `*` or `/` to an existing public method is a breaking change
- Credentials, tokens and serial numbers never in log or exception messages
- Every request has a timeout (`API_DEFAULT_TIMEOUT`), also with a passed session
- Log messages start with a capital letter, no trailing period, values as `%s` arguments
- Every file follows `.editorconfig`, whether a linter checks it or not
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
- No new dependencies (`pyproject.toml`, also dev dependencies) without asking first
- `git add` new files, the pre-commit hooks only check tracked files
- Never edit generated or CI-managed files (`version.py`, `coverage-badge.svg`)
- **Never edit `CLAUDE.md` files or `.claude/skills/` on your own**, only when asked
  - if a change conflicts with them, stop and ask

## Architecture

- `sections.py`: one `Enum` per device type (`device_type` as class keyword), members are `Endpoint`s
  - `path` relative to `APPL.CtrlAppl`, `%s` = zero-based device index
  - paths containing `.param.` are writable, other paths only with `writable=True`
  - `message_id`: component node with a `state.msgId`, only when confirmed on a controller
  - `unit`: unit of the raw value as the Web HMI delivers it, `None` for ratios (`0..1`)
    - always derived from the `unitId` of the variable and its conversion in `var/readAllUnits?action=getUnits`
      (display = raw × `multiplier` / `divisor`), the `unitId` itself is the display unit (`TimeHour` and `TimeMin`
      deliver seconds, `kWh` delivers joule, `MassFlow` delivers kg/s)
  - `HAS_*` options only when the gated endpoints have no `message_id`, the message id already shows availability
  - values of an energy meter (`*Meter` with `power`, `accumulatedHeat`, `heatDay`, `massFlow`) always as
    `[<METER>_]METER_[ACCUMULATED_|DAILY_]<QUANTITY>`, values of `sStatisticalData` without `METER` (`TOTAL_` only
    for the sum of all modes)
    - sensors named `*Meter` with only an `actValue` (e.g. `SourceFlowMeter`) are named like other sensors
    - `<METER>_` prefix only when a section has several meters of the same kind (`HEATING_`, `DHW_`, `COOLING_`,
      `SOURCE_` for the heat meters of the heat pump)
- `enums.py`: values of the Web HMI, `models.py`: `Reading`, `MessageId`, `DeviceCounts`, …,
  `exceptions.py`: `APIError` and subclasses
- `client.py`: `KebaKeEnergyAPI`, transport (POST to `/var/readWriteVars`), payloads and type conversion
  - **no conversion of values** beyond the type (no rounding, scaling or interpretation), that is up to the caller
- **Section and enum member names are always the correct technical term for what they deliver**, valid for every
  controller (e.g. fan or pump), not only for the test device
  - based on the KEBA variable and the Web HMI texts (EN and DE), checked against path, type, unit and limits
  - different from KEBA only where its name is ambiguous or technically wrong (e.g. `HeatingCircuit`, not `HeatCircuit`)
  - established technical abbreviations instead of long names (`DHW`, `COP`, `SPF`)
  - grammatically correct, consistent forms: activities and states as `-ING` form or noun (`AUTO_HEATING`,
    `WAITING_FOR_COMPRESSOR`), never imperatives or bare verbs (`AUTO_HEAT`, `WAIT_FOR_COMPRESSOR`)
  - fixed patterns: `TARGET_*`, `HAS_*` (options), `USE_*` (parameters), `*_ACTIVE` (boolean actual values),
    `EXCESS_ENERGY_*` as prefix, `*_SPEED`, `*_THERMAL_ENERGY` / `*_ELECTRICAL_ENERGY`, `*_FAILURE`
- Helpers in the package are `_`-prefixed methods of the class that uses them (`@staticmethod` if they need no
  `self`), not module-level functions
  - used by several classes: method of their shared base class
- All errors are raised as `APIError` or a subclass, never as a raw `aiohttp` or built-in exception
  - except programming errors in the endpoint definitions (e.g. a `message_id` without the device index of the path)
  - the responses of the Web HMI always have the expected shape, no extra checks of their structure
- Constants always in `constants.py`, also the module-private ones (`_` prefix)
- Class member order: `__init__`, dunder methods, properties, public methods grouped by topic, helpers directly
  below their first caller
  - applies to new methods, existing ones only moved when asked
- New device type: add its enum to `type Section`

## Documentation

- Update `website/content/` when the usage or behavior changes, the API reference, sections, enums and models are generated
- Keep the `<!--start-…-->` / `<!--end-…-->` markers in `README.md`, `CONTRIBUTING.md` and `CHANGELOG.md`
- Keep `README.md` short (install, a minimal example, the write warning), details go to `website/content/`

## Changelog, versions and git

- Every change users notice gets an entry under `## [Unreleased]` in `CHANGELOG.md` (not refactorings, tests, CI,
  `CLAUDE.md` or skills), use the `changelog` skill
- Version: comes from the git tag (`setuptools-scm`), only release when asked, use the `release` skill
- Work on `develop`
- Only commit or push when asked
- Commit message of a change for an issue starts with its number (`#67 Fix sensors that are not in use`)
