# Technology readiness — draft assessment

**Status:** repository assessment · October 2026
**Scope:** the lunar configuration's modules, plus the Mars-reference items that
matter for the platform framing. TRL calls are programmatic judgments, not
physics; each row states its basis so the call can be challenged on evidence.
Basis references are in `SOURCES.md`.

| Element | TRL (assessment) | Basis | Next gate |
|---|---|---|---|
| Ice feedstock — thermal mining | 3 | Integrated lab extraction demonstrated (LUWEX 2026: 50–70% recovery; 22.9–66.3 g/kWh); concept modeling exists (Sowers & Dreyer 2020) | The bench-test gate in `miner-heat-transfer.md`: ≤10 kWh/kg at ≥2.8 g/min |
| Ice feedstock — microwave option | 3 | Lab: 0.84–1.57 g/min collection from cryogenic icy regolith at kW-class input (Research 2025) | Scale, duty cycle, simulant realism |
| Atmosphere CO₂ feedstock (Mars) | 5 | Mars 2020 MOXIE demonstrated CO₂→O₂ on Mars at demo scale | Plant-scale acquisition/dryer |
| Processing — steam electrolysis / SOEC (Moon) | 5 | Commercial terrestrial SOEC stacks; no space-qualified string at this scale and duty | Flight-representative string test including thermal cycling |
| Processing — CO₂ co-electrolysis (Mars) | 5 | MOXIE flight demonstration (Mars 2020) | Scale-up, lifetime |
| Processing — Sabatier | 7 | ISS CO₂ Reduction Assembly flown 2009, operational 2011 | Integration with electrolysis + shared thermal loop |
| BoP — EDS dust mitigation | 5 | EDS tested on the ISS (MISSE); vacuum simulant tests >90% removal | Lunar-surface duration demonstration; regolith-interface seals |
| BoP — shared thermal mass + warm-swap | 3 | Concept; isolation and cooldown screened first-order only (`ops-screens.md`) | Bench isolation + cooldown validation |
| BoP — fission power (context) | 5 | KRUSTY 1 kWe ground test 2018 (28 h full-power incl. failure simulation); 40 kWe-class in development | Flight demonstration (NASA target: early 2030s) |
| BoP — gaseous storage | 7 | Standard flight pressure-vessel class | — |
| BoP — redundancy plumbing (warm-swap) | 3 | Standard valves/plumbing; the integrated swap concept is untested | Warm-swap demonstration on a two-string test rig |
| Contingency — regolith oxygen (MRE) | 3 | Lab-scale electrolysis cells (ESA/NASA); electrode life unproven | Cell life test at duty, scale |

**Reading:** nothing in the plant's critical path is beyond TRL 5 without a
dedicated development program, and the two items that gate the lunar concept —
ice extraction (3) and warm-swap integration (3) — have explicit bench gates
defined in `miner-heat-transfer.md` and `ops-screens.md`. The fission plant is
the long-pole programmatic dependency (ground-tested at 1 kWe, flight class
still in development).
