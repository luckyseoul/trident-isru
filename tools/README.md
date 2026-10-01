# tools/

Concept-level sizing model and figure generation for the TRIDENT variants.

## model.py

Composes a variant from three inputs and emits a budget:

- `bodies/<body>.yaml` — environment (night length, atmosphere, resources, dust)
- `modules/parameters.yaml` — module parameters, chemistry constants, sources
- `variants/<name>/variant.yaml` — selected modules + targets

```bash
python3 tools/model.py variants/moon          # human-readable budget
python3 tools/model.py variants/mars --json   # machine-readable
python3 tools/model.py --list                 # available variants
```

What it does: stoichiometric flows, energy per stage, average power, power
architecture implication (solar-battery storage sizing or fission allocation),
mass roll-up by category, flags for known gaps (e.g., imported H₂), and the
ice-mining energy sensitivity band.

What it does **not** do: thermal, structural, reliability or cost analysis;
margins; radiation; detailed component sizing. It is a concept estimator —
see `ASSUMPTIONS.md` for the uncertainty posture.

## figures.py

Generates the platform and lunar figures from the model (no numbers are
hardcoded in the plots):

```bash
python3 tools/figures.py
```

Outputs: `figures/platform_night_storage.png`,
`figures/platform_module_matrix.png`,
`variants/moon/figures/luna_{energy_budget,mining_sensitivity,mass_breakdown}.png`.
Requires matplotlib and Pillow. The Mars variant keeps its original published
figures in `variants/mars/figures/`.

## miner_check.py

First-order heat-transfer screen for the lunar ice miner (risk item 1): heat
demand at the design point, conduction-limited probe length and blanket area,
diffusion time constants across the Apollo conductivity range, and the
microwave lab anchor.

```bash
python3 tools/miner_check.py
```

Writes `variants/moon/figures/luna_miner_heat_transfer.png`. Analysis and the
bench-test gate: `variants/moon/miner-heat-transfer.md`.

## ops_check.py

First-order operations screens for the lunar variant: warm-swap cooldown time
(radiative integral, with assumption cases) and duty-cycle auxiliary load
profiles (continuous / batch mining / idle).

```bash
python3 tools/ops_check.py
```

Analysis: `variants/moon/ops-screens.md`.

## stowage_check.py

First-order logistics sketch: carried-oxygen baseline (three storage forms)
versus the TRIDENT-Luna plant mass, with and without a dedicated fission
plant boundary.

```bash
python3 tools/stowage_check.py
```

Analysis: `variants/moon/stowage-break-even.md`.
