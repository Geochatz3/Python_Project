from __future__ import annotations

"""Public package interface for the Cursor Python Project."""

from .cli import Settings, configure_logging, console_main, main, parse_args, run_demo
from .core import Circle, CircleSummary, format_circle_stats, generate_random_circles, summarize_circles
from .version import __version__

__all__ = [
    "__version__",
    "Circle",
    "CircleSummary",
    "Settings",
    "configure_logging",
    "console_main",
    "format_circle_stats",
    "generate_random_circles",
    "main",
    "parse_args",
    "run_demo",
    "summarize_circles",
]

