#!/usr/bin/env python3
"""First-order heat-transfer screen for the lunar ice miner.

Answers the question the design review raised: at TRIDENT-Luna's design
point, what does it take to inject the required heat into cold regolith,
and where do conduction limits bite?

This is a screening calculation - order-of-magnitude, single-geometry
proxies - not a process design. Constants and sources are listed in
variants/moon/miner-heat-transfer.md.

Run:  python3 tools/miner_check.py
Outputs: table on stdout, plus
         variants/moon/figures/luna_miner_heat_transfer.png
"""

from __future__ import annotations

import math
from pathlib import Path

from model import build  # tools/ is on sys.path when run as a script

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "variants" / "moon" / "figures" / "luna_miner_heat_transfer.png"

# --- constants (sources: variants/moon/miner-heat-transfer.md) -------------
H_SUB_J_PER_KG = 2.834e6        # sublimation enthalpy of water ice (NIST: 51.1 kJ/mol at 273.15 K)
CP_AVG_J_PER_KG_K = 400.0       # average regolith cp, ~100-350 K (NTRS 19930007428: 0.265-0.830 kJ/kgK)
DT_REGOLITH_K = 200.0           # ~80 K ground -> ~280 K process, first-order
RHO_KG_M3 = 1500.0              # bulk regolith, order-of-magnitude estimate
PROBE_R1_M = 0.02               # probe radius
PROBE_R2_M = 0.2                # conduction influence radius
DT_PROBE_K = 200.0              # probe surface vs bulk ground
BLANKET_L_M = 0.2               # conduction path length under a surface blanket
PROBE_KG_PER_M = 2.0            # steel/Inconel tube of ~20 mm OD, estimate
K_CASES = [0.001, 0.005, 0.01, 0.02]   # W/mK; Apollo heat-flow range (0.001-0.025)
DEMONSTRATED_G_PER_MIN = (0.84, 1.57)  # microwave heating lab rates (Research, 2025)


def screen() -> dict:
    moon = build("variants/moon")
    water_kg_day = moon["flows"]["water_kg_per_day"]
    regolith_kg_day = moon["flows"]["regolith_kg_per_day"]

    q_latent = water_kg_day / 86400.0 * H_SUB_J_PER_KG
    q_sensible = regolith_kg_day / 86400.0 * CP_AVG_J_PER_KG_K * DT_REGOLITH_K
    q_total = q_latent + q_sensible

    rows = []
    for k in K_CASES:
        q_probe = 2 * math.pi * k * DT_PROBE_K / math.log(PROBE_R2_M / PROBE_R1_M)
        length = q_total / q_probe
        rows.append(
            {
                "k": k,
                "q_probe_w_m": q_probe,
                "probe_length_m": length,
                "probe_mass_kg": length * PROBE_KG_PER_M,
                "blanket_area_m2": q_total / (k * DT_REGOLITH_K / BLANKET_L_M),
                "penetration_time_days": (BLANKET_L_M**2) / (k / (RHO_KG_M3 * CP_AVG_J_PER_KG_K)) / 86400.0,
            }
        )

    water_g_min = water_kg_day * 1000.0 / 1440.0
    return {
        "water_kg_day": water_kg_day,
        "regolith_kg_day": regolith_kg_day,
        "water_g_min": water_g_min,
        "q_latent_w": q_latent,
        "q_sensible_w": q_sensible,
        "q_total_w": q_total,
        "rows": rows,
        "rate_ratio": (water_g_min / max(DEMONSTRATED_G_PER_MIN), water_g_min / min(DEMONSTRATED_G_PER_MIN)),
        "kwh_per_kg_at_1kw": (1000.0 / (1.57e-3 / 60.0)) / 3.6e6,
        "kwh_per_kg_at_2kw": (2000.0 / (1.57e-3 / 60.0)) / 3.6e6,
        "design_kwh_per_kg": 3.0,
    }


