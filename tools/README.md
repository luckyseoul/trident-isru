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
