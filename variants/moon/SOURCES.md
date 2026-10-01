# TRIDENT source register

Every external figure used in this repository, grouped by topic. URLs were
checked on 2026-10-01. Where the literature gives a range, the range is
carried into the parameter files instead of being collapsed to one number.

## Lunar environment (TRIDENT-Luna)

- **Surface gravity 1.62 m/s² (0.166 g); solar irradiance 1361 W/m²;
  equatorial diurnal range 95–390 K; synodic day 29.53 d; tenuous
  exosphere (~25 t total; night surface pressure ~3×10⁻¹⁵ bar).**
  NASA NSSDC Moon Fact Sheet (last updated 2024-01-11; fetched 2026-10-01):
  https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html
- **PSR water ice (Cabeus): 5.6 ± 2.9 wt% water in LCROSS ejecta
  (~155 ± 12 kg water).**
  Colaprete et al., Science 330, 463 (2010), doi:10.1126/science.1186986;
  NASA release: https://www.nasa.gov/news-release/lcross-impact-data-indicates-water-on-moon/
- **Polar illumination: ~86% maximum annual illumination at the Shackleton
  rim (LOLA); the Connecting Ridge between Shackleton and de Gerlache
  reaches ~94% during the lunar day and ~86% over the year.**
  Mazarico et al. 2011: https://www.sciencedirect.com/science/article/pii/S0019103510004251
  Gläser et al. 2014: https://www.sciencedirect.com/science/article/pii/S0019103514004563
  Speyerer & Robinson 2013: https://www.sciencedirect.com/science/article/pii/S0019103512003913
- **Artemis III candidate landing regions include Connecting Ridge.**
  NASA (2022): https://www.nasa.gov/news-release/nasa-identifies-candidate-regions-for-artemis-iii-moon-landing/
- **PSR temperatures: ~40 K at the Cabeus floor; south-polar cold traps as
  low as ~33 K.**
  Paige et al., Science (2010), doi:10.1126/science.1187726;
  Hayne et al., Science (2010), doi:10.1126/science.1197136
- **Regolith oxygen content ≈ 40–45 wt%.**
  NASA Science, Lunar Regolith: https://science.nasa.gov/moon/lunar-regolith/
  ESA, Extracting oxygen from Moon dust:
  https://www.esa.int/Enabling_Support/Space_Engineering_Technology/Extracting_oxygen_from_Moon_dust
- **Dust mitigation: electrodynamic dust shield (EDS); >90% dust removal
  measured on simulant in vacuum tests (solar panels, optics, radiators).**
  NASA KSC EDS: https://www.nasa.gov/centers/kennedy/technology/eds.html
  Calle et al., NTRS: https://ntrs.nasa.gov/citations/20080023245

## Lunar ISRU processes

- **Water electrolysis, system boundary: ~51–55 kWh/kg H₂ today
  (PEM-class) with advanced/solid-oxide paths lower; equivalent to
  ≈ 6.4–6.9 kWh per kg O₂.** Derived using the 8:1 O₂:H₂ mass ratio of
  water splitting.
  DOE Hydrogen Shot Water Electrolysis Technology Assessment (2024):
  https://www.energy.gov/sites/default/files/2024-12/hydrogen-shot-water-electrolysis-technology-assessment.pdf
  MDPI review (~55 kWh/kg H₂): https://www.mdpi.com/2071-1050/15/24/16917
  ICCT (53 kWh/kg H₂, ~63% efficiency):
  https://theicct.org/sites/default/files/icct2020_assessment_of_hydrogen_production_costs_v1.pdf
- **Ice mining (thermal, modeled): ~1.2 kWh/kg water at 5 wt% ice
  (subsurface probe sublimation + cold trap).**
  Sowers & Dreyer, J. Aerospace Eng. 33(4) 04020037 (2020),
  doi:10.1061/(ASCE)AS.1943-5525.0001155
- **Ice extraction (demonstrated, lab): 50–70% recovery; energy efficiency
  22.9 g/kWh for icy regolith simulant and 66.3 g/kWh for icy glass beads
  — i.e. ~44 to ~15 kWh/kg water at current lab scale.**
  LUWEX project, Advances in Space Research (2026):
  https://www.sciencedirect.com/science/article/pii/S0273117726000669
  *The gap between the modeled 1.2 and the demonstrated ~44 kWh/kg is the
  single largest uncertainty in the lunar variant and is carried as an
  explicit sensitivity.*
- **Regolith oxygen via molten regolith electrolysis (MRE): ~20–25 kWh/kg O₂
  at system level (theoretical minimum ~8–10).**
  ESA: https://www.esa.int/Enabling_Support/Space_Engineering_Technology/Oxygen_from_moon_dust
  NASA NTRS: https://ntrs.nasa.gov/citations/20190002756
