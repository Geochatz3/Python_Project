# Contributing to Cursor Python Project

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/Python_Project.git
   cd Python_Project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install in development mode**
   ```bash
   pip install --upgrade pip
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes**
   - Write clear, documented code
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed

3. **Run quality checks**
   ```bash
   # Format code
   black src tests
   
   # Lint code
   ruff check src tests
   
   # Run tests
   pytest
   
   # Check coverage
   pytest --cov=src/cursor_python --cov-report=term-missing
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```
   
   Pre-commit hooks will run automatically. If they fail, fix the issues and commit again.

## Code Style

- **Formatting**: We use `black` with 100 character line length
- **Linting**: We use `ruff` with strict rules
- **Type hints**: Use type hints for all function signatures
- **Docstrings**: Follow NumPy-style docstrings (as configured in Sphinx)

## Testing

- Write tests for all new features
- Aim for high test coverage
- Tests should be fast and isolated
- Use descriptive test names

## Documentation

- Update `README.md` if adding new features
- Update `CHANGELOG.md` with your changes
- Update docstrings for new functions/classes
- Rebuild docs to verify: `cd docs && make html`

## Submitting Changes

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request**
   - Use a clear, descriptive title
   - Describe what changes you made and why
   - Reference any related issues
   - Ensure all CI checks pass

3. **Respond to feedback**
   - Be open to suggestions
   - Make requested changes promptly
   - Keep discussions constructive

## Code Review Process

- All PRs require review before merging
- Maintainers will review within a few days
- Address review comments in new commits
- Squash commits before merging (if requested)

## Questions?

Feel free to open an issue for questions or discussions about the project.

Thank you for contributing! 🎉

