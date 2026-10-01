# Regolith oxygen feedstock module

**ID:** `feedstock-regolith-oxygen` · **Category:** peripheral · **Applies to:** both (contingency; selected on the Moon)

## Purpose

Contingency, site-independent oxygen route where ice is not accessible: molten
regolith electrolysis (MRE) extracts O₂ from bulk regolith, with metals as a
by-product. At ~22 kWh/kg O₂ it costs roughly 2–3× the design-target ice route
(~10 kWh/kg O₂ all-in), so it ships as a contingency kit, not a baseline — and
becomes competitive if ice-mining energy proves toward the high end of its
demonstrated range (`ASSUMPTIONS.md`).

## Interfaces

| Direction | Stream | Notes |
|---|---|---|
| in | regolith | no ice concentration required |
| in | electric power | 900 W continuous |
| out | O₂ | outside the baseline budget |
| out | metals | by-product, not used by this concept |

## Parameters

- `mass_kg: 140`, `mass_range: [90, 220]`; `power_w: 900`
- `energy_kwh_per_kg_o2: 22` — system level (ESA/NASA: ~20–25; theoretical
  minimum ~8–10)
- Alternative: ilmenite hydrogen reduction at 800–1100 °C, product water
  electrolyzed to recycle H₂
- `outputs: ["O2 (and metals as by-product)"]`

## Body applicability

Both configs list regolith oxygen: ~40–45 wt% O in bulk regolith on the Moon
and Mars alike. The lunar variant selects it as `contingency_modules`; the Mars
baseline does not.

## Failure modes and maintainability

High specific energy, high cell temperature and electrode consumables are the
exposures; electrode life, melt containment and slag handling are not modeled
(open item; `ASSUMPTIONS.md`). Carried, not run, in the baseline.

## Sources

- ESA, "Extracting oxygen from Moon dust" — MRE ~20–25 kWh/kg O₂
- NASA NTRS 20190002756; NASA NTRS 19790021019 — ilmenite reduction
- NASA Science / ESA — regolith oxygen ≈ 40–45 wt%
