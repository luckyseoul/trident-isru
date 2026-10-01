# Power architecture module

**ID:** `bop-power` · **Category:** controls · **Applies to:** both (mode differs)

## Purpose

How the plant's continuous loads are met on each body. It carries no hardware
mass line in `modules/parameters.yaml`; power is architecture-level and the
plant is shared infrastructure.

## Interfaces

| Direction | Stream | Notes |
|---|---|---|
| in | solar flux | Mars 586 W/m²; Moon 1361 W/m² |
| in | fission allocation | ~3.4 kWe from a shared 40 kWe-class plant |
| out | conditioned power | 805 W continuous lunar |
| out | night storage | Mars 28.3 kWh / ~189 kg battery; Moon not viable |

## Parameters

- Mars solar + battery: `night_length_h: 12.5` implies 28.3 kWh of storage,
  ~189 kg at `battery_pack_wh_per_kg: 150` and `battery_dod: 0.8`, at the
  1.81 kW average load (model); published class 850–1100 W continuous
- Moon fission: 2.3 kW average, model `required_class_kwe: 3.4`; the
  40 kWe-class unit's lander-delivered concept mass is ~6.4 t (NTRS
  20220004670), not counted in the TRIDENT budget; batteries buffer only

## Body applicability

One body parameter flips the architecture, `night_length_h`: Mars is feasible
with batteries, the Moon (354 h equatorial) is not, so fission is baselined.

## Failure modes and maintainability

Mars arrays face 30-day dust-storm seasons, mitigated by
[bop-dust](bop-dust.md). The lunar case inherits a single shared fission plant;
availability timing is an open item (`ASSUMPTIONS.md`).

## Sources

- NASA NTRS 20220004670, NASA FSP, DOE — 40 kWe-class fission, ~6.4 t
- NASA SmallSat SOA, Saft VES180 — 100–200 Wh/kg class Li-ion storage
