# Thermal balance-of-plant module

**ID:** `bop-thermal` · **Category:** core · **Applies to:** both

## Purpose

Shared thermal mass baseplate, loop plumbing and radiators. It preheats the
vapor feed from regenerative process heat, keeps the plant alive through
eclipses, and provides the thermal half of warm-swap: a string is partially
cooled while the others keep producing.

## Interfaces

| Direction | Stream | Notes |
|---|---|---|
| in | process heat | Sabatier (Mars), electrolysis stack heat |
| in | electric power | 130 W keep-alive heaters and pump losses |
| out | vapor feed preheat | to [processing-electrolysis](processing-electrolysis.md) |
| out | warm-swap capability | isolation plus partial cool of one string |

## Parameters

- `mass_kg: 50`, `mass_range: [36, 70]`; `power_w: 130`
- Lunar override `power_w: 160` — vacuum environment, PSR-adjacent site:
  heaters plus pump losses
- Plant-wide continuous loads sum to 805 W (feedstock kit 300, electrolysis
  auxiliaries 250, thermal 160, dust 15, avionics 60, storage 20) → 19.3 kWh/day
  in the lunar budget; this module's own share is the 160 W keep-alive override

## Body applicability

Same hardware concept on both bodies; the load differs. Vacuum removes
convective heat rejection on the Moon, so 160 W of keep-alive heaters carry
more of the duty through the 354 h night. Radiator area and loop transients are
not modeled (open item; `ASSUMPTIONS.md`).

## Failure modes and maintainability

One shared baseplate is a plant-level common mode: a loop leak affects all
three strings, which is why the isolation hardware in
[bop-redundancy](bop-redundancy-extra.md) exists. Heater circuits are the
eclipse-critical load; pump seal life is not modeled (open item).

## Sources

- `variants/mars/README.md` — shared thermal mass, regenerative coupling
- `variants/moon/README.md` §1–§3 — vacuum rejection, keep-alive heater bus
