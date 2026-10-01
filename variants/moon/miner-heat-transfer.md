# Miner heat-transfer screen (first-order)

**Status:** screening analysis · October 2026
**Reproduce:** `python3 tools/miner_check.py` (writes the figure below and the table numbers)

**Why this exists.** The design review of TRIDENT-Luna flagged that the
"1.2–44 kWh/kg" framing of the mining risk hides a rate problem: in vacuum,
heat must be conducted into cold regolith of very low thermal conductivity,
so the extraction *rate* — not just the energy per kilogram — is a binding
constraint. This note converts that into first-order numbers and a
bench-test gate.

## Design point (same inputs as the sizing model)

- 4.05 kg water/day = **2.81 g/min**; 81 kg regolith/day at 5 wt% ice.
- Heat demand: latent 133 W (sublimation, 2.834 MJ/kg) + sensible ~75 W
  (81 kg/day heated ~200 K at ~0.4 kJ/kg·K average) = **~208 W
  continuous-equivalent**, before process losses. This is a physics floor for
  any extraction architecture.

## What conduction limits

Single-geometry proxies (steady-state radial conduction for a probe;
1-D conduction for a surface blanket; formulas in the script). The
conductivity range is the Apollo heat-flow spread: 0.001–0.025 W/m·K, with
bulk regolith near 0.01 W/m·K (vacuum; k falls with temperature, so cold PSR
ground sits toward the low end).

| k (W/m·K) | probe q′ (W/m) | probe length for 208 W | probe mass @2 kg/m | blanket area | 0.2 m penetration time |
|---|---|---|---|---|---|
| 0.001 | 0.55 | 381 m | 762 kg | 208 m² | 278 days |
| 0.005 | 2.73 | 76 m | 152 kg | 42 m² | 56 days |
| 0.010 | 5.46 | 38 m | 76 kg | 21 m² | 28 days |
| 0.020 | 10.92 | 19 m | 38 kg | 10 m² | 14 days |

Two conclusions:

1. **Meterage and area, not kilowatt-hours, are the binding constraints.**
   Delivering ~200 W through natural conduction needs tens to hundreds of
   meters of probe (tens to hundreds of kg of heater hardware) or tens to
   hundreds of m² of heated surface. The 95 kg feedstock-kit line does not
   represent this hardware and must be re-scoped for whatever heat-delivery
   architecture is chosen.
2. **Static heating cannot sustain the process.** The diffusion time constant
   to move a thermal front 0.2 m is weeks (14–278 days across the range).
   Sustained extraction therefore requires a heat source that *moves through
   fresh material* (advancing well/rod), engineered contact inside a vessel,
   or volumetric heating — not a fixed heated patch.

![Miner heat-transfer screen](figures/luna_miner_heat_transfer.png)
*Figure — Conduction-limited probe length (left) and diffusion time constant
(middle) vs regolith thermal conductivity, and the physics floor vs ice
concentration (right).*

## Physics floor vs target vs demonstrated

The energy floor for any extraction process is sublimation plus heating the
inert fraction of the regolith. Per kg of water (0.4 kJ/kg·K average over the
~200 K swing):

| Ice concentration | Inert regolith per kg water | Physics floor | vs design target |
|---|---|---|---|
| 10 wt% | 10 kg | 1.0 kWh/kg | 0.34× |
| 5 wt% (nominal) | 20 kg | 1.2 kWh/kg | 0.41× |
| 2 wt% | 50 kg | 1.9 kWh/kg | 0.63× |
| 1 wt% | 100 kg | 3.0 kWh/kg | 1.00× |

Three readings:

- The 3.0 kWh/kg design target equals the thermodynamic floor at **~1 wt%**
  concentration and sits ~2.4× above the floor at the nominal 5 wt%. The
  target is not thermodynamically forbidden — it is an engineering claim
  about heat delivery and losses.
- Measured lab processes (10.6–21.2 kWh/kg) are **9–17× the floor** at 5 wt%.
  The gap to the design target is engineering, not physics — which is exactly
  what the bench-test gate below is built to probe.
- Because the floor scales as 1/concentration, a 2 wt% site carries ~0.7
  kWh/kg of unavoidable extra energy versus 5 wt%; the variant README's
  concentration table is a throughput statement, not an energy-equivalent one.

## Where the process has to go (options, with anchors)

- **Moving heat source / drilled well.** The modelled 1.2 kWh/kg
  (Sowers & Dreyer 2020) presumes a favorable thermal-mining architecture;
  a pilot-scale drilling-based extraction reported lower energy than static
  heating (at 2% water content, static heating is ~37.9 Wh/g ≈ 37.9 kWh/kg).
  Not demonstrated at TRIDENT's duty cycle.
- **Engineered vessel / batch retort.** At this scale the solid handling is
  small — ~16 batches/day of 5 kg regolith — but heat must still bypass the
  conduction limit (agitation, gas loop, or volumetric heating), because the
  regolith bed is the insulator.
- **Volumetric (microwave).** A lab demonstration collected 0.84–1.57 g/min
  from cryogenic icy regolith at kW-class input → 10.6–21.2 kWh/kg water
  today. The design point needs 1.8–3.3× a single demonstrated unit, and the
  demonstrated specific energy is **3.5–7× the design target (3.0 kWh/kg)**.

Caveat: the proxies above are static-conduction screens. Real concepts use
vapor advection (the sublimated gas transports heat and mass to a cold trap),
which is exactly why engineered geometries exist; the point of the screen is
that natural conduction alone cannot be assumed.

## The gate that retires this risk

One bench test, specified so pass/fail is unambiguous:

1. Sealable retort or well; cryogenic start (≤100 K); lunar regolith simulant
   at 5 wt% ice; dust-bearing surfaces.
2. Metrics: **specific energy ≤ 10 kWh/kg water** (design target 3;
   demonstrated today 10.6–21.2; physics floor 1.2 at 5 wt%), **collection rate ≥ 2.8 g/min**, capture
   efficiency ≥ 90% (proposed), ≥ 100 h cumulative operation.
3. Negative-result handling: if the bench lands above 10 kWh/kg, the mining
   line rises — the model's sensitivity band already carries the consequence
   (55.1 → 83.4 kWh/day at 10 kWh/kg; 221 kWh/day at 44).

## Sources

- Regolith thermal conductivity: Apollo heat-flow measurements, 0.001–0.025
  W/m·K, bulk ≈ 0.01 W/m·K (see register: `SOURCES.md`).
- Specific heat: 0.265–0.830 kJ/kg·K over 100–350 K (NASA NTRS 19930007428;
  Hemingway et al. 1973).
- Sublimation enthalpy: 51.1 kJ/mol at 273.15 K (NIST) = 2.834 MJ/kg.
- Microwave extraction: Research (2025), "Massive Water Production from
  Cryogenic Icy Lunar Regolith by a Microwave Heating Method".
- Drilling-based extraction: pilot-scale study, 2022.
- Thermal mining baseline: Sowers & Dreyer 2020 (in `SOURCES.md`).
