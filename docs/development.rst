Development
===========

Prerequisites
-------------

* Python 3.10 or newer (matches the required interpreter).
* ``pip`` for dependency management.
* ``tox`` is optional if you prefer isolated automation, but not required.

Environment setup
-----------------

Create a virtual environment and install the project in editable mode alongside developer tools:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -e ".[dev]"

Running tests
-------------

The unit and integration tests reside in ``tests/`` and are executed with
``pytest``:

.. code-block:: bash

   pytest

The suite verifies:

* geometric calculations on ``Circle``;
* input validation for ``generate_random_circles`` (including invalid radius ranges);
* JSON/text reporting behaviour for the CLI;
* configuration merging across files, environment variables, and CLI flags.

Static analysis
---------------

The ``pyproject.toml`` configures common quality gates:

* ``ruff`` for linting and import sorting.
* ``mypy`` in ``strict`` mode for type checking.
* ``black`` for formatting (configures line length but is not run automatically).

Run them manually when making substantial edits:

.. code-block:: bash

   ruff check src tests
   mypy
   black --check src tests

Coding standards
----------------

* Use type hints for new functions and dataclasses.
* Raise explicit exceptions for invalid inputs rather than returning ``None``.
* Prefer dependency-injected randomness for deterministic tests when extending
  the codebase.
* Keep logging user-friendly—log actionable errors and retain structured
  ``INFO`` messages for routine flows.

Documentation workflow
----------------------

After updating code or docstrings, rebuild the docs:

.. code-block:: bash

   cd docs
   make html

Open ``docs/_build/html/index.html`` in a browser to review the output.

Continuous integration
----------------------

A GitHub Actions workflow (``.github/workflows/ci.yml``) installs dependencies, runs the test
suite, performs linting/type checking, and ensures the Sphinx docs still build. Extend it with
deployment steps (for example publishing documentation artifacts) when you are ready.

