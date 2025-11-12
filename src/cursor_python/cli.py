from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .config import (
    Settings,
    find_default_config,
    load_from_env,
    load_from_file,
    merge_settings,
)
from .core import CircleSummary, format_circle_stats, generate_random_circles, summarize_circles
from .version import __version__

LOG = logging.getLogger(__name__)
LOG_FORMAT_CHOICES = ("text", "json")
OUTPUT_FORMAT_CHOICES = ("text", "json")
LOG_LEVEL_CHOICES = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


class JsonFormatter(logging.Formatter):
    """Simple JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Generate random circles and inspect their statistics.",
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        help="Number of random circles to generate.",
    )
    parser.add_argument(
        "--min-radius",
        dest="min_radius",
        type=float,
        help="Minimum radius for generated circles.",
    )
    parser.add_argument(
        "--max-radius",
        dest="max_radius",
        type=float,
        help="Maximum radius for generated circles.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Seed for the random number generator (enables reproducible runs).",
    )
    parser.add_argument(
        "--log-level",
        choices=LOG_LEVEL_CHOICES,
        help="Set logging verbosity.",
    )
    parser.add_argument(
        "--log-format",
        choices=LOG_FORMAT_CHOICES,
        help="Choose between human-readable or JSON log output.",
    )
    parser.add_argument(
        "--output-format",
        choices=OUTPUT_FORMAT_CHOICES,
        help="Render the summary as text or JSON.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to a TOML configuration file.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments."""
    return build_parser().parse_args(argv)


def _collect_cli_overrides(namespace: argparse.Namespace) -> dict[str, Any]:
    raw = {
        key: value
        for key, value in vars(namespace).items()
        if value is not None and key != "config"
    }
    return raw


def _load_settings(namespace: argparse.Namespace) -> Settings:
    config_path = namespace.config or find_default_config()
    sources: list[dict[str, Any]] = []
    if config_path:
        sources.append(load_from_file(config_path))
    sources.append(load_from_env())
    sources.append(_collect_cli_overrides(namespace))
    return _validate_settings(merge_settings(*sources, base=Settings()))


def _validate_settings(options: Settings) -> Settings:
    if options.log_format not in LOG_FORMAT_CHOICES:
        raise ValueError(f"Unsupported log format '{options.log_format}'")
    if options.output_format not in OUTPUT_FORMAT_CHOICES:
        raise ValueError(f"Unsupported output format '{options.output_format}'")
    if options.count < 0:
        raise ValueError("count must be non-negative")
    return options


def configure_logging(level: str, log_format: str) -> None:
    """Configure application logging."""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level, logging.INFO))

    formatter: logging.Formatter
    if log_format == "json":
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    has_stream_handler = any(
        isinstance(handler, logging.StreamHandler)
        for handler in root_logger.handlers
    )
    if not has_stream_handler:
        root_logger.addHandler(logging.StreamHandler())

    for handler in root_logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setFormatter(formatter)


def log_execution_time(func):
    """Decorator that logs the execution time of the wrapped function."""

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        LOG.info("Function '%s' executed in %.4fs", func.__name__, duration)
        return result

    return wrapper


@log_execution_time
def run_demo(settings: Settings | int) -> CircleSummary:
    """Generate circles, log their stats, and return a summary."""
    options = settings if isinstance(settings, Settings) else Settings(count=settings)

    rng = None
    if options.seed is not None:
        rng = random_with_seed(options.seed)

    circles = generate_random_circles(
        options.count,
        min_radius=options.min_radius,
        max_radius=options.max_radius,
        rng=rng,
    )

    summary = summarize_circles(circles)

    if not summary.circles:
        LOG.warning("No circles generated.")
        return summary

    LOG.info(
        "Generated %d circles within radius range %.2f..%.2f",
        len(summary.circles),
        options.min_radius,
        options.max_radius,
    )
    LOG.debug("Runtime options: %s", json.dumps(asdict(options)))

    return summary


def random_with_seed(seed: int):
    """Create a random generator with a dedicated seed."""
    import random

    return random.Random(seed)


def _emit_summary(summary: CircleSummary, settings: Settings) -> None:
    if settings.output_format == "json":
        print(json.dumps(summary.as_dict(), indent=2))
        return

    if summary.circles:
        LOG.info("Circle statistics:\n%s", format_circle_stats(summary.circles))
        if summary.largest:
            LOG.info(
                "Largest circle: %s (area=%.2f, circumference=%.2f)",
                summary.largest,
                summary.largest.area(),
                summary.largest.circumference(),
            )
    else:
        LOG.info("Nothing to report.")


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point for CLI usage."""
    try:
        namespace = parse_args(argv)
        settings = _load_settings(namespace)
    except FileNotFoundError as exc:
        LOG.error("Config file not found: %s", exc)
        return 2
    except ValueError as exc:
        LOG.error("Invalid configuration: %s", exc)
        return 2

    configure_logging(settings.log_level, settings.log_format)

    try:
        summary = run_demo(settings)
    except ValueError as exc:
        LOG.error("Failed to generate circles: %s", exc)
        return 1

    _emit_summary(summary, settings)
    return 0


def console_main() -> None:
    """Console script entry point."""
    sys.exit(main())

