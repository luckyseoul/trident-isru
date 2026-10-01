# Changelog

## v1.0 — 2026-10-01 — concept baseline (lunar + modular platform)

### Added
- **Modular platform structure:** `bodies/` (Mars, Moon, template),
  `modules/` (12 module documents + the parameter catalog), `variants/`
  (assembled mission configurations).
- **Concept-level sizing model** (`tools/model.py`): stoichiometric flows,
  per-stage energy, power architecture implication (solar-battery storage vs
  fission allocation), mass roll-up, N-1 output, ice-mining sensitivity,
  and consistency flags.
- **TRIDENT-Luna**, the lunar baseline: polar water-ice feedstock → steam
  electrolysis → 3.6 kg O₂/day (~4.3 crew-equivalents); no methane
  (carbon-constrained); fission power baseline; EDS dust mitigation;
  324 kg plant incl. ice feedstock kit; contingency regolith-oxygen route.
- **Screening analyses** (each with a reproducible script):
  miner heat transfer and extraction-energy floor (`miner_check.py`),
  operations — warm-swap cooldown and duty profiles (`ops_check.py`),
  stowage break-even (`stowage_check.py`), availability and spares
  (`availability_check.py`).
- **Source register** (`variants/moon/SOURCES.md`, verified 2026-10-01),
  **assumption ledger** (`ASSUMPTIONS.md`), **TRL draft** (`trl-table.md`),
  **platform and lunar figures**, and a 5-page **overview PDF**.
- **Regression tests (11)** and **CI** running the tests plus every tool on
  each push.

### Changed
- The published Mars concept (August 2026) was moved to `variants/mars/`
  with an archival pointer; its README, PDF and figures are preserved
  unchanged.
- The top-level README now presents TRIDENT as a multi-body platform.

### Notes
- Concept design only — not flight hardware. Open items, boundaries and
  author decisions are tracked in `ASSUMPTIONS.md`.
- Mars consistency notes (hydrogen closure, ice-assisted oxygen, power
  boundary) are offered for the author's review and change nothing in the
  published Mars material.

## 2026-08 — Mars concept (as published in `trident-isru`)

- Original TRIDENT Mars overview: README, professional overview PDF, and
  five figures (oxygen comparison, mass breakdown, power budget, system
  comparison, installed mockup).