def print_table(s: dict) -> None:
    print("TRIDENT-Luna miner heat-transfer screen (first-order)\n")
    print(f"design point: {s['water_kg_day']:.2f} kg water/day = {s['water_g_min']:.2f} g/min; "
          f"{s['regolith_kg_day']:.0f} kg regolith/day at 5 wt%")
    print(f"heat demand : latent {s['q_latent_w']:.0f} W + sensible {s['q_sensible_w']:.0f} W "
          f"= {s['q_total_w']:.0f} W continuous-equivalent\n")
    print(f"{'k (W/mK)':>9} {'q (W/m)':>8} {'probe (m)':>10} {'probe (kg)':>11} {'blanket (m^2)':>14} {'tau 0.2m (d)':>13}")
    for r in s["rows"]:
        print(f"{r['k']:>9.3f} {r['q_probe_w_m']:>8.2f} {r['probe_length_m']:>10.0f} "
              f"{r['probe_mass_kg']:>11.0f} {r['blanket_area_m2']:>14.0f} {r['penetration_time_days']:>13.0f}")
    print(f"\nmicrowave lab anchor: demonstrated collection {DEMONSTRATED_G_PER_MIN[0]}-{DEMONSTRATED_G_PER_MIN[1]} g/min "
          f"(single experiment); the design point needs {s['rate_ratio'][0]:.1f}-{s['rate_ratio'][1]:.1f}x a single unit at that rate")
    print(f"demonstrated specific energy at 1-2 kW input: "
          f"{s['kwh_per_kg_at_1kw']:.1f}-{s['kwh_per_kg_at_2kw']:.1f} kWh/kg water "
          f"(design target: {s['design_kwh_per_kg']:.0f})")


def figure(s: dict) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ks = [r["k"] for r in s["rows"]]
    lengths = [r["probe_length_m"] for r in s["rows"]]
    taus = [r["penetration_time_days"] for r in s["rows"]]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.9))

    ax1.loglog(ks, lengths, "o-", color="#2b6cb0", lw=1.8)
    kit_line = 95.0 / PROBE_KG_PER_M
    ax1.axhline(kit_line, color="#718096", ls="--", lw=1)
    ax1.annotate(f"95 kg kit = {kit_line:.0f} m of probe at {PROBE_KG_PER_M:.0f} kg/m",
                 xy=(ks[0], kit_line), xytext=(0, 5), textcoords="offset points", fontsize=8, color="#718096")
    for k, L in zip(ks, lengths):
        ax1.annotate(f"{L:.0f} m", xy=(k, L), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=8.5)
    ax1.set_xlabel("regolith thermal conductivity k (W/m·K, log)")
    ax1.set_ylabel("probe length for 208 W (m, log)")
    ax1.set_title("Conduction-limited probe length", fontsize=11, weight="bold")

    ax2.loglog(ks, taus, "s-", color="#dd6b20", lw=1.8)
    for k, t in zip(ks, taus):
        ax2.annotate(f"{t:.0f} d", xy=(k, t), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=8.5)
    ax2.set_xlabel("regolith thermal conductivity k (W/m·K, log)")
    ax2.set_ylabel("time to penetrate 0.2 m (days, log)")
    ax2.set_title("Diffusion time constant", fontsize=11, weight="bold")

    fig.suptitle("TRIDENT-Luna miner: conduction is the bottleneck (first-order screen)", fontsize=12, weight="bold", y=1.03)
    fig.text(0.01, -0.06,
             "Screen only, single-geometry proxies; heat demand = latent (133 W) + sensible (~75 W) at the design point. "
             "k range: Apollo heat-flow (0.001-0.025 W/m·K). Sources: variants/moon/miner-heat-transfer.md",
             fontsize=7, color="#718096")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    from PIL import Image
    import numpy as np

    img = np.asarray(Image.open(OUT).convert("L"))
    print(f"\nwrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes; non-blank: {img.std() > 5})")


if __name__ == "__main__":
    screen_result = screen()
    print_table(screen_result)
    try:
        figure(screen_result)
    except ImportError:
        print("\n(matplotlib not available: figure skipped; table only)")
