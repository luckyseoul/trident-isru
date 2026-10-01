# Assumptions and open items

Every figure in this repository is an estimate. This file records what was
assumed, what is uncertain, and what would need to be resolved before either
variant could be taken beyond a concept.

**Method.** All numbers regenerate from three inputs via the sizing model:
`bodies/<body>.yaml` (environment), `modules/parameters.yaml` (module
parameters + chemistry), `variants/<name>/variant.yaml` (module selection +
targets). Regenerate with:

```bash
python3 tools/model.py variants/moon     # or variants/mars
python3 tools/figures.py                 # regenerates platform + lunar figures
```

External figures are registered in `variants/moon/SOURCES.md` (verified
2026-10-01). Estimate uncertainty is ±30–50% at this maturity unless stated.
Units: Mars figures are per 24.66 h sol, lunar figures per 24 h day; the
difference is ~3% and is not corrected for.

---

## TRIDENT-Luna — open items, ranked by consequence

1. **Ice-mining specific energy (dominant uncertainty).** Modeled thermal
   mining: ~1.2 kWh/kg water (Sowers & Dreyer 2020). Lab-demonstrated today:
   ~44 kWh/kg water on icy regolith simulant (LUWEX 2026, small unoptimized
   system). Across that band the plant's total energy moves between
   47.8 and 221 kWh/day (2.0–9.2 kW). The design target used here — 3.0
   kWh/kg — assumes heat recuperation and scale effects that are a **stated
   design requirement, not a demonstrated fact**. Retire this risk first.

   Design-review caveats (the first is now screened; the other two remain
   open model limitations):

   - **Heat-transfer screen completed** (see `variants/moon/miner-heat-transfer.md`,
     `tools/miner_check.py`). At the design point ~208 W must enter the ground;
     natural conduction would need 19–381 m of probe (38–762 kg) or 10–208 m² of
     heated surface, with diffusion time constants of weeks (14–278 days for
     0.2 m). The 95 kg kit does not represent that hardware; a bench-test gate
     (≤10 kWh/kg at ≥2.8 g/min) is specified to retire the risk.
   - **Concentration couples to energy in reality.** The first-order floor
     (sublimation + sensible heat of the inert fraction) is 1.0, 1.2, 1.9 and
     3.0 kWh/kg water at 10, 5, 2 and 1 wt% — the design target equals the
     floor only at ~1 wt%. The model applies a flat 3.0; treat its 2/5/10 wt%
     table as throughput scaling, and see `miner-heat-transfer.md` for the
     floor curve.
   - **Energy boundaries.** The feedstock kit's 300 W continuous (7.2 kWh/day)
     is charged separately from the specific-energy term; published kWh/kg
     figures may or may not include such auxiliaries — align boundaries when
     comparing.
2. **Ice concentration.** Nominal 5 wt% (LCROSS Cabeus: 5.6 ± 2.9 wt%).
   Regolith throughput is 81 kg/day at 5 wt%, 203 kg/day at 2 wt%. A site
   survey is required; the model carries the concentration as an input.
3. **PSR-to-plant concept of operations.** Mining in a PSR while processing at
   an illuminated site (for power and thermal reasons) implies regolith haul
   at tens of kg/day and repeated thermal cycling of hardware. Not modeled;
   assumed feasible. Needs a material-handling study. Policy note: mining
   alters a record-protected environment (PSR volatile stratigraphy);
   keep-out-zone compliance is a mission-level constraint.
4. **Hydrogen storage not modeled.** The lunar baseline produces 0.45 kg H₂
   per day as a by-product. Its storage mass is *not* in the 324 kg total
   (small at this scale; low priority). A likely larger trade: buffering
   oxygen as water/ice rather than as gas — ~43 kg of tanks for 3 days of
   gaseous O₂ versus a few kg of water — would shrink the storage line and
   decouple mining batch behavior from the electrolyser. Not modeled.
5. **Fission surface power availability.** The design assumes an allocation
   (~3.4 kWe) from a shared 40 kWe-class fission plant, a class NASA targets
   for the early 2030s. Without it, the solar-battery alternative at this load
   and a 354 h night is not viable (see Figure P1). Two qualifications: the
   3.4 kWe figure is the modeled average × 1.5 margin — a placeholder
   allocation, not an independently derived requirement; and at the high end
   of the mining-energy band the plant averages ~9 kW (~14 kWe class) —
   roughly a third of the shared plant, so the "minor tenant" framing holds
   only near the design target. The bounding-night figure (354 h) is
   equatorial; even the best-lit polar ridges spend ~14% of the year dark,
   and storage sized for contiguous eclipse runs remains tonne-class at this
   load — the fission baseline is robust to site choice.
6. **Dust at the regolith interface.** Electrodynamic dust shields show >90%
   removal on surfaces in vacuum simulant tests; behavior at intakes, seals
   and haul interfaces is a systems-level unknown.
