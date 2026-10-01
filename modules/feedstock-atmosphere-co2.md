# Atmosphere CO₂ feedstock module

**ID:** `feedstock-atmosphere-co2` · **Category:** core · **Applies to:** Mars

## Purpose

Intake, dust pre-separation, compressor/dryer skid. On Mars it supplies CO₂ at
process pressure to electrolysis (co-electrolysis mode) and Sabatier, with
`co2_available: true` at 610 Pa in `bodies/mars.yaml`.

## Interfaces

| Direction | Stream | Notes |
|---|---|---|
| in | Mars atmosphere | 610 Pa ambient |
| in | electric power | 110 W continuous |
| out | CO₂ at process pressure | to `processing-electrolysis`, `processing-sabatier` |
| out | rejected dust | via [bop-dust](bop-dust.md) |

## Parameters

- `mass_kg: 18`, `mass_range: [12, 26]`; `power_w: 110`
- `energy_kwh_per_kg_co2: 0.12` — drying plus compression, order-of-magnitude
- `chemistry`: `co2_per_kg_o2: 2.75`, `co2_per_kg_ch4: 2.75`
- `inputs: ["Mars atmosphere"]`, `outputs: ["CO2 at process pressure"]`

## Body applicability

Mars only. `bodies/moon.yaml` records night pressure 3.0e-10 Pa (`3×10⁻¹⁵ bar`)
and `co2_available: false`, so the lunar chain takes oxygen from polar ice
instead. Martian dust handling is gas-phase; see [bop-dust](bop-dust.md).

## Failure modes and maintainability

One skid serves all three process strings, so intake faults are plant-level:
recovery is isolation plus a warm-swap of the downstream string while the other
two keep producing. Compressor wear, dryer freeze-up and seal life are not
modeled (open item; `ASSUMPTIONS.md`).

## Sources

- NASA NSSDC Mars Fact Sheet (Mars reference section of `variants/moon/SOURCES.md`)
- `variants/mars/README.md`; `modules/parameters.yaml` engineering estimates
