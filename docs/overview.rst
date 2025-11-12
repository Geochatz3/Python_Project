Overview
========

The Cursor Python Project is a compact command-line tool that showcases how to:

* model geometric data with dataclasses;
* apply structured logging, timing decorators, and layered configuration;
* ship a production-ready entry point with clear exit codes; and
* back the implementation with automated tests and documentation.

High-level architecture
-----------------------

The codebase follows a `src`-layout package called ``cursor_python``. The key modules are:

``cursor_python.core``
    An immutable dataclass that exposes ``area`` and ``circumference`` helpers
    and produces a friendly string representation. It also offers helpers such as
    ``generate_random_circles`` and ``summarize_circles`` for deterministic data generation.

``cursor_python.config``
    A thin layer that merges configuration from TOML files, environment variables, and CLI
    arguments into a single ``Settings`` dataclass.

``cursor_python.cli``
    Houses the command-line interface, logging configuration, and the ``run_demo`` workflow.
    It exposes a ``cursor-python`` console script via ``pyproject.toml`` while keeping the API
    importable for other applications.

``main.py``
    Remains as a compatibility shim for direct execution but forwards to the package API.

The CLI orchestrates the workflow by generating sample data, formatting statistics, and
highlighting the largest circle by area. The ``log_execution_time`` decorator reports
execution duration, and structured logging can emit either plain text or JSON payloads.

``main()``
    Implements the CLI entry point. It parses arguments, configures logging, and returns an
    explicit exit code while converting domain errors into actionable log
    messages.

Project goals
-------------

The repository is meant to serve as a starter template for:

* experimenting with Cursor-assisted development workflows;
* demonstrating best practices (type hints, logging, packaging, unit tests, documentation);
* providing hooks for CI/CD pipelines, type checking, and code quality automation.

If you extend the project, update this overview to reflect new modules or
responsibilities.

