from __future__ import annotations

import math
import random
from collections.abc import Iterable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Circle:
    """Represent a mathematical circle with a radius."""

    radius: float

    def area(self) -> float:
        """Return the area of the circle."""
        return math.pi * self.radius**2

    def circumference(self) -> float:
        """Return the circumference of the circle."""
        return 2 * math.pi * self.radius

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"Circle(radius={self.radius:.2f})"


def generate_random_circles(
    count: int,
    *,
    min_radius: float = 1.0,
    max_radius: float = 10.0,
    rng: random.Random | None = None,
) -> list[Circle]:
    """Return a list of circles with random radii."""
    if count < 0:
        raise ValueError("count must be non-negative")
    if min_radius < 0:
        raise ValueError("min_radius must be non-negative")
    if max_radius <= 0:
        raise ValueError("max_radius must be greater than zero")
    if min_radius > max_radius:
        raise ValueError("min_radius cannot be greater than max_radius")

    random_generator = rng or random.Random()
    return [
        Circle(random_generator.uniform(min_radius, max_radius))
        for _ in range(count)
    ]


def format_circle_stats(circles: Iterable[Circle]) -> str:
    """Return a formatted table of circle statistics."""
    lines: list[str] = []
    for idx, circle in enumerate(circles, 1):
        lines.append(
            (
                f"{idx:02d}. {circle}: area={circle.area():.2f}, "
                f"circumference={circle.circumference():.2f}"
            )
        )
    return "\n".join(lines)


@dataclass(frozen=True, slots=True)
class CircleSummary:
    """Statistics that describe a collection of circles."""

    circles: tuple[Circle, ...]
    largest: Circle | None
    total_area: float
    average_radius: float | None
    min_radius: float | None
    max_radius: float | None

    def as_dict(self) -> dict[str, float | int | list[dict[str, float]] | None]:
        """Return the summary as a JSON-serialisable dictionary."""
        return {
            "count": len(self.circles),
            "total_area": self.total_area,
            "average_radius": self.average_radius,
            "min_radius": self.min_radius,
            "max_radius": self.max_radius,
            "largest": None
            if self.largest is None
            else {
                "radius": self.largest.radius,
                "area": self.largest.area(),
                "circumference": self.largest.circumference(),
            },
            "circles": [
                {
                    "radius": circle.radius,
                    "area": circle.area(),
                    "circumference": circle.circumference(),
                }
                for circle in self.circles
            ],
        }


def summarize_circles(circles: Sequence[Circle]) -> CircleSummary:
    """Build a high-level summary of the provided circles."""
    sequence = tuple(circles)
    if not sequence:
        return CircleSummary(
            circles=sequence,
            largest=None,
            total_area=0.0,
            average_radius=None,
            min_radius=None,
            max_radius=None,
        )

    total_area = sum(circle.area() for circle in sequence)
    average_radius = sum(circle.radius for circle in sequence) / len(sequence)
    largest = max(sequence, key=lambda circle: circle.area())
    min_radius = min(circle.radius for circle in sequence)
    max_radius = max(circle.radius for circle in sequence)

    return CircleSummary(
        circles=sequence,
        largest=largest,
        total_area=total_area,
        average_radius=average_radius,
        min_radius=min_radius,
        max_radius=max_radius,
    )

