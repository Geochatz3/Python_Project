from __future__ import annotations

import json
import math
import random
from pathlib import Path

import pytest

from cursor_python import (
    Circle,
    Settings,
    format_circle_stats,
    generate_random_circles,
    main,
    run_demo,
)


def test_circle_area_and_circumference() -> None:
    circle = Circle(radius=2.0)
    assert circle.area() == pytest.approx(math.pi * 4.0)
    assert circle.circumference() == pytest.approx(2 * math.pi * 2.0)


def test_generate_random_circles_reproducible_seed() -> None:
    rng = random.Random(42)
    circles = generate_random_circles(3, min_radius=1.0, max_radius=2.0, rng=rng)
    assert len(circles) == 3
    assert [circle.radius for circle in circles] == pytest.approx(
        [1.6394267985, 1.0250107552, 1.2750293184],
        rel=1e-9,
    )


def test_generate_random_circles_negative_count() -> None:
    with pytest.raises(ValueError):
        generate_random_circles(-1)


def test_generate_random_circles_invalid_radius_range() -> None:
    with pytest.raises(ValueError):
        generate_random_circles(1, min_radius=2.0, max_radius=1.0)


def test_format_circle_stats() -> None:
    circles = [Circle(radius=1.0), Circle(radius=2.0)]
    stats = format_circle_stats(circles)
    lines = stats.splitlines()
    assert lines[0].startswith("01.")
    assert "Circle(radius=1.00)" in lines[0]
    assert lines[1].startswith("02.")


def test_run_demo_returns_summary(caplog) -> None:
    caplog.set_level("INFO")
    settings = Settings(count=2, seed=7)
    summary = run_demo(settings)
    assert len(summary.circles) == 2
    assert any("Generated 2 circles" in message for message in caplog.messages)


def test_main_invocation_success(monkeypatch, caplog) -> None:
    caplog.set_level("INFO")
    monkeypatch.setattr(
        "sys.argv",
        [
            "cursor-python",
            "--count",
            "2",
            "--seed",
            "1",
            "--min-radius",
            "1.0",
            "--max-radius",
            "1.0",
        ],
    )
    exit_code = main()
    assert exit_code == 0
    assert any("Generated 2 circles" in message for message in caplog.messages)


def test_main_json_output(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["cursor-python", "--count", "1", "--seed", "1234", "--output-format", "json"],
    )
    exit_code = main()
    assert exit_code == 0
    captured = capsys.readouterr().out
    payload = json.loads(captured)
    assert payload["count"] == 1
    assert payload["largest"]["radius"] == pytest.approx(payload["circles"][0]["radius"])


def test_main_reads_config_file(monkeypatch, tmp_path: Path) -> None:
    config_path = tmp_path / "cursor-python.toml"
    config_path.write_text(
        """
        [cursor_python]
        count = 1
        seed = 99
        output_format = "json"
        """,
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "sys.argv",
        ["cursor-python", "--config", str(config_path)],
    )
    exit_code = main()
    assert exit_code == 0


def test_environment_overrides(monkeypatch) -> None:
    monkeypatch.setenv("CURSOR_PYTHON_COUNT", "0")
    monkeypatch.setattr("sys.argv", ["cursor-python"])
    exit_code = main()
    assert exit_code == 0

