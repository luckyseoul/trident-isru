# Dust mitigation balance-of-plant module

**ID:** `bop-dust` · **Category:** core · **Applies to:** both (physics differ)

## Purpose

No-consumable dust rejection and exclusion. Mars uses a parasitic RF
electrostatic precipitator on the intake; the Moon has no gas phase to
precipitate from and uses electrodynamic dust shields (EDS) plus seals. Same
module id, same mass line and interfaces — different physics inside.

## Interfaces

| Direction | Stream | Notes |
|---|---|---|
| in | dusty intake stream (Mars) | gas-phase, upstream of compression |
| in | electric power | 15 W continuous, parasitic |
| out | dust rejection / exclusion | Mars gas-phase; Moon sealing and surface clearing |
| out | protected surfaces | radiators, optics, intake, regolith interface |

## Parameters

- `mass_kg: 10`, `mass_range: [6, 15]`; `power_w: 15`
- `inputs: []`, `outputs: ["dust rejection / exclusion"]`
- Lunar EDS basis: >90% dust removal measured on simulant in vacuum tests

## Body applicability

Mars: global dust storms with fine (approx. 1–3 µm) electrostatically adhering
particles and perchlorate-bearing soil at some sites. Moon: no atmosphere, so
grains are angular, abrasive and charged; Apollo-era experience documented seal,
optical and radiator degradation.

## Failure modes and maintainability

No filter cartridges, so nothing is replaced on a dust schedule. EDS electrode
and high-voltage supply life, seal wear at the regolith interface and
long-duration adhesion are not modeled (open item; `ASSUMPTIONS.md`).

## Sources

- NASA KSC EDS and Calle et al., NTRS 20080023245 — EDS, >90% removal
- Mars reference section — NSSDC Mars Fact Sheet, `variants/mars/README.md`
