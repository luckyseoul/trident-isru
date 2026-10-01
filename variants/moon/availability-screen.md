# Availability and spares screen (first-order)

**Status:** screening analysis · October 2026 · **not an FMEA**
**Reproduce:** `python3 tools/availability_check.py`

## Method and assumptions

- Three independent process strings; failures Poisson; unlimited repair
  capacity ⇒ expected down strings = 3·(MTTR/MTBF) (M/M/∞ form).
- **MTBF and MTTR are assumed** — no failure data exists for this plant. The
  table spans MTBF 1–3 years per string at a 12 h repair, which includes
  isolation, cool-down (order 1 h per `ops-screens.md`), swap, leak check and
  restart.
- Crew demand 3.36 kg O₂/day (4 × 0.84); set point 3.6 kg/day; 3-day buffer
  = 10.8 kg.

## Results (MTTR 12 h)

| MTBF per string | P(2+ strings down) | spare stacks per year | online fraction |
|---|---|---|---|
| 1 year | 8.4 × 10⁻⁶ | 3.0 | 0.9986 |
| 2 years | 2.1 × 10⁻⁶ | 1.5 | 0.9993 |
| 3 years | 9.4 × 10⁻⁷ | 1.0 | 0.9995 |

## The binding finding: N-1 output, not double failure

- Two of three strings online deliver **2.40 kg O₂/day — 0.96 kg/day short of
  crew demand**. The 3-day buffer (10.8 kg) covers **11.3 days** of
  single-string outage.
- For N-1 to be *production-neutral*, per-string capacity must be
  **1.80 kg/day = 1.5× the nameplate share**. The concept does not currently
  state that design requirement.
- Simultaneous double failures are negligible at any plausible MTBF (≤ 10⁻⁵).
  The real availability concerns are therefore the output shortfall and
  **spare-stack cadence: 1–3 stacks per year**.
- Drawing down the buffer with reduced activity is a legitimate CONOPS answer
  to a single-string outage — it should be stated explicitly rather than
  implied by "the other two keep producing."

## Resolving the N-1 finding

Two defensible closures, both cheap to state and both one line of design
intent in the variant document:

1. **Design margin** — size each string for 1.80 kg O₂/day (1.5× its nameplate
   share) so two strings cover the 3.6 kg/day set point; N-1 becomes
   production-neutral. Cost: stack capacity bought for redundancy.
2. **Buffer CONOPS** — run strings at their share and accept draw-down: the
   3-day buffer (10.8 kg) covers 11.3 days at the 0.96 kg/day shortfall, with
   a stated repair timeline (12 h assumed here) and a reduced-activity
   fallback if the outage outlasts the buffer.

`variants/moon/README.md` §2 now states both. What is not acceptable is
leaving the availability behavior implicit behind "the other two keep
producing."

## What this is not

Not an FMEA. There is no failure-mode taxonomy, no common-cause analysis
(shared thermal mass, shared power and shared avionics are all common modes),
and no spares mass/stowage accounting. It is a scoping tool: it says where the
availability problem actually is.
