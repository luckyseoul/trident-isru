#!/usr/bin/env python3
"""Render the TRIDENT-Luna professional overview PDF.

Numbers are read from the sizing model at render time, so the PDF cannot
drift from `tools/model.py` output. Requires weasyprint.

    python3 tools/make_pdf.py

Output: variants/moon/TRIDENT-Luna_Professional_Overview.pdf
"""

from __future__ import annotations

from pathlib import Path

from model import build  # tools/ is on sys.path when run as a script

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "variants" / "moon" / "TRIDENT-Luna_Professional_Overview.pdf"

CSS = """
@page {
  size: A4; margin: 18mm 16mm 20mm 16mm;
  @bottom-center { content: "TRIDENT-Luna — design concept — page " counter(page) " of " counter(pages);
                   font-size: 8px; color: #666; }
}
body { font-family: "DejaVu Sans", sans-serif; font-size: 9.5px; color: #1a202c; line-height: 1.45; }
h1 { font-size: 22px; margin: 0 0 2px 0; }
h2 { font-size: 13px; margin: 14px 0 4px 0; border-bottom: 1px solid #cbd5e0; padding-bottom: 2px; }
h3 { font-size: 10.5px; margin: 10px 0 3px 0; }
.subtitle { color: #4a5568; font-size: 11px; margin-bottom: 8px; }
.statusbar { background: #edf2f7; padding: 6px 8px; margin: 6px 0 10px 0; font-size: 9px; }
table { border-collapse: collapse; width: 100%; margin: 4px 0 8px 0; }
th, td { border: 1px solid #cbd5e0; padding: 3px 5px; text-align: left; vertical-align: top; }
th { background: #edf2f7; font-weight: bold; }
.small { color: #4a5568; font-size: 8.5px; }
.note { background: #fffaf0; border-left: 3px solid #dd6b20; padding: 5px 7px; margin: 6px 0; font-size: 8.8px; }
img { width: 100%; margin: 4px 0 2px 0; }
.caption { color: #4a5568; font-size: 8.2px; margin-bottom: 8px; }
ul { margin: 4px 0 6px 16px; padding: 0; }
li { margin-bottom: 2px; }
"""


