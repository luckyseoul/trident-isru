# Operations screens (first-order)

**Status:** screening analysis · October 2026
**Reproduce:** `python3 tools/ops_check.py`

Two operations questions the design review flagged and the sizing model does
not cover: warm-swap cooldown, and duty-cycle load profiles.

## Warm-swap cooldown

The maintainability claim — "one string is isolated and partially cooled while
the other two keep producing" — requires the isolated string to reach a
serviceable temperature. First-order radiative cooling of a lumped mass:

```
t = m·cp / (3·ε·σ·A) × (1/T1³ − 1/T0³),  T0 = 1000 K → T1 = 500 K, ε = 0.8
```

| assumptions | mass | radiating area | cooldown |
|---|---|---|---|
| nominal | 25 kg | 0.30 m² | ~43 min |
| light string / generous area | 15 kg | 0.50 m² | ~15 min |
| heavy string / cramped area | 40 kg | 0.15 m² | ~2.3 h |

Three caveats:

- These assume **radiative decoupling** from the shared thermal mass. Without a
  real isolation (vacuum gap or conduction break), the shared mass dominates
  and cooling is far slower. The isolation hardware is the enabler of the
  maintainability claim — this is the engineering that must be demonstrated,
  not a nicety.
- Time to service also includes purge/depressurization (if any), reconnect,
  leak check and restart transient — not modeled.
- Component mass, cp and radiating area are concept estimates. The screen
  exists to size the isolation requirement, not to certify a turnaround time.

## Duty-cycle profiles

Continuous auxiliary loads (from `tools/model.py`):

| ops mode | average auxiliary load | auxiliary energy |
|---|---|---|
| continuous mining (model baseline) | 805 W | 19.3 kWh/day |
| batch mining, 12 h/day | 655 W | 15.7 kWh/day |
| mining off / idle (hibernation) | 505 W | 12.1 kWh/day |

Reading it correctly:

- This table covers **auxiliary loads only**. The process energy — mining
  thermal 12.1 kWh/day + electrolysis 23.6 kWh/day = 35.7 kWh/day — is
  scheduled separately; the continuous-production total is 55.0 kWh/day, the
  batch-mining total 51.4 kWh/day, and the idle mode carries 12.1 kWh/day with
  **no production** (the O₂ buffer covers consumption until restart).
- **Batching concentrates power**: running the same daily thermal mining duty
  in 12 h doubles its instantaneous rate (~2 kW thermal) and runs the mining
  kit at 600 W; the worst-case instantaneous load is then ~3 kW class against
  a 3.4 kWe allocation — the 1.5× margin is mostly consumed, so the margin
  factor should be revisited once the real load list exists.
- Simultaneous peak in continuous mode (all loads on) is 805 W, comfortably
  inside the allocation with room for heater transients.

## What remains unmodeled

Restart transients, deep-hibernation thermal behavior, batching transients for
the thermal mining duty, and the full service turnaround sequence.
