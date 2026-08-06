"""Pure geometry helpers for Witch Tools Guided Align.

This module intentionally has no Blender imports so its constraint math can be
unit-tested without launching Blender.
"""

from __future__ import annotations

import math
from typing import Iterable, Sequence

_EPS = 1.0e-12


def _v3(value: Sequence[float]) -> tuple[float, float, float]:
    if len(value) != 3:
        raise ValueError("Expected a 3D vector")
    return (float(value[0]), float(value[1]), float(value[2]))


def add(a: Sequence[float], b: Sequence[float]) -> tuple[float, float, float]:
    a = _v3(a)
    b = _v3(b)
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Sequence[float], b: Sequence[float]) -> tuple[float, float, float]:
    a = _v3(a)
    b = _v3(b)
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def mul(a: Sequence[float], scalar: float) -> tuple[float, float, float]:
    a = _v3(a)
    scalar = float(scalar)
    return (a[0] * scalar, a[1] * scalar, a[2] * scalar)


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    a = _v3(a)
    b = _v3(b)
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Sequence[float], b: Sequence[float]) -> tuple[float, float, float]:
    a = _v3(a)
    b = _v3(b)
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def length(a: Sequence[float]) -> float:
    return math.sqrt(dot(a, a))


def normalized(a: Sequence[float], *, epsilon: float = _EPS) -> tuple[float, float, float]:
    a = _v3(a)
    size = length(a)
    if size <= epsilon:
        raise ValueError("Direction has zero length")
    return mul(a, 1.0 / size)


def median_point(points: Iterable[Sequence[float]]) -> tuple[float, float, float]:
    values = [_v3(point) for point in points]
    if not values:
        raise ValueError("At least one point is required")
    count = float(len(values))
    return (
        sum(point[0] for point in values) / count,
        sum(point[1] for point in values) / count,
        sum(point[2] for point in values) / count,
    )


def build_frame(
    origin: Sequence[float],
    endpoint: Sequence[float],
) -> tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]:
    """Return origin and a stable right-handed orthonormal XYZ basis.

    Custom X follows origin -> endpoint. The helper chooses the least-parallel
    world axis as a seed, preventing the custom frame from collapsing when the
    guide points close to world X, Y, or Z.
    """

    origin = _v3(origin)
    x_axis = normalized(sub(endpoint, origin))
    world_axes = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    seed = min(world_axes, key=lambda axis: abs(dot(axis, x_axis)))
    z_axis = normalized(cross(x_axis, seed))
    y_axis = normalized(cross(z_axis, x_axis))
    return origin, x_axis, y_axis, z_axis


def to_frame(
    point: Sequence[float],
    frame: Sequence[Sequence[float]],
) -> tuple[float, float, float]:
    origin, x_axis, y_axis, z_axis = frame
    relative = sub(point, origin)
    return (dot(relative, x_axis), dot(relative, y_axis), dot(relative, z_axis))


def from_frame(
    point: Sequence[float],
    frame: Sequence[Sequence[float]],
) -> tuple[float, float, float]:
    origin, x_axis, y_axis, z_axis = frame
    point = _v3(point)
    return add(
        origin,
        add(mul(x_axis, point[0]), add(mul(y_axis, point[1]), mul(z_axis, point[2]))),
    )


def match_components(
    point: Sequence[float],
    reference: Sequence[float],
    mask: Sequence[bool],
) -> tuple[float, float, float]:
    point = _v3(point)
    reference = _v3(reference)
    if len(mask) != 3:
        raise ValueError("Expected a three-axis mask")
    return tuple(reference[index] if bool(mask[index]) else point[index] for index in range(3))


def component_delta(
    point: Sequence[float],
    reference: Sequence[float],
    mask: Sequence[bool],
) -> tuple[float, float, float]:
    return sub(match_components(point, reference, mask), point)


def solve_slide_parameter(
    point: Sequence[float],
    direction: Sequence[float],
    reference: Sequence[float],
    mask: Sequence[bool],
    *,
    tolerance: float = 1.0e-6,
) -> float:
    """Solve p + t*d so enabled components match the reference.

    Multiple enabled components are valid only when they resolve to the same t.
    This catches impossible rail/axis combinations before any geometry moves.
    """

    point = _v3(point)
    direction = normalized(direction)
    reference = _v3(reference)
    if len(mask) != 3 or not any(bool(value) for value in mask):
        raise ValueError("Enable at least one alignment component")

    solutions: list[float] = []
    for index, enabled in enumerate(mask):
        if not enabled:
            continue
        difference = reference[index] - point[index]
        component = direction[index]
        if abs(component) <= _EPS:
            if abs(difference) > tolerance:
                raise ValueError("Captured rail cannot change one of the requested components")
            continue
        solutions.append(difference / component)

    if not solutions:
        return 0.0

    result = sum(solutions) / len(solutions)
    allowed = max(tolerance, tolerance * max(1.0, abs(result)))
    if any(abs(value - result) > allowed for value in solutions):
        raise ValueError("Requested components do not intersect the captured rail at one point")
    return result


def line_extent(
    points: Iterable[Sequence[float]],
    origin: Sequence[float],
    direction: Sequence[float],
) -> tuple[float, float, float]:
    """Return min/max projected distance and max perpendicular deviation."""

    values = [_v3(point) for point in points]
    if not values:
        raise ValueError("At least one rail point is required")
    origin = _v3(origin)
    direction = normalized(direction)
    projections: list[float] = []
    max_deviation = 0.0
    for point in values:
        relative = sub(point, origin)
        projection = dot(relative, direction)
        projections.append(projection)
        nearest = mul(direction, projection)
        max_deviation = max(max_deviation, length(sub(relative, nearest)))
    return min(projections), max(projections), max_deviation
