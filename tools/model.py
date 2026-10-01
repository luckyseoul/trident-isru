#!/usr/bin/env python3
"""TRIDENT concept-level sizing model.

Composes a mission variant (variants/<name>/variant.yaml) with a body
environment (bodies/<body>.yaml) and the module parameter catalog
(modules/parameters.yaml) into an order-of-magnitude consumables, energy,
power and mass budget.

This is a concept estimator for a design study, not a design tool. Values
carry +/-30-50% uncertainty at this maturity; ranges are recorded in the
parameter files and in variants/<name>/SOURCES.md.

Usage:
    python3 tools/model.py variants/moon
    python3 tools/model.py variants/mars --json
    python3 tools/model.py --list

Output is deterministic and intended to be pasted into the variant documents
(marked as generated). Re-run this after editing any parameter file.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict:
    with path.open() as fh:
        return yaml.safe_load(fh)


def variant_paths() -> list[Path]:
    return sorted((ROOT / "variants").glob("*/variant.yaml"))


def build(variant_rel: str) -> dict:
    vpath = (ROOT / variant_rel).resolve()
    variant = load(vpath / "variant.yaml")
    body = load(ROOT / "bodies" / f"{variant['body']}.yaml")
    catalog = load(ROOT / "modules" / "parameters.yaml")

    chem = catalog["chemistry"]
    sizing = catalog["sizing"]
    mods = catalog["modules"]
    categories = catalog["categories"]
    overrides = variant.get("overrides", {})

    def P(module_id: str, field: str):
        """Module parameter with variant-level override."""
        ov = overrides.get(module_id, {})
        if field in ov:
            return ov[field]
        if module_id not in mods:
            raise KeyError(f"unknown module '{module_id}' (variant {variant['name']})")
        if field not in mods[module_id]:
            raise KeyError(f"module '{module_id}' has no field '{field}'")
        return mods[module_id][field]

    result: dict = {
        "variant": variant["name"],
        "body": body["name"],
        "status": variant.get("status", "concept"),
        "flags": [],
    }

    o2_target = float(variant["o2_target_kg_per_day"])
    ch4_target = float(variant.get("methane_kg_per_day") or 0.0)
    strategy = variant.get("hydrogen_strategy", "closed_loop")

    flows: dict[str, float] = {}
    energy: dict[str, float] = {}  # kWh/day
    loads: dict[str, float] = {}   # W continuous
    water_total: float | None = None

    # ---- Process stoichiometry -------------------------------------------
    eff = float(P("processing-electrolysis", "system_efficiency"))
    e_per_kg_o2 = chem["electrolysis_thermoneutral_kwh_per_kg_o2"] / eff

    h2_from_o2 = o2_target * chem["h2_per_kg_o2"]

    if ch4_target > 0:
        water_sabatier = ch4_target * chem["h2o_per_kg_ch4"]
        h2_for_ch4 = ch4_target * chem["h2_per_kg_ch4"]
        if strategy == "imported_stock":
            h2_import = h2_for_ch4
            h2_recovered = 0.0
            water_from_sabatier = 0.0  # dumped/stocked, not electrolyzed
        else:  # closed_loop
            h2_recovered = h2_for_ch4 / 2.0           # from product-water electrolysis
            h2_import = h2_for_ch4 - h2_recovered     # net deficit supplied from water
            water_from_sabatier = water_sabatier      # recycled internally
        flows["sabatier_h2o_produced_kg_per_day"] = round(water_sabatier, 2)
        flows["h2_import_kg_per_day"] = round(h2_import, 2)
        energy["processing-sabatier"] = ch4_target * float(P("processing-sabatier", "parasitic_kwh_per_kg_ch4"))
        loads["processing-sabatier"] = float(P("processing-sabatier", "power_w"))
    else:
        h2_import = 0.0
        h2_recovered = h2_from_o2 * 0.0  # not applicable; kept for clarity

    if variant.get("feedstock") == "ice-water" or "feedstock-ice-water" in _flat_modules(variant):
        water_for_o2 = o2_target * chem["water_per_kg_o2"]
        water_total = water_for_o2
        if ch4_target > 0 and strategy == "closed_loop":
            # net water to close the H2 deficit: h2_import / 0.125 kg H2 per kg O2 -> 8 kg O2 per kg H2
            water_total += water_from_sabatier
        ice_wt = float(variant.get("feedstock_params", {}).get("ice_wt_pct", 5.0))
        regolith = water_total / (ice_wt / 100.0)
        flows["water_kg_per_day"] = round(water_total, 2)
        flows["regolith_kg_per_day"] = round(regolith, 1)
        energy["feedstock-ice-water"] = water_total * float(P("feedstock-ice-water", "energy_kwh_per_kg_water"))
        loads["feedstock-ice-water"] = float(P("feedstock-ice-water", "power_w"))
    elif "feedstock-atmosphere-co2" in _flat_modules(variant) or variant.get("feedstock") == "atmosphere-co2":
        co2 = o2_target * chem["co2_per_kg_o2"] + ch4_target * chem["co2_per_kg_ch4"]
        flows["co2_kg_per_day"] = round(co2, 1)
        energy["feedstock-atmosphere-co2"] = co2 * float(P("feedstock-atmosphere-co2", "energy_kwh_per_kg_co2"))
        loads["feedstock-atmosphere-co2"] = float(P("feedstock-atmosphere-co2", "power_w"))

    if "feedstock-regolith-oxygen" in variant.get("contingency_modules", []):
        # contingency route: energy per kg O2 if ice is not accessible (informational)
        result["contingency_regolith_o2_kwh_per_kg"] = float(P("feedstock-regolith-oxygen", "energy_kwh_per_kg_o2"))

    # O2 gross production / delivery accounting
    energy["processing-electrolysis"] = o2_target * e_per_kg_o2
    loads["processing-electrolysis"] = float(P("processing-electrolysis", "power_w"))
    flows["o2_delivered_kg_per_day"] = o2_target
    if ch4_target > 0 and strategy == "closed_loop":
        o2_gross = o2_target + ch4_target * 4.0  # overall: CO2 + 2 H2O -> CH4 + 2 O2 (4 kg O2 per kg CH4)
        flows["o2_gross_kg_per_day"] = round(o2_gross, 2)
        flows["o2_surplus_kg_per_day"] = round(o2_gross - o2_target, 2)
    if water_total is not None:
        h2_for_methane = ch4_target * chem["h2_per_kg_ch4"] if (ch4_target > 0 and strategy == "closed_loop") else 0.0
        flows["h2_byproduct_kg_per_day"] = round(max(h2_from_o2 - h2_for_methane, 0.0), 2)

    # ---- Balance of plant -------------------------------------------------
    for mid in ("bop-thermal", "bop-dust", "bop-power-avionics"):
        loads[mid] = float(P(mid, "power_w"))
    loads["bop-storage"] = float(P("bop-storage", "power_w"))

    energy_total = sum(energy.values()) + sum(loads.values()) * 24.0 / 1000.0
    avg_kw = energy_total / 24.0

    # ---- Power architecture implication -----------------------------------
    mode = variant.get("power", {}).get("mode", "fission")
    night_h = float(body["night_length_h"])
    dod = float(sizing["battery_dod"])
    wh_per_kg = float(sizing["battery_pack_wh_per_kg"])
    e_store = avg_kw * night_h / dod
    battery_kg = e_store * 1000.0 / wh_per_kg
    result["solar_battery_crosscheck"] = {
        "night_length_h": night_h,
        "storage_kwh": round(e_store, 1),
        "storage_mass_kg": round(battery_kg, 0),
        "viable": bool(battery_kg < 1000),
    }
    power_block: dict = {"mode": mode, "night_length_h": night_h, "average_load_kw": round(avg_kw, 2)}
    if mode == "solar-battery":
        power_block.update(
            storage_needed_kwh=round(e_store, 1),
            storage_mass_kg=round(battery_kg, 0),
            feasible=bool(battery_kg < 1000),
        )
        if battery_kg >= 1000:
            result["flags"].append(
                f"night storage of {e_store:.0f} kWh implies ~{battery_kg/1000:.1f} t of battery at this load - not viable; fission or hibernation required"
            )
    else:
        power_block["required_class_kwe"] = round(avg_kw * 1.5, 1)  # 1.5x margin for peaks/heaters
        result["flags"].append("power provided by shared surface fission plant; storage mass not counted in TRIDENT")

    result["power_architecture"] = power_block

    # ---- Mass --------------------------------------------------------------
    selected = _flat_modules(variant)
    if "bop-storage" in selected:
        gas_days = float(variant.get("storage_params", {}).get("buffer_days", sizing["o2_buffer_days"]))
        gas_kg = o2_target * gas_days
        storage_kg = round(gas_kg * float(sizing["tank_kg_per_kg_gas"]), 0)
    else:
        storage_kg = None

    mass_lines: list[dict] = []
    for mid in selected:
        if mid == "bop-storage" and storage_kg is None:
            continue
        m = storage_kg if mid == "bop-storage" else float(P(mid, "mass_kg"))
        mass_lines.append(
            {
                "module": mid,
                "category": categories.get(mid, "core"),
                "mass_kg": m,
                "mass_range_kg": mods.get(mid, {}).get("mass_range"),
            }
        )
    by_cat: dict[str, float] = {}
    for line in mass_lines:
        by_cat[line["category"]] = by_cat.get(line["category"], 0.0) + line["mass_kg"]

    result["flows"] = flows
    result["energy_kwh_per_day"] = {k: round(v, 1) for k, v in energy.items()}
    result["continuous_loads_w"] = loads
    result["energy_total_kwh_per_day"] = round(energy_total, 1)
    result["average_power_kw"] = round(avg_kw, 2)
    result["mass_lines"] = mass_lines
    result["mass_by_category_kg"] = {k: round(v, 0) for k, v in by_cat.items()}
    result["mass_total_kg"] = round(sum(by_cat.values()), 0)

    cont = [m for m in variant.get("contingency_modules", []) if m in mods]
    if cont:
        result["contingency_kit_mass_kg"] = round(sum(float(P(m, "mass_kg")) for m in cont), 0)

    result["crew_equivalent"] = round(o2_target / float(sizing["crew_o2_kg_per_person_day"]), 1)

    # Ice-mining energy sensitivity: the dominant uncertainty for a water-based variant.
    if water_total and "feedstock-ice-water" in selected:
        base = energy_total - energy.get("feedstock-ice-water", 0.0)
        result["sensitivity_ice_mining_kwh_per_kg_water"] = {
            f"{e:g}": {
                "kwh_per_day": round(base + water_total * e, 1),
                "average_kw": round((base + water_total * e) / 24.0, 2),
            }
            for e in (1.2, 3.0, 10.0, 44.0)
        }

    if h2_import > 0:
        result["flags"].append(f"requires imported/stocked H2 at {h2_import:.2f} kg/day (stoichiometric deficit is not ISRU-closed in this configuration)")

    return result


def _flat_modules(variant: dict) -> list[str]:
    out: list[str] = []
    for group in variant.get("modules", {}).values():
        out.extend(group)
    return out


def print_human(r: dict) -> None:
    print(f"== {r['variant']}  (body: {r['body']}, status: {r['status']}) ==")
    print(f"crew equivalent (@0.84 kg O2/person-day): {r['crew_equivalent']}")
    print("\n-- flows (per day) --")
    for k, v in r["flows"].items():
        print(f"  {k}: {v}")
    print("\n-- energy (kWh/day) --")
    for k, v in r["energy_kwh_per_day"].items():
        print(f"  {k}: {v}")
    print(f"  TOTAL: {r['energy_total_kwh_per_day']} kWh/day  -> average {r['average_power_kw']} kW")
    print("\n-- continuous loads (W) --")
    for k, v in r["continuous_loads_w"].items():
        print(f"  {k}: {v}")
    print("\n-- power architecture --")
    for k, v in r["power_architecture"].items():
        print(f"  {k}: {v}")
    cb = r.get("solar_battery_crosscheck")
    if cb:
        print(
            "  solar-battery equivalent on this body: "
            f"{cb['storage_kwh']} kWh storage / {cb['storage_mass_kg']} kg battery (viable: {cb['viable']})"
        )
    print("\n-- mass (kg) --")
    for line in r["mass_lines"]:
        print(f"  [{line['category']}] {line['module']}: {line['mass_kg']}")
    print(f"  by category: {r['mass_by_category_kg']}")
    print(f"  TOTAL: {r['mass_total_kg']} kg")
    if r.get("contingency_regolith_o2_kwh_per_kg"):
        print(f"\ncontingency regolith-O2 route: {r['contingency_regolith_o2_kwh_per_kg']} kWh/kg O2")
    if r.get("sensitivity_ice_mining_kwh_per_kg_water"):
        print("\n-- sensitivity: ice-mining energy (kWh/kg water -> total) --")
        for band, v in r["sensitivity_ice_mining_kwh_per_kg_water"].items():
            print(f"  {band:>5} kWh/kg: {v['kwh_per_day']} kWh/day, {v['average_kw']} kW")
    if r["flags"]:
        print("\n-- flags --")
        for f in r["flags"]:
            print(f"  * {f}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("variant", nargs="?", help="path to variants/<name> directory")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    ap.add_argument("--list", action="store_true", help="list available variants")
    args = ap.parse_args()

    if args.list:
        for p in variant_paths():
            print(p.parent.relative_to(ROOT))
        return 0
    if not args.variant:
        ap.print_help()
        return 2

    try:
        r = build(args.variant)
    except (KeyError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(r, indent=2))
    else:
        print_human(r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
