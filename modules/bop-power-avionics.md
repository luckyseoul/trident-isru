# Avionics and power conditioning module

**ID:** `bop-power-avionics` · **Category:** controls · **Applies to:** both

## Purpose

Control, telemetry and power conditioning across the three process strings:
string sequencing, warm-swap state, heater and valve commanding, and the
electrical interface to the shared power source. One common set of hardware
across variants.

## Interfaces

| Direction | Stream | Notes |
|---|---|---|
| in | conditioned power | from the body power architecture ([bop-power](bop-power.md)) |
| in | sensor and status data | temperatures, pressures, flows per string |
| out | actuator commands | strings, valves ([bop-redundancy](bop-redundancy-extra.md)), heaters |
| out | telemetry | to the host habitat / ops system |

## Parameters

- `mass_kg: 24`, `mass_range: [17, 32]`; `power_w: 60`

## Body applicability

Identical across bodies; only the host power interface differs (solar-battery
on Mars, fission allocation on the Moon). Radiation tolerance varies with the
host environment and is not modeled (open item).

## Failure modes and maintainability

A single avionics set is a common mode for all three strings; no failover or
degraded-mode concept is modeled at this concept level. Connector and harness
discipline near the regolith interface is a dust exposure
([bop-dust](bop-dust.md)).

## Sources

- `modules/parameters.yaml` — mass and power estimates
- `variants/moon/README.md` §3 — controls line in the mass budget
