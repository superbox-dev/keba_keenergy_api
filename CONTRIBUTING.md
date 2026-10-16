# Contributing

<!--start-contributing-->

## Guidelines

Contributing to this project should be as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features

## Getting started

Set up the project with `./scripts/setup.sh`.

## GitHub is used for everything

GitHub is used to host code, to track issues and feature requests, as well as accept pull requests.

Pull requests are the best way to propose changes to the codebase.

1. Fork the repo and create your branch from `develop`
2. If you've changed something, update the documentation and add an entry under `[Unreleased]` in the
   `CHANGELOG.md`.
3. Make sure your code lints with `./scripts/lint.sh`.
4. Test your contribution.
5. Issue that pull request!

## Report bugs using Github's [issues](https://github.com/superbox-dev/keba_keenergy_api/issues)

GitHub issues are used to track public bugs.
Report a bug by [opening a new issue](https://github.com/superbox-dev/keba_keenergy_api/issues/new/choose);
it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

People *love* thorough bug reports. I'm not even kidding.

## Use a Consistent Coding Style

Use [ruff](https://docs.astral.sh/ruff/) for formatting and linting and [ty](https://docs.astral.sh/ty/)
for type checking. Run all linters at once with:

```bash
./scripts/lint.sh
```

## Test your code modification

To test the code we use [pytest](https://docs.pytest.org):

```bash
uv run pytest
```

The test coverage must stay at 100%, so every new code path needs a test.

## License

By contributing, you agree that your contributions will be licensed under its [Apache License][license].

[license]: https://github.com/superbox-dev/keba_keenergy_api/blob/main/LICENSE

<!--end-contributing-->