7. **Night operations.** The plant is assumed to run at full load through
   eclipses on fission power, with 160 W of vacuum keep-alive heating. The
   354 h continuous-night thermal duty has not been analyzed. First-order
   screen of the rejection side: radiating ~2 kW of waste heat in vacuum at
   plausible rejection temperatures (300–350 K, sink ~0–40 K) needs roughly
   3–6 m² of radiator (P = εσA(T⁴ − T_sink⁴), ε ≈ 0.9) — area is not the
   binding constraint; keep-alive power and design-in for a 354 h dark
   period are. The 160 W figure remains a placeholder until a real thermal
   model exists.
8. **Scope confirmation.** The lunar baseline produces no methane (carbon
   constraint). If a mission requires ascent propellant from this node, the
   scope changes materially; methane would need imported carbon.

## Cross-variant module-detail items

**Component-level failure modes (both bodies).** The module documents flag
items that are not modeled at this concept level — compressor wear, catalyst
and electrode life, valve actuation power, radiator transients, launch and
landing loads, connector/harness exposure at the regolith interface. They are
pointers for a next-phase analysis, not omissions of the sizing model.

**Not modeled in this revision (next-phase analyses).** Redundancy as
engineering substance: N-1 production with two of three strings, warm-swap
cooldown time and turnaround losses, and the realization of thermal isolation
in vacuum (the shared thermal mass is a thermal *short* as well as an asset).
Duty cycles, peak loads and a hibernation mode. A heat-transfer-limited miner
model with contact-area and power-density constraints. Radiator sizing,
rejection temperature and condensation control. FMEA/availability/spares for
a life-support-critical plant. A stowage baseline and break-even against
carried consumables with an explicit cost boundary (including the shared
fission plant). A TRL table naming the bench test that retires item 1.

## TRIDENT-Mars — consistency notes on the published configuration

The Mars material is reproduced as published (August 2026). These notes
record where the shared model could not reconcile the published figures and
are offered for the author's review — they are **not** corrections.

1. **Hydrogen closure.** The overview pairs 3.6–4.0 kg CH₄/sol with
   3.6–3.9 kg O₂/sol and acknowledges a "2 mol H₂ per mol CH₄" deficit. For
   3.8 kg CH₄/sol that deficit is **0.95 kg H₂/sol** net (with product-water
   recycle), or **1.9 kg H₂/sol** without recycle (4 mol per mol CH₄ — the
   figure the model uses for the "core mode" it can actually close). The
   overview does not state the recycle fraction or the H₂ source in core
   mode; until stated, the core configuration carries an external hydrogen
   dependency.
2. **Ice-assisted oxygen.** Closing the loop fully for 3.8 kg CH₄/sol
   produces **~15.2 kg O₂/sol gross** (overall: CO₂ + 2 H₂O → CH₄ + 2 O₂).
   The published ice-assisted O₂ of 5.8–6.3 kg/sol implies a partial
   closure of roughly **25–30%** of the deficit, not a closed loop. As
   published, the CH₄ and O₂ figures are not simultaneously satisfiable
   without stating the intended partial-closure fraction (or adjusting the
   numbers).
3. **Power.** Published continuous power is 850–1100 W. The model's
   all-electric estimate for the same production is ~1.8 kW average,
   including ~645 W of balance-of-plant loads. The published figure is
   reachable only if a substantial share of SOEC process enthalpy is
   supplied as *external heat* (implied by "regenerative thermal coupling"
   but not quantified) and ancillary loads are lean (~200–300 W). State the
   process-heat source and the ancillary-load boundary to close this gap.
4. **Mass.** The model's itemization sums to ~277 kg for
   core + storage + controls, inside the published 240–280 kg class within
   estimate uncertainty. No action; recorded for traceability.
5. **Storage basis.** The model assumes a 3-day gaseous O₂ buffer
   (4 kg tank per kg gas). If the published breakdown uses a different
   buffer, align the parameter and re-run.

## Key parameter ranges (single source of truth: `modules/parameters.yaml`)

| Parameter | Value used | Range / basis |
|---|---|---|
| Crew O₂ consumption | 0.84 kg/person-day | NASA HIDH / BVAD |
| Electrolysis system efficiency | 0.75 (≈6.6 kWh/kg O₂) | DOE: 51–55 kWh/kg H₂ system (PEM-class) |
| Ice-mining energy (lunar) | 3.0 kWh/kg water | 1.2 modeled – ~44 lab-demonstrated |
| Regolith O₂ (contingency) | 22 kWh/kg O₂ | 20–25 system level (ESA/NASA) |
| Battery pack | 150 Wh/kg, 80% DoD | 100–200 Wh/kg class |
| O₂ storage tanks | 4 kg per kg gas, 3-day buffer | concept estimate |
| Fission plant (context) | 40 kWe, ~6.4 t lander-delivered | NASA NTRS 20220004670 |
| Ice concentration | 5 wt% | LCROSS Cabeus 5.6 ± 2.9 wt% |
