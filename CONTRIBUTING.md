# Contributing

Thank you for your interest in contributing to the Hypersender Python SDK.

## Reporting issues

Open an issue on GitHub with a clear title, steps to reproduce, expected and actual behavior, and your Python and `hypersender` versions (`python -c "import hypersender, sys; print(sys.version, hypersender.__version__)"`).

## Pull requests

1. Fork the repository and create a branch.
2. Set up a virtual environment and install the package with the dev tools:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e . pytest ruff
   ```

3. Make your change and add a test in `tests/`.
4. Make sure the checks pass:

   ```bash
   ruff check src tests
   ruff format --check src tests
   pytest
   ```

5. Open a pull request describing the change.

The SDK mirrors the [Hypersender API](https://docs.hypersender.com). New methods should follow the existing style: snake_case names, keyword arguments, and a plain dict as the return value.
