#!/usr/bin/env python3
"""First-order logistics sketch: carried oxygen vs ISRU (TRIDENT-Luna).

Compares the mass of carrying the crew's oxygen for a surface mission (in
three storage forms) against the modeled lunar plant mass, with explicit
boundaries. Concept-level; assumptions are listed inline and in
variants/moon/stowage-break-even.md.

Run: python3 tools/stowage_check.py
"""

from __future__ import annotations

from model import build  # tools/ is on sys.path when run as a script

CREW = 4
O2_KG_PER_PERSON_DAY = 0.84   # NASA HIDH / BVAD
DAYS_PER_YEAR = 365.0

# Tankage/storage factors (concept estimates, see the doc)
TANK_FACTOR_GAS = 5.0         # 4 kg tank per kg gas + gas mass
TANK_FACTOR_LOX = 1.2         # +20% for cryogenic tankage
TANK_FACTOR_WATER = 1.1       # +10% for water tanks
WATER_PER_KG_O2 = 1.125

DEDICATED_FISSION_KG = 6400.0  # 40 kWe-class plant, lander-delivered (NTRS 20220004670)


def compute(plant_kg: float) -> dict:
    """Carried-oxygen masses per storage form for the baseline mission year."""
    o2_year = CREW * O2_KG_PER_PERSON_DAY * DAYS_PER_YEAR
    return {
        "o2_year": o2_year,
        "forms": {
            "gaseous O2 (5x for tanks)": o2_year * TANK_FACTOR_GAS,
            "LOX (+20% tankage)": o2_year * TANK_FACTOR_LOX,
            "water, electrolyzed on site (+10% tanks)": o2_year * WATER_PER_KG_O2 * TANK_FACTOR_WATER,
        },
    }


def break_even_months(plant_kg: float, mass_per_year: float) -> float:
    return plant_kg / mass_per_year * 12.0


def break_even_years_with_fission(plant_kg: float, mass_per_year: float) -> float:
    return (plant_kg + DEDICATED_FISSION_KG) / mass_per_year


def main() -> None:
    moon = build("variants/moon")
    plant_kg = moon["mass_total_kg"]

    data = compute(plant_kg)
    o2_year = data["o2_year"]
    forms = data["forms"]

    print("Carried-O2 baseline vs TRIDENT-Luna (first-order)\n")
    print(f"carried baseline: {CREW} crew x {O2_KG_PER_PERSON_DAY} kg/day "
          f"= {o2_year:,.0f} kg O2 per year\n")
    print(f"TRIDENT-Luna plant mass (incl. ice feedstock kit): {plant_kg:,.0f} kg\n")
    print(f"{'storage form':<45} {'kg/year':>9} {'break-even (plant only)':>25} {'+ dedicated fission':>22}")
    for label, mass in forms.items():
        print(f"{label:<45} {mass:>9,.0f} {break_even_months(plant_kg, mass):>21.1f} mo "
              f"{break_even_years_with_fission(plant_kg, mass):>19.1f} yr")


if __name__ == "__main__":
    main()
