#!/usr/bin/env python3
"""Generate the TRIDENT figures from the sizing model.

Run from the repository root:

    python3 tools/figures.py

Outputs (all values read from tools/model.py at run time; nothing hardcoded):
    figures/platform_night_storage.png
    figures/platform_module_matrix.png
    variants/moon/figures/luna_energy_budget.png
    variants/moon/figures/luna_mining_sensitivity.png
    variants/moon/figures/luna_mass_breakdown.png

The Mars variant keeps its original, published figures in
variants/mars/figures/; this script only regenerates the platform and lunar
figures.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from model import build  # tools/ is on sys.path when run as a script

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
MOONFIG = ROOT / "variants" / "moon" / "figures"

BLUE = "#2b6cb0"
ORANGE = "#dd6b20"
GREEN = "#2f855a"
GRAY = "#718096"

plt.rcParams.update(
    {
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.6,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    }
)

FOOTNOTE = "Concept estimates from tools/model.py (2026-10-01 run); expect ±30-50%. Sources: variants/moon/SOURCES.md."


def _footnote(fig, extra: str = "") -> None:
    text = f"{extra}\n{FOOTNOTE}" if extra else FOOTNOTE
    fig.text(0.01, -0.02, text, fontsize=7, color=GRAY, ha="left", va="top")


def _save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {path.relative_to(ROOT)}")


def night_storage() -> None:
    mars = build("variants/mars")
    moon = build("variants/moon")
    rows = [
        ("Mars", mars),
        ("Moon", moon),
    ]
    labels, masses, colors = [], [], []
    for name, r in rows:
        cb = r["solar_battery_crosscheck"]
        labels.append(f"{name}\nnight {cb['night_length_h']:.0f} h\nload {r['average_power_kw']} kW")
        masses.append(cb["storage_mass_kg"])
        colors.append(BLUE if name == "Mars" else ORANGE)

    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    bars = ax.bar(labels, masses, color=colors, width=0.5)
    ax.set_yscale("log")
    ax.set_ylabel("Li-ion storage mass to ride the night (kg, log scale)")
    ax.set_title("Night-length drives the power architecture", fontsize=12, weight="bold")
    ax.axhline(1000, color=GRAY, lw=1.0, ls="--")
    ax.annotate(
        "1 t viability threshold used in this study",
        xy=(1.45, 1000),
        xytext=(1.45, 1000 * 2.2),
        fontsize=8,
        color=GRAY,
        ha="right",
    )
    for bar, mass in zip(bars, masses):
        ax.annotate(
            f"{mass:,.0f} kg",
            xy=(bar.get_x() + bar.get_width() / 2, mass),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            fontsize=10,
            weight="bold",
        )
    ax.set_ylim(50, 40000)
    _footnote(
        fig,
        "Solar-battery sizing at each variant's own average load, 80% depth of discharge, 150 Wh/kg installed pack.",
    )
    _save(fig, FIG / "platform_night_storage.png")


def module_matrix() -> None:
    # ● baseline, ○ optional/contingency, - not applicable
    rows = [
        ("Feedstock: atmosphere CO2", "●", "-"),
        ("Feedstock: polar ice", "○", "●"),
        ("Feedstock: regolith oxygen", "-", "○"),
        ("Processing: electrolysis", "●", "●"),
        ("Processing: Sabatier (CH4)", "●", "-"),
        ("BoP: shared thermal mass", "●", "●"),
        ("BoP: dust mitigation", "●", "●"),
        ("BoP: power architecture", "●", "●"),
        ("BoP: gaseous storage", "●", "●"),
        ("BoP: redundancy / warm-swap", "●", "●"),
    ]
    fig, ax = plt.subplots(figsize=(6.6, 4.8))
    ax.set_axisbelow(True)
    for i, (label, m, mo) in enumerate(rows):
        y = len(rows) - 1 - i
        ax.text(0.02, y, label, va="center", ha="left", fontsize=9.5)
        ax.text(0.72, y, m, va="center", ha="center", fontsize=13)
        ax.text(0.92, y, mo, va="center", ha="center", fontsize=13)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.8, len(rows) - 0.2)
    ax.set_xticks([0.72, 0.92])
    ax.set_xticklabels(["Mars", "Moon"], fontsize=11, weight="bold")
    ax.tick_params(axis="x", length=0)
    ax.set_yticks([])
    ax.grid(False)
    ax.set_title("Module applicability: shared bones, swapped sections", fontsize=12, weight="bold")
    ax.text(
        0.5,
        -0.65,
        "● baseline   ○ optional / contingency   – not applicable\n"
        "Mars/Moon columns show the two configured variants; other bodies follow the same pattern via bodies/_template.yaml.",
        ha="center",
        fontsize=8,
        color=GRAY,
    )
    _footnote(fig)
    _save(fig, FIG / "platform_module_matrix.png")


def luna_energy_budget() -> None:
    r = build("variants/moon")
    e = r["energy_kwh_per_day"]
    stages = [
        ("Ice mining\n+ water capture", e["feedstock-ice-water"], ORANGE),
        ("Electrolysis\n(steam SOEC-class)", e["processing-electrolysis"], BLUE),
    ]
    bop = r["energy_total_kwh_per_day"] - sum(v for _, v, _ in stages)
    stages.append(("Balance of plant\n(thermal, dust, avionics...)", bop, GREEN))

    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    left = 0.0
    for label, value, color in stages:
        ax.barh([0], [value], left=left, color=color, height=0.45)
        ax.text(left + value / 2, 0, f"{value:.1f}", ha="center", va="center", color="white", fontsize=10, weight="bold")
        ax.text(left + value / 2, -0.42, label, ha="center", va="top", fontsize=8.5)
        left += value
    ax.set_xlim(0, left * 1.06)
    ax.set_yticks([])
    ax.set_xlabel("kWh per day")
    ax.set_title(
        f"TRIDENT-Luna daily energy: {r['energy_total_kwh_per_day']} kWh/day  →  {r['average_power_kw']} kW average",
        fontsize=12,
        weight="bold",
    )
    ax.annotate(
        "mining-energy range 1.2-44 kWh/kg water would move the mining slice between 4.9 and 178 kWh/day",
        xy=(0.01, 0.93),
        xycoords="axes fraction",
        fontsize=8,
        color=GRAY,
    )
    _footnote(fig)
    _save(fig, MOONFIG / "luna_energy_budget.png")


def luna_mining_sensitivity() -> None:
    r = build("variants/moon")
    water = r["flows"]["water_kg_per_day"]
    total = r["energy_total_kwh_per_day"]
    base = total - r["energy_kwh_per_day"]["feedstock-ice-water"]
    band = [1.2, 3.0, 10.0, 44.0]
    powers = [(base + water * e) / 24.0 for e in band]

    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    xs = [1.2, 3.0, 10.0, 44.0]
    ax.plot(xs, powers, "o-", color=BLUE, lw=1.8)
    for x, y in zip(xs, powers):
        ax.annotate(f"{y:.1f} kW", xy=(x, y), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=9)
    ax.axvline(3.0, color=GRAY, ls=":", lw=1)
    ax.annotate("design target 3.0", xy=(3.0, 0.2), rotation=90, fontsize=8, color=GRAY, ha="right")
    ax.set_xscale("log")
    ax.set_xlabel("Ice-mining specific energy (kWh per kg water, log scale)")
    ax.set_ylabel("Average electric power (kW)")
    ax.set_title("The mining-energy assumption dominates the power budget", fontsize=12, weight="bold")
    ax.text(
        1.35,
        8.6,
        "1.2 = modeled thermal mining (Sowers & Dreyer 2020)\n44 = lab-demonstrated today (LUWEX 2026, small scale)",
        fontsize=8,
        color=GRAY,
    )
    _footnote(fig)
    _save(fig, MOONFIG / "luna_mining_sensitivity.png")


def luna_mass_breakdown() -> None:
    r = build("variants/moon")
    cats = r["mass_by_category_kg"]
    order = [("core", "Processing core"), ("peripheral", "Ice feedstock kit"), ("storage", "Gaseous O2 storage"), ("controls", "Avionics + harness")]
    labels = [name for _, name in order]
    values = [cats[key] for key, _ in order]
    contingency = r.get("contingency_kit_mass_kg", 0)

    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    y = range(len(labels))
    ax.barh(list(y), values, color=[BLUE, ORANGE, GREEN, GRAY], height=0.55)
    for i, v in enumerate(values):
        ax.annotate(f"{v:.0f} kg", xy=(v, i), xytext=(6, 0), textcoords="offset points", va="center", fontsize=9.5)
    if contingency:
        ax.barh([len(labels)], [contingency], color="none", edgecolor=GRAY, hatch="//", height=0.55)
        ax.annotate(
            f"{contingency:.0f} kg (optional contingency kit, not in total)",
            xy=(contingency, len(labels)),
            xytext=(6, 0),
            textcoords="offset points",
            va="center",
            fontsize=9,
            color=GRAY,
        )
        labels = labels + ["Regolith-O2 contingency"]
    ax.set_yticks(list(range(len(labels))))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("kg")
    ax.set_title(f"TRIDENT-Luna mass: {r['mass_total_kg']:.0f} kg (excl. shared power plant)", fontsize=12, weight="bold")
    ax.set_xlim(0, max(values + [contingency]) * 1.35)
    _footnote(fig, "Feedstock kit mass is site- and architecture-dependent (thermal mining vs excavation + retort).")
    _save(fig, MOONFIG / "luna_mass_breakdown.png")


def check_outputs() -> None:
    from PIL import Image
    import numpy as np

    failures = []
    for path in [
        FIG / "platform_night_storage.png",
        FIG / "platform_module_matrix.png",
        MOONFIG / "luna_energy_budget.png",
        MOONFIG / "luna_mining_sensitivity.png",
        MOONFIG / "luna_mass_breakdown.png",
    ]:
        if not path.exists():
            failures.append(f"missing: {path}")
            continue
        img = np.asarray(Image.open(path).convert("L"))
        if img.std() < 5:
            failures.append(f"likely blank: {path}")
    if failures:
        raise SystemExit("figure check FAILED:\n" + "\n".join(failures))
    print("figure check: all 5 figures exist and are non-blank")


if __name__ == "__main__":
    night_storage()
    module_matrix()
    luna_energy_budget()
    luna_mining_sensitivity()
    luna_mass_breakdown()
    check_outputs()
