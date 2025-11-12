from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:  # pragma: no cover - exercised indirectly during runtime
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[assignment]

ENV_PREFIX = "CURSOR_PYTHON_"
DEFAULT_CONFIG_FILENAMES = ("cursor-python.toml", "cursor_python.toml")


@dataclass(frozen=True, slots=True)
class Settings:
    """Configuration values derived from args, env vars, and config files."""

    count: int = 5
    min_radius: float = 1.0
    max_radius: float = 10.0
    seed: int | None = None
    log_level: str = "INFO"
    log_format: str = "text"
    output_format: str = "text"


def load_from_mapping(mapping: Mapping[str, Any]) -> dict[str, Any]:
    """Normalise a mapping with user-provided configuration values."""
    normalised: dict[str, Any] = {}
    for key, value in mapping.items():
        normalised[key.replace("-", "_").lower()] = value
    return normalised


def load_from_env(environ: Mapping[str, str] | None = None) -> dict[str, Any]:
    """Pull configuration from the environment with the project prefix."""
    environ = environ or os.environ
    collected: dict[str, Any] = {}
    for key, value in environ.items():
        if not key.startswith(ENV_PREFIX):
            continue
        option = key[len(ENV_PREFIX) :].lower()
        collected[option] = value
    return collected


def load_from_file(path: Path) -> dict[str, Any]:
    """Load configuration from a TOML file."""
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    return load_from_mapping(data.get("cursor_python", data))


def find_default_config(start_dir: Path | None = None) -> Path | None:
    """Search for a default config file relative to a directory."""
    start = start_dir or Path.cwd()
    for candidate in DEFAULT_CONFIG_FILENAMES:
        config_path = start / candidate
        if config_path.is_file():
            return config_path
    return None


def coerce_types(raw: Mapping[str, Any], base: Settings) -> Settings:
    """Coerce raw values (strings) into their expected types."""
    def pick(name: str, cast, default):
        if name not in raw:
            return default
        value = raw[name]
        if isinstance(default, bool):
            lower = str(value).lower()
            if lower in {"1", "true", "yes", "on"}:
                return True
            if lower in {"0", "false", "no", "off"}:
                return False
        try:
            return cast(value) if value is not None else None
        except (TypeError, ValueError) as exc:  # pragma: no cover
            raise ValueError(f"Invalid value for option '{name}': {value!r}") from exc

    return Settings(
        count=pick("count", int, base.count),
        min_radius=pick("min_radius", float, base.min_radius),
        max_radius=pick("max_radius", float, base.max_radius),
        seed=pick("seed", int, base.seed),
        log_level=str(raw.get("log_level", base.log_level)).upper(),
        log_format=str(raw.get("log_format", base.log_format)).lower(),
        output_format=str(raw.get("output_format", base.output_format)).lower(),
    )


def merge_settings(
    *sources: Mapping[str, Any],
    base: Settings | None = None,
) -> Settings:
    """Merge multiple configuration sources with precedence."""
    merged: dict[str, Any] = {}
    for source in sources:
        merged.update(load_from_mapping(source))
    return coerce_types(merged, base or Settings())

