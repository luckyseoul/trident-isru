"""Regression tests for the TRIDENT tooling.

Run:  python3 -m unittest discover -s tests -t . -v

These tests pin the numbers the documents quote, the screens' core results,
the repository's internal links, and the presence of the key artifacts. They
are deliberately dependency-light (stdlib unittest + PyYAML) so CI can run
them anywhere.
"""

from __future__ import annotations

import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import availability_check  # noqa: E402
import miner_check  # noqa: E402
import model  # noqa: E402
import ops_check  # noqa: E402
import stowage_check  # noqa: E402


class ModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.moon = model.build("variants/moon")
        self.mars = model.build("variants/mars")

    def test_lunar_flows(self) -> None:
        f = self.moon["flows"]
        self.assertAlmostEqual(f["water_kg_per_day"], 4.05, delta=0.02)
        self.assertAlmostEqual(f["regolith_kg_per_day"], 81.0, delta=0.5)
        self.assertAlmostEqual(f["o2_delivered_kg_per_day"], 3.6, delta=0.01)
        self.assertAlmostEqual(f["h2_byproduct_kg_per_day"], 0.45, delta=0.01)

    def test_lunar_energy_mass_and_n1(self) -> None:
        self.assertAlmostEqual(self.moon["energy_kwh_per_day"]["processing-electrolysis"], 23.6, delta=0.2)
        self.assertAlmostEqual(self.moon["energy_total_kwh_per_day"], 55.1, delta=0.3)
        self.assertAlmostEqual(self.moon["average_power_kw"], 2.3, delta=0.05)
        self.assertAlmostEqual(self.moon["mass_total_kg"], 324, delta=1)
        self.assertAlmostEqual(self.moon["n_minus_1"]["o2_kg_per_day_with_one_string_down"], 2.4, delta=0.01)

    def test_mars_reference_flows(self) -> None:
        f = self.mars["flows"]
        self.assertAlmostEqual(f["co2_kg_per_day"], 20.8, delta=0.2)
        self.assertAlmostEqual(f["h2_import_kg_per_day"], 1.9, delta=0.05)
        self.assertAlmostEqual(self.mars["mass_total_kg"], 277, delta=1)

    def test_solar_battery_crosscheck(self) -> None:
        self.assertAlmostEqual(self.moon["solar_battery_crosscheck"]["storage_mass_kg"], 6771, delta=25)
        self.assertAlmostEqual(self.mars["solar_battery_crosscheck"]["storage_mass_kg"], 189, delta=3)


class ScreenTests(unittest.TestCase):
    def test_miner_heat_demand_and_floor(self) -> None:
        s = miner_check.screen()
        self.assertAlmostEqual(s["q_total_w"], 208, delta=3)
        self.assertAlmostEqual(s["floor_kwh_per_kg"][0.05], 1.23, delta=0.02)

    def test_miner_probe_length_at_bulk_conductivity(self) -> None:
        s = miner_check.screen()
        row = next(r for r in s["rows"] if r["k"] == 0.01)
        self.assertAlmostEqual(row["probe_length_m"], 38, delta=1)

    def test_warm_swap_cooldown_and_duty_profiles(self) -> None:
        minutes = ops_check.cooldown_time(25, 600.0, 0.30, 0.8, 1000.0, 500.0) / 60.0
        self.assertAlmostEqual(minutes, 43, delta=1.5)
        profiles = ops_check.duty_profiles(self.moon_loads())
        self.assertAlmostEqual(profiles["continuous mining (model baseline)"], 805, delta=1)
        self.assertAlmostEqual(profiles["mining off / idle (hibernation)"], 505, delta=1)

    def test_stowage_break_even(self) -> None:
        data = stowage_check.compute(324.0)
        lox = data["forms"]["LOX (+20% tankage)"]
        self.assertAlmostEqual(stowage_check.break_even_months(324.0, lox), 2.6, delta=0.1)

    def test_availability_screen(self) -> None:
        r = availability_check.screen(mtbf_years=2.0, mttr_hours=12.0)
        self.assertLess(r["p_two_or_more_down"], 1e-5)
        self.assertAlmostEqual(r["failures_per_year"], 1.5, delta=0.01)

    @staticmethod
    def moon_loads() -> dict:
        return model.build("variants/moon")["continuous_loads_w"]


class RepoTests(unittest.TestCase):
    def test_relative_links_resolve(self) -> None:
        bad = []
        for md in ROOT.rglob("*.md"):
            if ".git" in md.parts:
                continue
            for m in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", md.read_text()):
                target = m.group(1).split("#")[0].strip()
                if target and not target.startswith(("http", "mailto:")) and not (md.parent / target).resolve().exists():
                    bad.append(f"{md.relative_to(ROOT)} -> {target}")
        self.assertEqual(bad, [])

    def test_key_artifacts_exist(self) -> None:
        for rel in [
            "README.md",
            "ASSUMPTIONS.md",
            "bodies/moon.yaml",
            "bodies/mars.yaml",
            "modules/parameters.yaml",
            "tools/model.py",
            "variants/moon/README.md",
            "variants/moon/SOURCES.md",
            "variants/moon/miner-heat-transfer.md",
            "variants/moon/TRIDENT-Luna_Professional_Overview.pdf",
        ]:
            self.assertTrue((ROOT / rel).exists(), rel)


if __name__ == "__main__":
    unittest.main()
