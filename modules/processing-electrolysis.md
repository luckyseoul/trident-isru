# Electrolysis module

**ID:** `processing-electrolysis` · **Category:** core · **Applies to:** both (steam mode / CO₂ co-electrolysis mode)

## Purpose

Triple-string solid-oxide cell modules producing oxygen from the body's
feedstock: steam mode (2 H₂O → 2 H₂ + O₂) on the Moon, CO₂ co-electrolysis mode
on Mars. The shared thermal mass of the three strings makes warm-swap
maintenance practical.

## Interfaces

| Direction | Stream | Notes |
|---|---|---|
| in | water / CO₂ | 4.05 kg/day lunar at the 3.6 kg O₂/day set point |
| in | electric power | 250 W controls and heaters, external to stack energy |
| out | O₂ | 3.6 kg/day lunar, to life support |
| out | H₂ | 0.45 kg/day lunar, to [bop-storage](bop-storage.md) |
| out | process heat | shared baseplate, [bop-thermal](bop-thermal.md) |

## Parameters

- `mass_kg: 80`, `mass_range: [60, 100]`; `power_w: 250`
- `system_efficiency: 0.75` — stack + rectifier + thermal, HHV basis
  (~6.6 kWh/kg O₂; DOE PEM-class 51–55 kWh/kg H₂)
- `electrolysis_thermoneutral_kwh_per_kg_o2: 4.92`; `water_per_kg_o2: 1.125`,
  `h2_per_kg_o2: 0.125`; Mars reference override `system_efficiency: 0.88`

## Body applicability

Same cell class, different feed and mode: 23.6 kWh/day on the Moon, lower stack
energy on Mars at the 0.88 override. The lunar loop produces hydrogen
(0.45 kg/day); the Mars core mode carries an imported hydrogen deficit
(`ASSUMPTIONS.md`).

## Failure modes and maintainability

One string is isolated and partially cooled while the other two keep producing,
so stack faults do not stop oxygen delivery. Cell degradation and electrolyte
life are not modeled (open item). Isolation: [bop-redundancy](bop-redundancy-extra.md).

## Sources

- DOE Hydrogen Shot Water Electrolysis Technology Assessment (2024) — 51–55
  kWh/kg H₂, PEM-class system boundary
- MDPI review (~55 kWh/kg H₂); ICCT (53 kWh/kg H₂)
