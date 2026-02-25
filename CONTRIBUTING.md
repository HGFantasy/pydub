# Contributing

This is a community-maintained fork of [jiaaro/pydub](https://github.com/jiaaro/pydub).
We welcome pull requests for features, bug fixes, documentation, tests, and
anything else that makes pydub better.

## How to contribute

1. Fork [this repository](https://github.com/HGFantasy/pydub)
2. Create a feature branch
3. Make your changes
4. Run the tests and linter (see below)
5. Open a Pull Request

## Development setup

```bash
git clone https://github.com/HGFantasy/pydub.git
cd pydub
pip install -e ".[dev]"
```

## Running tests and lint

```bash
# Tests
python test/test.py

# Lint (must pass cleanly)
ruff check pydub/
```

## Guidelines

1. **Maintain backward compatibility** with the upstream pydub API
2. **Include tests** and make sure all 113+ tests pass
3. **Lint must pass** — run `ruff check pydub/` before submitting
4. Write a short description of **what** changed and **why**
5. Keep PRs small and focused on a single change

## Upstream contributions

If your change is relevant to the original project as well, consider also
opening a PR against [jiaaro/pydub](https://github.com/jiaaro/pydub).
