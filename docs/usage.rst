Usage
=====

Environment setup
-----------------

The project uses a ``src``-layout package. Create and activate a local virtual environment:

.. code-block:: bash

   cd /mnt/c/Users/gpchatzitsompanis/Documents/CursorPython
   source .venv/bin/activate

Install the package in editable mode alongside the developer tooling:

.. code-block:: bash

   pip install --upgrade pip
   pip install -e ".[dev]"

Running the CLI
---------------

Once installed, the executable ``cursor-python`` is available on your ``PATH``:

.. code-block:: bash

   cursor-python --help

Example run:

.. code-block:: bash

   cursor-python --count 5 --seed 123 --output-format text

Arguments
~~~~~~~~~

``--count`` (``-n``)
    Number of random circles to generate. Must be a non-negative integer.
``--min-radius`` / ``--max-radius``
    Inclusive bounds for generated radii.
``--seed``
    Optional seed to make runs reproducible.
``--log-level``
    Logging level for the run (DEBUG, INFO, WARNING, ERROR, CRITICAL).
``--log-format``
    Choose ``text`` (default) or ``json`` structured logs.
``--output-format``
    Render the report as ``text`` (logged) or ``json`` (printed to stdout).
``--config``
    Path to a ``cursor-python.toml`` file that stores defaults.

Expected output
~~~~~~~~~~~~~~~

The CLI logs the generated circles, their areas and circumferences, and reports the largest
circle by area. Execution duration is logged via the ``log_execution_time`` decorator. When
``--output-format json`` is supplied the full summary is printed as a JSON document, which is
useful for scripting or piping into ``jq``.

Configuration cascade
~~~~~~~~~~~~~~~~~~~~~

Settings are resolved in the following order (later sources override earlier ones):

1. ``cursor-python.toml`` (or ``cursor_python.toml``) if present in the working directory.
2. Environment variables prefixed with ``CURSOR_PYTHON_`` (for example ``CURSOR_PYTHON_COUNT=3``).
3. CLI arguments passed to ``cursor-python``.

Building the documentation
--------------------------

Use the provided ``Makefile`` inside ``docs``:

.. code-block:: bash

   cd docs
   make html

The generated HTML documentation will be located in ``docs/_build/html``.

