# Polar ice / water feedstock module

**ID:** `feedstock-ice-water` · **Category:** peripheral · **Applies to:** Moon (baseline); optional on Mars

## Purpose

Peripheral kit: regolith acquisition/transfer plus thermal miner and cold-trap
capture, converting ice-bearing regolith into water for steam electrolysis.
Mass is site- and architecture-dependent (thermal mining vs
excavation-plus-retort). [bop-thermal](bop-thermal.md) takes the low-grade heat.

## Interfaces

| Direction | Stream | Notes |
|---|---|---|
| in | ice-bearing regolith | 5 wt% nominal, polar PSR site |
| in | electric power | 300 W continuous |
| out | water | 4.05 kg/day at the 3.6 kg O₂/day set point |
| out | spent regolith | ~77 kg/day (81 kg/day mined at 5 wt%, minus extracted water); haul CONOPS is an open item (`ASSUMPTIONS.md`) |

## Parameters

- `mass_kg: 95`, `mass_range: [55, 150]`; `power_w: 300`
- `energy_kwh_per_kg_water: 3.0`;
  `energy_kwh_per_kg_water_range: [1.2, 3.0, 44]` — 1.2 modeled (Sowers &
  Dreyer 2020), ~44 lab-demonstrated (LUWEX 2026)
- Sensitivity: *plant* energy totals 47.8 kWh/day at 1.2 kWh/kg water and
  221 kWh/day at 44 kWh/kg (the mining term alone is 4.9 and 178 kWh/day)
- `water_per_kg_o2: 1.125`

## Body applicability

Lunar baseline, where LCROSS ejecta at Cabeus measured 5.6 ± 2.9 wt% water and
PSR sites run ~40 K. Mars lists ice as available but treats it as an optional
ice-melt subsystem, not a baseline.

## Failure modes and maintainability

Ice-mining energy is the dominant uncertainty and the risk to retire first.
Mechanism wear, cold-trap fouling and haul distance are not modeled (open item;
`ASSUMPTIONS.md`). Fallback: [regolith-oxygen](feedstock-regolith-oxygen.md).

## Sources

- Colaprete et al., Science 330, 463 (2010) — LCROSS/Cabeus 5.6 ± 2.9 wt%
- Sowers & Dreyer 2020 — ~1.2 kWh/kg water (modeled)
- LUWEX project (2026) — ~44 to ~15 kWh/kg water, lab scale
