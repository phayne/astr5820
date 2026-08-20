# Data

Every dataset used in this course is archival, and every figure you hand in must
say where its numbers came from. Each file below is a plain CSV with a single
header line, values in the units named in the column header, and a provenance
block recorded here.

Load them through `astrotools.data` rather than reading paths directly, so that
the provenance stays attached to the numbers.

---

## `core_velocity_gradients.csv` — required for Problem Set 1, stage A

Velocity gradients of dense molecular cloud cores, used to set the range of
rotation rates in the Ω sweep.

| Column | Units | Meaning |
|---|---|---|
| `core_name` | — | Source designation as published |
| `grad_km_s_pc` | km s⁻¹ pc⁻¹ | Fitted linear velocity gradient across the core |
| `grad_err` | km s⁻¹ pc⁻¹ | 1σ uncertainty on the gradient |
| `radius_pc` | pc | Core radius at the tracer's contour |
| `tracer` | — | Line used (e.g. NH₃, N₂H⁺) |

Notes for whoever assembles this file:

- Gradients are **projected**, so each is a lower bound on Ω by a factor sin *i*.
  No inclination correction is applied anywhere in the code; say so in the write-up.
- Report the gradient as published. Do not convert to Ω in the file — the
  conversion lives in `constants.omega_from_velocity_gradient` so that students
  meet it explicitly.
- The sample needs to span the full observed range, roughly a decade, because the
  spread is the entire point of the Week 2 prediction. A sample truncated at the
  slow end will make the predicted distribution look artificially narrow.

**Status: not yet in the repository.** — *(instructor to supply)*

---

## `class2_disk_radii.csv` — required for Problem Set 1, stage A

Radii of Class II protoplanetary disks, for comparison against the predicted
centrifugal radii.

| Column | Units | Meaning |
|---|---|---|
| `disk_name` | — | Source designation |
| `region` | — | Star-forming region |
| `R_gas_au` | AU | Gas (CO-emitting) radius |
| `R_gas_err` | AU | 1σ uncertainty |
| `R_dust_au` | AU | Millimetre continuum radius, where available |
| `tracer` | — | CO isotopologue and transition |
| `R_definition` | — | Enclosed-flux fraction used to define the radius (e.g. 68%, 90%) |

Notes:

- **Gas radii, not dust radii, are the ones to compare against R_c.** Millimetre
  dust radii of the same disks are systematically smaller, often by a factor of
  two or more, because solids drift inward relative to the gas — that is Lecture 13,
  not a measurement discrepancy. Both columns are here so the effect can be seen.
- The radius definition matters at the tens-of-percent level. Keep the sample to a
  single definition, or record it per row and say which one the figure uses.
- Single-region samples are cleaner but small. A heterogeneous compilation is
  acceptable provided `region` is recorded, since one plausible explanation for
  the narrow observed spread is a selection effect.

**Status: not yet in the repository.** — *(instructor to supply)*

---

## Provenance requirements

For each dataset, record here before it is used:

1. Full citation of the source paper or catalogue, with a DOI or bibcode.
2. The table or query that produced it, verbatim, including access date.
3. Any cuts applied, and the sample size before and after.
4. Any unit conversion performed on the way into the CSV.
