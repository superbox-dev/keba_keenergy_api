# Contributing

<!--start-contributing-->

## Guidelines

Contributing to this project should be as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features

## Getting started

The project uses [uv](https://docs.astral.sh/uv/).

Set up the project with `./scripts/setup.sh`. This installs the dependencies, the [prek](https://prek.j178.dev) hooks
and a git `pre-push` hook that validates release tags.

## Pull requests

Pull requests are the best way to propose changes to the codebase.

1. Fork the repository and create your branch from `develop`. `main` is the release branch.
2. Update the documentation in `website/content/` if you changed something user-visible.
3. Add an entry under `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md).
4. Make sure `./scripts/lint.sh` and `uv run pytest` pass.
5. Open the pull request against `develop`.

Never use real credentials, serial numbers or IP addresses of your heat pump in code, tests or issues.

## Coding style

`./scripts/lint.sh` runs [ruff](https://docs.astral.sh/ruff/) (format and lint), [ty](https://docs.astral.sh/ty/),
yamllint, [rumdl](https://github.com/rvben/rumdl) and [editorconfig-checker](https://editorconfig-checker.github.io). See [CLAUDE.md](CLAUDE.md) for the
project rules.

## AI assistant

The project only uses [Claude Code](https://claude.com/claude-code) as AI assistant. Its rules are in
[CLAUDE.md](CLAUDE.md), `tests/CLAUDE.md`, `website/CLAUDE.md` and the skills in `.claude/skills/`.

## Documentation

The documentation is a [Docusaurus](https://docusaurus.io) website in `website/` and needs Node.js.
The API reference is generated from the docstrings:

```bash
./scripts/docs.sh        # build
./scripts/docs.sh start  # live reload
```

## Tests

Tests use [pytest](https://docs.pytest.org). **100% test coverage is enforced**, so every new code path needs a test.

```bash
uv run pytest
```

Large expected values are stored as [syrupy](https://github.com/syrupy-project/syrupy) snapshots in `__snapshots__`
folders. After an intended change, update them and review the diff:

```bash
uv run pytest -n0 --snapshot-update
```

## Releases

Only maintainers create releases. Tags cannot be deleted, so a release must be correct before the tag is pushed.
The version comes from the tag ([setuptools-scm](https://setuptools-scm.readthedocs.io)), don't set it in a file.

1. Rename `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md) to `## [X.Y.Z] - YYYY-MM-DD` and add a new empty
   `## [Unreleased]` section above it. Pre-releases don't need a changelog section.
2. Merge the changes into `main`. Pre-releases are tagged on `develop` instead.
3. Run `./scripts/release.sh vX.Y.Z` from `main`, or `./scripts/release.sh vX.Y.ZbN` from `develop`.

`./scripts/release.sh` creates and pushes the tag only if `./scripts/check-release.sh` passes. The check verifies the
tag format and that stable releases have a changelog entry. The same check runs again in the release workflow before
anything is published on PyPI.

Don't create tags manually and don't use `git push --no-verify` for tags.

## Report bugs

Report a bug by [opening a new issue](https://github.com/superbox-dev/keba_keenergy_api/issues/new/choose).
Great bug reports tend to have:

- A quick summary and/or background
- Steps to reproduce (sample code if you can)
- What you expected would happen
- What actually happens
- The Web HMI software version and the device hardware name
- Debug logs (remove credentials first)
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## License

By contributing, you agree that your contributions will be licensed under the [Apache License][license].

[license]: https://github.com/superbox-dev/keba_keenergy_api/blob/main/LICENSE

<!--end-contributing-->
