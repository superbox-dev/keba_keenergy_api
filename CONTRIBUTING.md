# Contributing

Thank you for investing your time in contributing to **KEBA KeEnergy API**.

## Setting up an environment

Clone the `KEBA-KeEnergy-API` repository.
Inside the repository, create a virtual environment:

```bash
uv sync --locked --all-extras --dev
```

## Testing

To test the code we use [pytest](https://docs.pytest.org):

```bash
uv run pytest -n auto
```

## Making a pull request

When you're finished with the changes, create a pull request, also known as a PR.
The branch to contribute is `main`. Please also update the [CHANGELOG.md](CHANGELOG.md) with your changes.
