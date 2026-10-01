# Stowage break-even (first-order)

**Status:** screening analysis · October 2026
**Reproduce:** `python3 tools/stowage_check.py`

ISRU's first sales argument is "don't carry the consumable." This sketch
compares carrying the crew's oxygen (three storage forms) against the modeled
lunar plant mass, with the power boundary stated explicitly.

## Assumptions

- 4 crew × 0.84 kg O₂/person-day (NASA HIDH / BVAD) × 365 days.
- Storage factors (concept estimates): gaseous O₂ ×5 (4 kg tank per kg gas);
  LOX ×1.2; water ×1.125 ×1.1 (water electrolyzed on site by the plant's own
  electrolysis).
- TRIDENT-Luna plant: 324 kg including the ice feedstock kit; power excluded.
- Dedicated fission boundary: 40 kWe class, ~6.4 t lander-delivered
  (NASA NTRS 20220004670).

## Results

| carried form | kg/year | break-even, plant only | break-even, + dedicated fission |
|---|---|---|---|
| gaseous O₂ (5× tanks) | 6,132 | 0.6 months | 1.1 years |
| LOX (+20% tankage) | 1,472 | 2.6 months | 4.6 years |
| water, electrolyzed on site (+10% tanks) | 1,518 | 2.6 months | 4.4 years |

## Reading

- **If surface power already exists** (the baseline assumption for a crewed
  site — the habitat needs it anyway), the ISRU plant pays for itself on mass
  in **under 3 months** against any carried storage form.
- **With a dedicated fission plant counted**, break-even moves to **1.1–4.6
  years** depending on storage form. On pure mass, the ISRU argument is a
  multi-year-base argument; the resupply-independence argument (no launch
  cadence risk, no perishable inventory) applies from day one regardless.
- Not counted: spares, crew time, plant consumables (none major), and the
  fission plant's cost share if it serves the habitat anyway. This is a
  boundary sketch, not a logistics analysis.
