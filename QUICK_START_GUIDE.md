# Quick Start: Pre-commit & Coverage

## 🚀 Setup Pre-commit Hooks (One-Time)

```bash
# 1. Install pre-commit (if not already installed)
pip install pre-commit

# 2. Install the hooks into your git repository
pre-commit install

# That's it! Now hooks run automatically on every commit
```

### Test It Out

```bash
# Create a test file with issues
echo "def test():    " > test_file.py  # trailing whitespace
echo "    print('hello')" >> test_file.py

# Try to commit it
git add test_file.py
git commit -m "test commit"

# Watch pre-commit:
# ✅ Automatically removes trailing whitespace
# ✅ Formats code with black
# ✅ Runs ruff linting
# ✅ Then commits successfully!
```

## 📊 Run Test Coverage

```bash
# 1. Install coverage tools (if needed)
pip install pytest-cov

# 2. Run tests with coverage
pytest --cov=src/cursor_python --cov-report=term-missing

# 3. Generate HTML report
pytest --cov=src/cursor_python --cov-report=html

# 4. Open the report
# Linux/Mac:
open htmlcov/index.html
# Windows:
start htmlcov/index.html
```

### What You'll See

**Terminal Output:**
```
tests/test_main.py ..........                                            [100%]

---------- coverage: platform linux, python 3.10.12 -----------
Name                              Stmts   Miss  Cover   Missing
----------------------------------------------------------------
src/cursor_python/__init__.py        12      0   100%
src/cursor_python/cli.py            150     10    93%   45-50, 120-125
src/cursor_python/config.py          80      5    94%   60-65
src/cursor_python/core.py           100      2    98%   55, 78
----------------------------------------------------------------
TOTAL                               342     17    95%
```

**HTML Report:**
- Green background = covered ✅
- Red background = not covered ❌
- Click on any file to see line-by-line coverage

## 💡 Real-World Example

### Scenario: Adding a New Feature

```bash
# 1. Create feature branch
git checkout -b feature/new-function

# 2. Write code
# Edit src/cursor_python/core.py

# 3. Stage changes
git add src/cursor_python/core.py

# 4. Try to commit
git commit -m "add new function"

# Pre-commit runs:
# - Removes trailing whitespace ✅
# - Formats with black ✅
# - Lints with ruff ✅
# - If all pass, commit succeeds! ✅

# 5. Write tests
# Edit tests/test_main.py

# 6. Run tests with coverage
pytest --cov=src/cursor_python --cov-report=html

# 7. Check coverage report
# Open htmlcov/index.html
# See if your new function is covered (green) ✅

# 8. If coverage is low, add more tests
# Edit tests/test_main.py

# 9. Commit everything
git add tests/test_main.py
git commit -m "add tests for new function"
# Pre-commit runs again automatically ✅
```

## 🎯 Common Commands

### Pre-commit
```bash
# Run hooks manually on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files

# Update hook versions
pre-commit autoupdate
```

### Coverage
```bash
# Quick coverage check
pytest --cov=src/cursor_python

# Detailed coverage with missing lines
pytest --cov=src/cursor_python --cov-report=term-missing

# HTML report
pytest --cov=src/cursor_python --cov-report=html

# Only show files below threshold
pytest --cov=src/cursor_python --cov-fail-under=80
```

## ❓ Troubleshooting

### Pre-commit not running?
```bash
# Check if installed
pre-commit --version

# Reinstall hooks
pre-commit uninstall
pre-commit install
```

### Coverage not showing?
```bash
# Install pytest-cov
pip install pytest-cov

# Verify installation
pytest --version
```

### Want to skip hooks once?
```bash
# Not recommended, but sometimes needed
git commit --no-verify -m "emergency fix"
```
