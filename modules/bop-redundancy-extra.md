# Warm-swap redundancy module

**ID:** `bop-redundancy-extra` · **Category:** core · **Applies to:** both

## Purpose

Isolation valves, bypass manifolds and extra plumbing that make warm-swap real.
The three parallel process strings are the functional redundancy; this module
lets one string be fluidically and thermally isolated and partially cooled
while the other two keep producing.

## Interfaces

| Direction | Stream | Notes |
|---|---|---|
| in | command and status | from `bop-power-avionics` |
| in/out | process fluid | isolate one string from the shared manifold |
| in/out | coolant/heat | thermal decoupling before servicing |
| out | warm-swap capability | maintenance without stopping production |

## Parameters

- `mass_kg: 10`, `mass_range: [7, 15]`
- No `power_w` line in the catalog (passive valves and plumbing); valve
  actuation power is not modeled (open item)
- Lunar budget groups this with structure: "Structure + redundancy plumbing
  (warm-swap hardware) 22 kg" = `bop-structure` 12 + `bop-redundancy-extra` 10

## Body applicability

Identical intent and hardware class on both bodies; the surrounding interfaces
differ: angular abrasive dust and seals near the regolith interface on the Moon,
perchlorate-bearing soil on Mars. Dust: [bop-dust](bop-dust.md). Thermal:
[bop-thermal](bop-thermal.md).

## Failure modes and maintainability

The module is itself a common mode: a leak in shared plumbing affects all three
strings, so bypass manifolds must be selectable before a string is opened. Seal
and valve wear and warm-swap turnaround time are not modeled (open item;
`ASSUMPTIONS.md`).

## Sources

- `variants/moon/README.md` §2–§3 — isolated strings, warm-swap, 22 kg line
- `variants/mars/README.md` — warm-swap capability, shared thermal mass
