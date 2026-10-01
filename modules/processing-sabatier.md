# Sabatier module

**ID:** `processing-sabatier` · **Category:** core · **Applies to:** Mars only

## Purpose

Methanation: CO₂ + 4 H₂ → CH₄ + 2 H₂O. It converts atmospheric CO₂ and
electrolysis hydrogen into methane and product water, and is thermally coupled
to the electrolysis stage. Absent from the lunar baseline: methane needs carbon
and the Moon has no usable carbon feedstock.

## Interfaces

| Direction | Stream | Notes |
|---|---|---|
| in | CO₂ | from [feedstock-atmosphere-co2](feedstock-atmosphere-co2.md) |
| in | H₂ | imported stock in the published core mode; recovered from product water in a closed loop (`ASSUMPTIONS.md`) |
| in | electric power | 60 W continuous |
| out | CH₄ | Mars set point 3.8 kg/day (published 3.6–4.0 kg/sol) |
| out | H₂O | `h2o_per_kg_ch4: 2.25`; recycled closed-loop, else vented/stocked |
| out | reaction heat | credited in [bop-thermal](bop-thermal.md) |

## Parameters

- `mass_kg: 28`, `mass_range: [20, 38]`; `power_w: 60`
- `parasitic_kwh_per_kg_ch4: 1.2` — recirculation/compression; the reaction is
  exothermic and heat is credited internally
- `co2_per_kg_ch4: 2.75`, `h2_per_kg_ch4: 0.5`, `h2o_per_kg_ch4: 2.25`

## Body applicability

Mars only. The lunar variant sets `methane_kg_per_day: 0` on the
carbon-constrained Moon (`co2_available: false`); methane there would need
imported carbon and could not be ISRU-closed. The mirror case is the Mars core
mode's imported hydrogen (`ASSUMPTIONS.md`).

## Failure modes and maintainability

The reactor sits inside each of the three parallel process strings, so warm-swap
covers catalyst or thermal faults without stopping the other two. Catalyst
life, poisoning and product storage inventory are not modeled (open item).

## Sources

- `variants/mars/README.md` and the August 2026 overview PDF (Mars reference
  section) — 3.6–4.0 kg/sol, regenerative SOEC coupling
- Stoichiometry and mass/power: `modules/parameters.yaml`
