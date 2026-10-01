# Structure module

**ID:** `bop-structure` · **Category:** core · **Applies to:** both

## Purpose

Frames, mounts and feed lines common to all variants: the baseplate support
structure for the three process strings, mounting interfaces for the feedstock
kit and storage, and routing for process fluid lines.

## Interfaces

| Direction | Stream | Notes |
|---|---|---|
| in/out | mechanical loads | launch, landing and surface loads; not analyzed |
| in/out | feed lines | process fluid routing between modules |
| out | mounting interfaces | strings, [bop-thermal](bop-thermal.md) baseplate, storage |

## Parameters

- `mass_kg: 12`, `mass_range: [8, 17]`
- No `power_w` line in the catalog (passive structure)

## Body applicability

Identical on both bodies. Lunar site grading / anchoring at a PSR-margin site
and Mars footpad behavior are site works and are not carried in this line
(open item).

## Failure modes and maintainability

Structure is a static common mode; no maintenance concept is modeled.
Launch/landing load analysis and vibration qualification are outside this
concept (open item).

## Sources

- `modules/parameters.yaml` — mass estimate
- `variants/moon/README.md` §3 — structure line in the mass budget
