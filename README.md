# Cursor Python Project

Cursor Python Project is a small, documented command-line tool that showcases a modern Python
workflow:

- `src`-layout package with a reusable API and an installable `cursor-python` script.
- Deterministic random data generation with configurable radius boundaries.
- Structured logging (`text` or `json`) and optional JSON summaries for automation.
- Sphinx documentation and a growing test suite powered by `pytest`.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
cursor-python --help
```

## Configuration sources

Runtime options can be supplied via (highest precedence last):

1. `cursor-python.toml` (or `cursor_python.toml`)
2. Environment variables prefixed with `CURSOR_PYTHON_` (for example `CURSOR_PYTHON_COUNT=3`)
3. CLI arguments such as `--count`, `--seed`, `--output-format json`

Consult `docs/usage.rst` for a full rundown of examples.

