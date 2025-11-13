# Pre-commit Hooks & Test Coverage Guide

## 🔧 Pre-commit Hooks

### What Are Pre-commit Hooks?

Pre-commit hooks are **automated scripts that run before you commit code**. They act as a safety net to catch issues before they reach your repository.

Think of them as a **quality gate** that runs automatically every time you try to commit.

### How They Work

1. You write code and stage it: `git add .`
2. You try to commit: `git commit -m "my changes"`
3. **Pre-commit hooks run automatically** (if installed)
4. If hooks pass → commit succeeds ✅
5. If hooks fail → commit is blocked ❌ (you fix issues and try again)

### What Your Pre-commit Hooks Do

Looking at your `.pre-commit-config.yaml`, here's what runs:

#### 1. **Basic File Checks** (pre-commit-hooks)
- **trailing-whitespace**: Removes extra spaces at end of lines
- **end-of-file-fixer**: Ensures files end with a newline
- **check-yaml**: Validates YAML files (like your CI config)
- **check-json**: Validates JSON files
- **check-toml**: Validates TOML files (like pyproject.toml)
- **check-added-large-files**: Prevents accidentally committing huge files
- **check-merge-conflict**: Detects leftover merge conflict markers (`<<<<<<<`)
- **debug-statements**: Finds leftover `pdb.set_trace()` or `print()` statements

#### 2. **Code Linting** (ruff)
- **ruff**: Checks for code quality issues (like unused imports, style violations)
- **ruff-format**: Automatically formats code to match style rules
- Runs with `--fix` flag, so it **auto-fixes** many issues!

#### 3. **Code Formatting** (black)
- **black**: Automatically formats Python code to consistent style
- Ensures all code looks the same (indentation, spacing, etc.)

### Benefits

✅ **Catch errors early** - Before code reaches CI or teammates
✅ **Consistent code style** - Everyone's code looks the same
✅ **Save CI time** - Fix issues locally instead of waiting for CI to fail
✅ **Automatic fixes** - Many issues are fixed automatically
✅ **Team consistency** - Everyone follows the same rules

### Example Scenario

**Without pre-commit:**
```bash
# You write code with trailing whitespace
git add .
git commit -m "add feature"
git push
# CI fails because of linting errors
# You have to fix, commit again, push again
```

**With pre-commit:**
```bash
# You write code with trailing whitespace
git add .
git commit -m "add feature"
# Pre-commit automatically removes whitespace
# Pre-commit runs ruff and black
# Code is automatically formatted
# Commit succeeds on first try!
```

### Installation

```bash
# Install pre-commit (if not already installed)
pip install pre-commit

# Install the hooks (one-time setup)
pre-commit install

# Now hooks run automatically on every commit!
```

### Manual Usage

```bash
# Run hooks on all files (useful before pushing)
pre-commit run --all-files

# Run a specific hook
pre-commit run ruff --all-files

# Skip hooks for one commit (not recommended)
git commit --no-verify -m "emergency fix"
```

---

## 📊 Test Coverage

### What Is Test Coverage?

Test coverage measures **how much of your code is tested**. It shows which lines, functions, and branches are executed by your tests.

Think of it as a **report card** for your tests.

### Why It Matters

- **Find untested code**: See what parts of your codebase aren't tested
- **Prevent regressions**: More coverage = fewer bugs
- **Code quality**: High coverage often means better code quality
- **Confidence**: Know that your changes are tested

### How Coverage Works

1. **Run tests with coverage**: `pytest --cov=src/cursor_python`
2. **Coverage tool tracks**: Which lines of code were executed during tests
3. **Generate report**: Shows percentage covered and highlights missing areas

### Coverage Metrics

- **Line Coverage**: % of lines executed
- **Branch Coverage**: % of if/else branches tested
- **Function Coverage**: % of functions called
- **Statement Coverage**: % of statements executed

### Your Coverage Configuration

From your `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "-ra --cov=src/cursor_python --cov-report=term-missing --cov-report=html"
```

This means:
- `--cov=src/cursor_python`: Measure coverage for your package
- `--cov-report=term-missing`: Show missing lines in terminal
- `--cov-report=html`: Generate HTML report

### Reading Coverage Reports

#### Terminal Report
```
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
src/cursor_python/__init__.py        12      0   100%
src/cursor_python/cli.py            150     10    93%   45-50, 120-125
src/cursor_python/core.py             80      5    94%   60-65
---------------------------------------------------------------
TOTAL                               242     15    94%
```

- **Stmts**: Total statements
- **Miss**: Statements not covered
- **Cover**: Coverage percentage
- **Missing**: Line numbers not covered

#### HTML Report
- Open `htmlcov/index.html` in browser
- **Green lines**: Covered by tests ✅
- **Red lines**: Not covered ❌
- **Yellow lines**: Partially covered ⚠️

### Example: Improving Coverage

**Before:**
```python
# src/cursor_python/core.py
def generate_random_circles(count: int) -> list[Circle]:
    if count < 0:
        raise ValueError("count must be non-negative")  # ❌ Not tested
    return [Circle(random.uniform(1.0, 10.0)) for _ in range(count)]
```

**Test:**
```python
# tests/test_main.py
def test_generate_random_circles_negative_count():
    with pytest.raises(ValueError):
        generate_random_circles(-1)  # ✅ Now this line is covered!
```

**After running coverage:**
- Error handling line is now green ✅
- Coverage increased from 90% to 95%

### Coverage Best Practices

✅ **Aim for 80%+ coverage** (100% is often impractical)
✅ **Focus on critical paths** (business logic, error handling)
✅ **Don't test everything** (trivial getters/setters can be skipped)
✅ **Use coverage to find gaps**, not as a strict requirement
✅ **Review missing lines** to see if they need tests

### Running Coverage

```bash
# Run tests with coverage (terminal report)
pytest --cov=src/cursor_python --cov-report=term-missing

# Generate HTML report
pytest --cov=src/cursor_python --cov-report=html

# Open HTML report
# On Linux/Mac: open htmlcov/index.html
# On Windows: start htmlcov/index.html
```

### Coverage in CI

Your CI workflow now includes:
```yaml
- name: Run tests with coverage
  run: pytest --cov=src/cursor_python --cov-report=xml --cov-report=term
```

This:
- Runs tests with coverage
- Generates XML report (for Codecov integration)
- Shows terminal report in CI logs
- Can upload to Codecov for tracking over time

---

## 🎯 Summary

### Pre-commit Hooks
- **What**: Automated quality checks before commits
- **When**: Every `git commit`
- **Why**: Catch issues early, maintain consistency
- **How**: `pre-commit install` (one-time setup)

### Test Coverage
- **What**: Measure of how much code is tested
- **When**: During `pytest` runs
- **Why**: Find untested code, prevent bugs
- **How**: `pytest --cov=src/cursor_python --cov-report=html`

### Together They Provide
✅ **Quality assurance** at commit time (pre-commit)
✅ **Confidence** that code is tested (coverage)
✅ **Automation** that saves time and prevents errors
✅ **Professional standards** for open-source projects