- **Ilmenite hydrogen reduction: FeTiO₃ + H₂ → Fe + TiO₂ + H₂O at
  800–1100 °C; ~95% conversion in 30 min at 1000 °C; the product water is
  electrolyzed, recycling H₂.**
  NASA NTRS: https://ntrs.nasa.gov/citations/19790021019
- **Human metabolic baselines: 0.84 kg O₂ and ~1.0 kg CO₂ per person-day.**
  NASA/SP-2010-3407 (HIDH): https://ntrs.nasa.gov/citations/20140003093
  NASA/TP-2015-218570 (BVAD): https://ntrs.nasa.gov/citations/20150014436

### Miner heat-transfer screen (`variants/moon/miner-heat-transfer.md`)

- **Regolith thermal conductivity: 0.001–0.025 W/m·K; bulk ≈ 0.01 W/m·K.**
  Apollo heat-flow reassessment (JGR 2010): https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2010JE003612
  Revised lunar heat-flow values (NTRS 19770051977): https://ntrs.nasa.gov/citations/19770051977
- **Regolith specific heat: 0.265 → 0.830 kJ/kg·K over 100–350 K.**
  NASA NTRS 19930007428: https://ntrs.nasa.gov/api/citations/19930007428/downloads/19930007428.pdf
  Hemingway et al. 1973 (Apollo 14/15/16 soils): https://adsabs.harvard.edu/full/1973LPSC....4.2481H
- **Sublimation enthalpy of water ice: 51.1 kJ/mol at 273.15 K = 2.834 MJ/kg.**
  NIST Chemistry WebBook (water): https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Units=SI
- **Microwave extraction (lab): 0.84–1.57 g/min collection from cryogenic icy
  regolith at kW-class input → 10.6–21.2 kWh/kg water.**
  Research (2025), “Massive Water Production from Cryogenic Icy Lunar Regolith
  by a Microwave Heating Method”: https://spj.science.org/doi/10.34133/research.0800
- **Drilling-based thermal extraction: pilot-scale study; static heating of 2%
  ice regolith reported at ~37.9 Wh/g.**
  https://www.researchgate.net/publication/365155522_Water_extraction_from_icy_lunar_regolith_by_drilling-based_thermal_method_in_a_pilot-scale_unit

## Power

- **Fission surface power: 40 kWe-class unit targeted to operate on the
  Moon by the early 2030s; a deployable 40 kWe concept's lander-delivered
  mass is ~6.4 t (fission system ~4.0 t + power electronics ~1.1 t +
  thermal control ~1.4 t).**
  NASA FSP: https://www.nasa.gov/exploration-systems-development-mission-directorate/fission-surface-power/
  NTRS 20220004670: https://ntrs.nasa.gov/citations/20220004670
  DOE: https://www.energy.gov/ne/articles/5-things-you-need-know-about-fission-surface-power-systems
- **Li-ion energy storage: ~100–200 Wh/kg class for space Li-ion; Saft
  VES180 cell rated 180 Wh/kg. Installed-pack estimate used by the model:
  150 Wh/kg.**
  NASA SmallSat SOA: https://www.nasa.gov/smallsat-institute/sst-soa/
  Saft VES180: https://www.saft.com/products/space-and-defense/li-ion-cells/ves180

## Program context (as of 2026-10)

- **Artemis II: crewed lunar flyby flown in 2026 (first crewed lunar flyby
  since Apollo; launched in the April 2026 window after a February 2026
  upper-stage troubleshooting and roll-back).**
  NASA: https://www.nasa.gov/mission/artemis-ii/
  NASA blog (2026-02-21): https://www.nasa.gov/blogs/missions/2026/02/21/nasa-troubleshooting-artemis-ii-rocket-upper-stage-issue-preparing-to-roll-back/
- **Artemis III: first crewed landing, targeting the lunar South Pole;
  the most recent NASA public schedule referenced by this repository is the
  2024-12-05 update (no earlier than mid-2027; dependent on HLS readiness).**
  NASA: https://www.nasa.gov/news-release/nasa-shares-orion-heat-shield-findings-updates-artemis-moon-missions/
  https://www.nasa.gov/mission/artemis-iii/
- **VIPER: after the 2024 cancellation, NASA task-ordered Blue Origin
  (2025-09) to deliver the rover to the south pole on Blue Moon MK1.**
  NASA: https://www.nasa.gov/news-release/nasa-selects-blue-origin-to-deliver-viper-rover-to-moons-south-pole/

## Mars reference (the original concept)

- NASA NSSDC Mars Fact Sheet:
  https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html
- Original Mars performance figures: `variants/mars/TRIDENT_Professional_Overview.pdf`
  (August 2026) and `variants/mars/README.md`.
