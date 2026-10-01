# Storage module

**ID:** `bop-storage` · **Category:** storage · **Applies to:** both

## Purpose

Gaseous oxygen storage and buffering between production and crew consumption.
The baseline is gaseous; cryogenic liquefaction is optional and outside this
budget. The buffer is sized from the oxygen target, not carried as a catalog
mass.

## Interfaces

| Direction | Stream | Notes |
|---|---|---|
| in | O₂ | 3.6 kg/day lunar; 3.75 kg/day Mars variant |
| in | H₂ (lunar) | 0.45 kg/day by-product |
| in | electric power | 20 W continuous |
| out | O₂ to life support | 3-day buffer (`o2_buffer_days: 3`) |
| out | tank isolation | via [bop-redundancy](bop-redundancy-extra.md) |

## Parameters

- `mass_kg: null` in the catalog; `tools/model.py` computes O₂ target × buffer
  days × `tank_kg_per_kg_gas: 4.0` → 43 kg in the lunar variant's budget
- `power_w: 20`; `crew_o2_kg_per_person_day: 0.84`

## Body applicability

The same gaseous baseline applies to both bodies; only the inventory differs.
**Hydrogen storage for the lunar by-product (0.45 kg/day) is not modeled yet
and is an open item**: the budget carries no tank, mass or power line for it
(see `ASSUMPTIONS.md`). Methane storage on Mars is likewise not modeled, and
cryogenic liquefaction is excluded on both bodies.

## Failure modes and maintainability

Leak and valve isolation are the principal exposures; there are no consumables.
The tank factor is order-of-magnitude, so storage mass carries more relative
uncertainty than the rest of the budget.

## Sources

- NASA/SP-2010-3407 (HIDH), NASA/TP-2015-218570 (BVAD) — 0.84 kg O₂ per person-day
- Tank and buffer factors: `modules/parameters.yaml` engineering estimates
