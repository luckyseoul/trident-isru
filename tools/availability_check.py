#!/usr/bin/env python3
"""First-order availability and spares screen (not an FMEA).

Questions:
  - How often are process strings down, and does that threaten oxygen delivery?
  - How many spare stacks per year does a three-string plant imply?
  - What per-string capacity margin makes N-1 production-neutral?

Model: independent failures, unlimited repair capacity, so the number of
down strings is Poisson with mean (strings * rho), rho = MTTR/MTBF.

MTBF and MTTR are ASSUMED (no failure data exists for this plant). The screen
shows sensitivity, not prediction; it is a scoping tool, not an FMEA.

Run: python3 tools/availability_check.py
"""

from __future__ import annotations

import math

from model import build  # tools/ is on sys.path when run as a script

HOURS_PER_YEAR = 8760.0
CREW = 4
O2_KG_PER_PERSON_DAY = 0.84
BUFFER_DAYS = 3.0


def screen(mtbf_years: float, mttr_hours: float, strings: int = 3) -> dict:
    lam = 1.0 / (mtbf_years * HOURS_PER_YEAR)   # per-string failure rate, 1/h
    mu = 1.0 / mttr_hours                       # repair rate, 1/h
    rho = lam / mu                              # expected repairs in progress per string
    mean_down = strings * rho
    p0 = math.exp(-mean_down)
    p1 = mean_down * p0
    return {
        "mtbf_years": mtbf_years,
        "mttr_hours": mttr_hours,
        "mean_down_strings": mean_down,
        "p_two_or_more_down": 1.0 - p0 - p1,
        "failures_per_year": strings / mtbf_years,
        "expected_online_fraction": 1.0 - rho,
    }


def main() -> None:
    moon = build("variants/moon")
    o2 = moon["flows"]["o2_delivered_kg_per_day"]
    demand = CREW * O2_KG_PER_PERSON_DAY
    buffer_kg = o2 * BUFFER_DAYS

    print("TRIDENT-Luna availability screen (first-order; MTBF/MTTR assumed)\n")
    print(f"{'MTBF (yr)':>9} {'MTTR (h)':>9} {'P(2+ down)':>12} {'spares/yr':>10} {'online frac':>12}")
    for mtbf in (1.0, 2.0, 3.0):
        r = screen(mtbf, 12.0)
        print(f"{mtbf:>9.1f} {12.0:>9.0f} {r['p_two_or_more_down']:>12.2e} "
              f"{r['failures_per_year']:>10.1f} {r['expected_online_fraction']:>12.4f}")

    print(f"\noxygen set point {o2:.2f} kg/day; crew demand {demand:.2f} kg/day "
          f"({CREW} x {O2_KG_PER_PERSON_DAY})")
    one_down = o2 * 2.0 / 3.0
    shortfall = max(0.0, demand - one_down)
    print(f"two of three strings online: {one_down:.2f} kg/day -> shortfall {shortfall:.2f} kg/day")
    print(f"the {BUFFER_DAYS:.0f}-day buffer ({buffer_kg:.1f} kg) covers "
          f"{buffer_kg / shortfall:.1f} days of single-string outage")
    print(f"per-string capacity to cover crew demand under N-1: {demand / 2.0:.2f} kg/day "
          f"= {(demand / 2.0) / (o2 / 3.0):.2f}x nameplate share; to hold the set point: "
          f"{o2 / 2.0:.2f} kg/day = {(o2 / 2.0) / (o2 / 3.0):.2f}x")
    print("\nreading: simultaneous double failures are negligible at any plausible MTBF;")
    print("the binding issues are (a) the N-1 output shortfall and (b) stack spares cadence.")


if __name__ == "__main__":
    main()
