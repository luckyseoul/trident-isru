#!/usr/bin/env python3
"""First-order operations screens for the lunar variant.

Two screens the design review asked for and the sizing model does not cover:

- Warm-swap cooldown: radiative cooling time for an isolated process string
  (analytic integral: t = m*cp/(3*eps*sigma*A) * (1/T1^3 - 1/T0^3)).
- Duty-cycle profiles: continuous vs batch mining auxiliary loads, and the
  hibernation/idle load.

Concept-level estimates; geometry and material assumptions are listed inline
and discussed in variants/moon/ops-screens.md.

Run: python3 tools/ops_check.py
"""

from __future__ import annotations

from model import build  # tools/ is on sys.path when run as a script

SIGMA = 5.670374419e-8  # Stefan-Boltzmann constant, W/m^2/K^4


def cooldown_time(m_kg: float, cp: float, area_m2: float, eps: float, t0: float, t1: float) -> float:
    """Radiative cooling time from t0 to t1 [K] for lumped mass m_kg."""
    return m_kg * cp / (3 * eps * SIGMA * area_m2) * (1.0 / t1**3 - 1.0 / t0**3)


def duty_profiles(loads: dict) -> dict[str, float]:
    """Average auxiliary load [W] per ops mode, from a variant's load dict."""
    mining = loads["feedstock-ice-water"]
    rest = sum(v for k, v in loads.items() if k != "feedstock-ice-water")
    return {
        "continuous mining (model baseline)": rest + mining,
        "batch mining, 12 h/day": rest + mining * 0.5,
        "mining off / idle (hibernation)": rest,
    }


def main() -> None:
    moon = build("variants/moon")
    loads = moon["continuous_loads_w"]
    mining = loads["feedstock-ice-water"]
    rest = sum(v for k, v in loads.items() if k != "feedstock-ice-water")

    print("TRIDENT-Luna ops screens (first-order)\n")

    print("-- warm-swap cooldown (isolated string, radiative only) --")
    cases = [
        (25.0, 0.30, "nominal"),
        (15.0, 0.50, "light string / generous radiating area"),
        (40.0, 0.15, "heavy string / cramped radiating area"),
    ]
    for m, a, label in cases:
        t = cooldown_time(m, 600.0, a, 0.8, 1000.0, 500.0)
        print(f"  {m:>4.0f} kg, {a:.2f} m^2 radiating, 1000->500 K: {t/60:>5.0f} min  ({label})")
    print("  assumes: cp 600 J/kg-K, eps 0.8, sink ~40 K neglected; radiative")
    print("  isolation from the shared mass (conduction-coupled cooling is slower)")

    print("\n-- duty-cycle profiles (continuous auxiliary loads, W) --")
    print(f"  base loads (always on, excluding mining kit): {rest:.0f}")
    print(f"  mining kit: {mining:.0f}")
    for label, avg in duty_profiles(loads).items():
        print(f"  {label}: {avg:>4.0f} W average -> {avg * 24 / 1000:>4.1f} kWh/day auxiliary")
    print(f"  simultaneous peak: {rest + mining:.0f} W; the model's fission allocation")
    print("  (1.5x average) covers this with margin for heater transients")

    print("\n(restart transients, deep-hibernation thermal behavior and service turnaround")
    print(" remain unmodeled - see variants/moon/ops-screens.md)")


if __name__ == "__main__":
    main()
