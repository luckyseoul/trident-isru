# TRIDENT module catalog

**Purpose.** This directory is the body-agnostic half of TRIDENT: one parameter
file (`parameters.yaml`) that every variant reads, and one document per module.
A module is a functional block with a defined interface, a concept mass line and
a continuous load. Bodies supply environment; variants select modules; no
chemistry or budget number is hardcoded in prose. Platform overview:
[`../README.md`](../README.md). Open items: [`../ASSUMPTIONS.md`](../ASSUMPTIONS.md).
Provenance: [`../variants/moon/SOURCES.md`](../variants/moon/SOURCES.md).

## Modules

| Module id | Category | Applies to | Mass (kg) | Power (W) | Doc |
|---|---|---|---|---|---|
| `feedstock-atmosphere-co2` | core | Mars | 18 (range 12–26) | 110 | [doc](feedstock-atmosphere-co2.md) |
| `feedstock-ice-water` | peripheral | Moon (baseline); Mars (optional) | 95 (55–150) | 300 | [doc](feedstock-ice-water.md) |
| `feedstock-regolith-oxygen` | peripheral | both (contingency; selected on the Moon) | 140 (90–220) | 900 | [doc](feedstock-regolith-oxygen.md) |
| `processing-electrolysis` | core | both (steam / CO₂ co-electrolysis mode) | 80 (60–100) | 250 | [doc](processing-electrolysis.md) |
| `processing-sabatier` | core | Mars | 28 (20–38) | 60 | [doc](processing-sabatier.md) |
| `bop-thermal` | core | both | 50 (36–70) | 130 (Moon override 160) | [doc](bop-thermal.md) |
| `bop-dust` | core | both (physics differ) | 10 (6–15) | 15 | [doc](bop-dust.md) |
| `bop-power` | architecture (no catalog entry) | both (mode differs) | no hardware mass line in the catalog | no continuous-load line | [doc](bop-power.md) |
| `bop-power-avionics` | controls | both | 24 (17–32) | 60 | [doc](bop-power-avionics.md) |
| `bop-storage` | storage | both | computed by the model: 43 (Moon, 3-day buffer) | 20 | [doc](bop-storage.md) |
| `bop-redundancy-extra` | core | both | 10 (7–15) | no line (passive valves/plumbing) | [doc](bop-redundancy-extra.md) |
| `bop-structure` | core | both | 12 (8–17) | no line | [doc](bop-structure.md) |

Masses and powers are the `modules:` block of
[`parameters.yaml`](parameters.yaml); categories are its `categories:` block
(the `bop-power` row is architecture-level and has no catalog entry).
Computed masses (storage) are reproduced by
`python3 tools/model.py variants/<name>`.

## Applicability matrix: shared vs swapped

| Element | Mars | Moon | Basis |
|---|---|---|---|
| Feedstock chain | atmosphere CO₂ | polar water ice | `co2_available` in `bodies/*.yaml` |
| Contingency feedstock | — | regolith oxygen | site-independent fallback |
| Electrolysis | CO₂ co-electrolysis mode | steam mode | same solid-oxide cell class |
| Sabatier | present | absent | no ISRU carbon on the Moon |
| Thermal | shared baseplate | shared baseplate | common hardware |
| Dust | RF electrostatic precipitator | EDS + seals | gas phase vs vacuum |
| Power | solar + battery | fission allocation | `night_length_h` |
| Storage | gaseous O₂ | gaseous O₂ | same baseline |
| Structure, avionics, redundancy | common | common | `bop-structure`, `bop-power-avionics`, `bop-redundancy-extra` |

## How a variant is composed

`tools/model.py` reads three inputs: `bodies/<body>.yaml` (night length,
atmosphere, resources, dust), [`parameters.yaml`](parameters.yaml) (chemistry,
sizing rules, categories, module mass/power/specific energy) and
`variants/<name>/variant.yaml` (body, module selection, targets, power mode,
`overrides`). Module fields are fetched through one accessor, so a variant
override such as the lunar `bop-thermal` power of 160 W or the Mars reference
electrolysis efficiency of 0.88 replaces the catalog value without editing the
catalog. The model then composes stoichiometric flows from the O₂ and CH₄
targets, per-stage energy, continuous loads, the solar-battery cross-check from
`night_length_h`, and the mass budget including storage sized as O₂ target ×
`o2_buffer_days` × `tank_kg_per_kg_gas`. Output is deterministic and is the
source of the headline tables in the variant documents; re-run it after editing
any parameter file.

## Module documents

[feedstock-atmosphere-co2](feedstock-atmosphere-co2.md) ·
[feedstock-ice-water](feedstock-ice-water.md) ·
[feedstock-regolith-oxygen](feedstock-regolith-oxygen.md) ·
[processing-electrolysis](processing-electrolysis.md) ·
[processing-sabatier](processing-sabatier.md) ·
[bop-thermal](bop-thermal.md) · [bop-dust](bop-dust.md) ·
[bop-power](bop-power.md) · [bop-power-avionics](bop-power-avionics.md) ·
[bop-storage](bop-storage.md) · [bop-structure](bop-structure.md) ·
[bop-redundancy](bop-redundancy-extra.md)