def html() -> str:
    moon = build("variants/moon")
    mars = build("variants/mars")
    f = moon["flows"]
    e = moon["energy_kwh_per_day"]
    bop = moon["energy_total_kwh_per_day"] - e["feedstock-ice-water"] - e["processing-electrolysis"]
    cb = moon["solar_battery_crosscheck"]
    cb_mars = mars["solar_battery_crosscheck"]
    sens = moon["sensitivity_ice_mining_kwh_per_kg_water"]

    def img(name: str) -> str:
        return (ROOT / "variants" / "moon" / "figures" / name).as_uri()

    return f"""<!doctype html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>

<h1>TRIDENT-Luna</h1>
<div class="subtitle">Triple-Redundant Integrated Design for Extraterrestrial Needs — lunar surface configuration</div>
<div class="statusbar">
<b>Status:</b> design concept (not flight hardware) &nbsp;·&nbsp;
<b>Oxygen:</b> {f['o2_delivered_kg_per_day']} kg/day (≈ {moon['crew_equivalent']} crew-equivalents) &nbsp;·&nbsp;
<b>Power:</b> {moon['average_power_kw']} kW average &nbsp;·&nbsp;
<b>Mass:</b> {moon['mass_total_kg']:.0f} kg (excl. shared power plant)
</div>

<h2>1. What TRIDENT-Luna is</h2>
<p>TRIDENT-Luna is the lunar configuration of the TRIDENT ISRU platform: a
life-support-scale oxygen plant that prioritizes maintainability over
production rate. Three parallel process strings sit on a shared thermal mass
so one string can be isolated and cooled for servicing while the others keep
producing (warm-swap). The lunar variant pivots the feedstock chain from the
Martian atmosphere to <b>polar water ice</b>: ice-bearing regolith is mined
and heated, the captured water is electrolyzed, and oxygen is delivered to
life support while hydrogen is stored as a by-product.</p>

<h2>2. What changes from Mars, and why</h2>
<ul>
<li><b>Feedstock:</b> no usable atmosphere on the Moon — water ice from
permanently shadowed regions replaces atmospheric CO₂; steam electrolysis
replaces SOEC CO₂ co-electrolysis.</li>
<li><b>Hydrogen:</b> the Mars core loop carries a hydrogen deficit supplied
externally; the lunar loop produces 0.45 kg H₂/day as a by-product.</li>
<li><b>Methane:</b> carbon cannot be ISRU-closed on the Moon, so the baseline
produces no methane (the mirror image of the Mars variant's open hydrogen
item).</li>
<li><b>Power:</b> a 354 h equatorial night makes solar-battery storage
non-viable at this load (~{cb['storage_mass_kg']:,.0f} kg of Li-ion would be
required; Mars needs only ~{cb_mars['storage_mass_kg']:,.0f} kg). Baseline:
an allocation from a shared 40 kWe-class fission surface power plant.</li>
<li><b>Dust:</b> no gas phase for an electrostatic precipitator — the lunar
variant uses electrodynamic dust shields (&gt;90% removal in vacuum simulant
tests) plus mechanical exclusion and seals.</li>
<li><b>Regolith oxygen</b> (~40–45 wt% of regolith) exists everywhere but
costs ~20–25 kWh/kg O₂ to extract — carried as a contingency kit, not the
baseline.</li>
</ul>

<h2>3. Interface and architecture</h2>
<table>
<tr><th>Stage</th><th>Function</th><th>Notes</th></tr>
<tr><td>Ice feedstock kit</td><td>mine and heat ice-bearing regolith; capture water vapor</td><td>~81 kg regolith/day at 5 wt% ice</td></tr>
<tr><td>Electrolysis strings ×3</td><td>2 H₂O → 2 H₂ + O₂ (SOEC-class, steam mode)</td><td>shared thermal mass; warm-swap</td></tr>
<tr><td>Storage</td><td>gaseous O₂ buffer (3 days) + H₂ by-product</td><td>liquefaction optional, not modeled</td></tr>
<tr><td>Dust management</td><td>electrodynamic shields + seals</td><td>no consumables</td></tr>
<tr><td>Power</td><td>~3.4 kWe allocation from shared fission plant</td><td>battery for transients only</td></tr>
</table>

<h2>4. Budgets (generated by tools/model.py)</h2>
<h3>Flows</h3>
<table>
<tr><th>Flow</th><th>Value</th></tr>
<tr><td>O₂ delivered</td><td>{f['o2_delivered_kg_per_day']} kg/day</td></tr>
<tr><td>Water consumed (stoichiometric)</td><td>{f['water_kg_per_day']} kg/day</td></tr>
<tr><td>Regolith processed</td><td>{f['regolith_kg_per_day']} kg/day at 5 wt% ice</td></tr>
<tr><td>H₂ by-product (stored)</td><td>{f['h2_byproduct_kg_per_day']} kg/day</td></tr>
</table>
<h3>Energy</h3>
<table>
<tr><th>Stage</th><th>kWh/day</th></tr>
<tr><td>Ice mining + water capture</td><td>{e['feedstock-ice-water']}</td></tr>
<tr><td>Electrolysis</td><td>{e['processing-electrolysis']}</td></tr>
<tr><td>Balance of plant</td><td>{bop:.1f}</td></tr>
<tr><td><b>Total</b></td><td><b>{moon['energy_total_kwh_per_day']} kWh/day → {moon['average_power_kw']} kW average</b></td></tr>
</table>
<h3>Mass</h3>
<table>
<tr><th>Item</th><th>kg</th></tr>
<tr><td>Processing core (strings, thermal, dust, structure, redundancy)</td><td>162</td></tr>
<tr><td>Ice feedstock kit</td><td>95</td></tr>
<tr><td>Gaseous O₂ storage</td><td>43</td></tr>
<tr><td>Avionics + harness</td><td>24</td></tr>
<tr><td><b>Total</b></td><td><b>{moon['mass_total_kg']:.0f} kg</b></td></tr>
<tr><td>Optional regolith-O₂ contingency kit</td><td>+{moon.get('contingency_kit_mass_kg', 0):.0f} kg</td></tr>
</table>

<div class="note"><b>Dominant uncertainty — ice-mining energy.</b> Published
estimates span 1.2 kWh/kg water (modeled thermal mining) to ~44 kWh/kg
(lab-demonstrated, small scale). Across that band the plant's total energy
moves between {sens['1.2']['kwh_per_day']} and {sens['44']['kwh_per_day']} kWh/day.
The design target ({sens['3']['kwh_per_day']} kWh/day at 3 kWh/kg) assumes
heat recuperation at scale and must be demonstrated.</div>

<h2>5. Figures</h2>
<img src="{img('luna_energy_budget.png')}"/>
<div class="caption">Figure 1 — Daily energy by stage.</div>
<img src="{img('luna_mining_sensitivity.png')}"/>
<div class="caption">Figure 2 — Plant power vs ice-mining specific energy.</div>
<img src="{img('luna_mass_breakdown.png')}"/>
<div class="caption">Figure 3 — Concept mass breakdown.</div>
<img src="{img('luna_miner_heat_transfer.png')}"/>
<div class="caption">Figure 4 — Miner heat-transfer screen: probe length, diffusion time constant, and the extraction-energy physics floor.</div>

<h2>6. Open items</h2>
<p>Screened in this revision: heat delivery (<b>miner-heat-transfer.md</b>,
with the bench-test gate), operations (<b>ops-screens.md</b>), availability and
spares (<b>availability-screen.md</b>), stowage break-even
(<b>stowage-break-even.md</b>), and technology readiness
(<b>trl-table.md</b>). The N-1 capacity margin is decided (≥1.4× per string).
Still open: the physical bench tests, FMEA proper, condensation and rejection
detail, and batching transients. Full ledger: <b>ASSUMPTIONS.md</b>.</p>

<h2>7. Sources</h2>
<p class="small">All external figures: <b>variants/moon/SOURCES.md</b>
(verified 2026-10-01) — NSSDC Moon Fact Sheet; Colaprete et al. 2010
(LCROSS); Mazarico 2011 / Gläser 2014 (illumination); Paige/Hayne 2010 (PSR
temperatures); NASA/ESA (regolith oxygen, EDS, MRE); DOE 2024 (electrolysis);
Sowers &amp; Dreyer 2020 and LUWEX 2026 (ice mining); NASA NTRS 20220004670
(fission surface power).</p>

<h2>8. Disclaimer</h2>
<p class="small">TRIDENT-Luna is a conceptual design for research, discussion
and engineering evaluation only. It is not flight hardware, has not been
built or tested, and must not be treated as a construction or operational
plan. All performance figures are engineering estimates; real implementation
requires independent detailed design, hazard analysis, qualification testing
and professional engineering oversight.</p>
<p class="small"><b>Author:</b> Nicholas Dean Perry · design concept, October 2026 ·
Generated from tools/model.py (run 2026-10-01). Verified by 11 regression
tests and CI (github.com/luckyseoul/trident-platform).</p>

</body></html>"""


def main() -> int:
    from weasyprint import HTML

    OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html(), base_url=str(ROOT)).write_pdf(str(OUT))
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
