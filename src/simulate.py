"""Numerically integrate a toy logistic-growth ODE and emit a reproducible JSON record.

This is a numerical methods smoke test, not a validated cancer model.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def logistic_exact(t: float, x0: float, r: float, capacity: float) -> float:
    """Analytical logistic solution for positive x0, r, and capacity."""
    _validate(t, x0, r, capacity)
    if t < 0:
        raise ValueError("t must be >= 0")
    return capacity / (1.0 + ((capacity - x0) / x0) * math.exp(-r * t))


def _validate(t: float, x0: float, r: float, capacity: float) -> None:
    values = (t, x0, r, capacity)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("all parameters must be finite")
    if x0 <= 0:
        raise ValueError("x0 must be > 0")
    if r <= 0:
        raise ValueError("r must be > 0")
    if capacity <= 0:
        raise ValueError("capacity must be > 0")
    if x0 > capacity:
        raise ValueError("x0 must be <= capacity")


def simulate(duration: float = 10.0, dt: float = 0.1, x0: float = 0.1,
             growth_rate: float = 0.6, capacity: float = 1.0) -> dict[str, Any]:
    """Run fixed-step RK4 and compare with the analytical reference."""
    _validate(duration, x0, growth_rate, capacity)
    if not math.isfinite(dt) or dt <= 0:
        raise ValueError("dt must be finite and > 0")
    if duration < 0:
        raise ValueError("duration must be >= 0")

    steps = int(math.ceil(duration / dt)) if duration else 0
    state = x0
    elapsed = 0.0

    def derivative(value: float) -> float:
        return growth_rate * value * (1.0 - value / capacity)

    for _ in range(steps):
        step = min(dt, duration - elapsed)
        if step <= 0:
            break
        k1 = derivative(state)
        k2 = derivative(state + 0.5 * step * k1)
        k3 = derivative(state + 0.5 * step * k2)
        k4 = derivative(state + step * k3)
        state += (step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        elapsed += step

    reference = logistic_exact(duration, x0, growth_rate, capacity)
    return {
        "schema_version": "1.0",
        "model": "toy_logistic_growth_ode",
        "model_scope": "numerical verification only; not a validated cancer model",
        "solver": "classical_rk4_fixed_step",
        "parameters": {
            "duration_simulated_time_units": duration,
            "dt_simulated_time_units": dt,
            "initial_normalized_burden": x0,
            "growth_rate_per_simulated_time_unit": growth_rate,
            "carrying_capacity_normalized": capacity,
        },
        "result": {
            "final_normalized_burden": state,
            "analytic_reference": reference,
            "absolute_error": abs(state - reference),
            "steps": steps,
        },
        "interpretation_limit": (
            "Simulated time is a model variable; it does not accelerate real biology "
            "or establish treatment efficacy."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=float, default=10.0)
    parser.add_argument("--dt", type=float, default=0.1)
    parser.add_argument("--x0", type=float, default=0.1)
    parser.add_argument("--growth-rate", type=float, default=0.6)
    parser.add_argument("--capacity", type=float, default=1.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    record = simulate(args.duration, args.dt, args.x0, args.growth_rate, args.capacity)
    encoded = json.dumps(record, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
