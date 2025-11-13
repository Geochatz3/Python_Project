# Cursor Python Project

[![CI](https://github.com/Geochatz3/Python_Project/actions/workflows/ci.yml/badge.svg)](https://github.com/Geochatz3/Python_Project/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A well-structured Python CLI tool that demonstrates modern Python development practices. Generate random circles, calculate geometric properties, and configure behavior through multiple sources.

## Features

- ✅ **Modern Python practices**: Type hints, dataclasses, `src`-layout package
- ✅ **Flexible configuration**: TOML files, environment variables, and CLI arguments
- ✅ **Structured output**: Text or JSON formats for human/automation use
- ✅ **Deterministic generation**: Seed support for reproducible runs
- ✅ **Comprehensive testing**: pytest with coverage reporting
- ✅ **Full documentation**: Sphinx-generated docs
- ✅ **CI/CD**: Automated testing across Python 3.10-3.12
- ✅ **Code quality**: Linting (ruff) and formatting (black)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Geochatz3/Python_Project.git
cd Python_Project

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install --upgrade pip
pip install -e ".[dev]"

# Run the CLI
cursor-python --help
```

### Basic Usage

```bash
# Generate 5 random circles (default)
cursor-python

# Generate 10 circles with a specific seed
cursor-python --count 10 --seed 42

# Output as JSON for automation
cursor-python --count 5 --output-format json

# Custom radius range
cursor-python --count 3 --min-radius 2.0 --max-radius 5.0
```

## Configuration

Runtime options can be supplied via (highest precedence last):

1. **TOML config file**: `cursor-python.toml` or `cursor_python.toml` in the project root
   - See `cursor-python.toml.example` for a template
2. **Environment variables**: Prefixed with `CURSOR_PYTHON_`
   - Example: `CURSOR_PYTHON_COUNT=3 cursor-python`
3. **CLI arguments**: Direct command-line options
   - Example: `cursor-python --count 3 --seed 42`

### Example Configuration File

```toml
[cursor_python]
count = 10
min_radius = 1.0
max_radius = 10.0
seed = 42
log_level = "INFO"
log_format = "text"
output_format = "json"
```

## Development

### Setup

```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/cursor_python --cov-report=html

# Run specific test file
pytest tests/test_main.py
```

### Code Quality

```bash
# Format code
black src tests

# Lint code
ruff check src tests

# Auto-fix lint issues
ruff check src tests --fix
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Building Documentation

```bash
cd docs
make html
# Open docs/_build/html/index.html in your browser
```

## Project Structure

```
CursorPython/
├── src/
│   └── cursor_python/      # Main package
│       ├── __init__.py      # Public API
│       ├── cli.py           # Command-line interface
│       ├── config.py        # Configuration management
│       ├── core.py          # Domain logic
│       └── version.py        # Version info
├── tests/                   # Test suite
├── docs/                    # Sphinx documentation
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
├── pyproject.toml           # Project configuration
├── README.md                # This file
├── LICENSE                  # MIT License
└── CHANGELOG.md             # Version history
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Documentation

Full documentation is available in the `docs/` directory. Build it locally with:

```bash
cd docs && make html
```

Or view the generated HTML at `docs/_build/html/index.html`.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed list of changes.

