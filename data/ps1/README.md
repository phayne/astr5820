# Data

## `herschel_core_catalog.csv`

Dense cores in the Aquila cloud complex, from the *Herschel* Gould Belt Survey.

**Source:** Könyves et al. (2015), A&A 584, A91, Table A.2, obtained from VizieR
(catalog J/A+A/584/A91) and converted from the published pipe-separated format to
CSV. Distance to the complex: 260 pc.

**Rows:** 749 cores, labeled `starless`, `prestellar`, or `protostellar` in the
`Coretype` column. The three labels are mutually exclusive here.

**Columns and units.** The published units are not uniform; convert to SI before
using anything with `astrotools`.

| Column | Quantity | Units |
|---|---|---|
| `Seq` | core running number | — |
| `Name` | core name | — |
| `Rd` | deconvolved core radius | pc |
| `Robs` | observed core radius | pc |
| `Mcore`, `e_Mcore` | core mass and uncertainty | M<sub>&#9737;</sub> |
| `Tdust`, `e_Tdust` | dust temperature from SED fitting and uncertainty | K |
| `NH2peak` | peak H<sub>2</sub> column density | 10<sup>21</sup> cm<sup>-2</sup> |
| `NH2av` | mean H<sub>2</sub> column density, using `Robs` | 10<sup>21</sup> cm<sup>-2</sup> |
| `NH2avd` | mean H<sub>2</sub> column density, using `Rd` | 10<sup>21</sup> cm<sup>-2</sup> |
| `nH2peak` | beam-averaged peak H<sub>2</sub> volume density | 10<sup>4</sup> cm<sup>-3</sup> |
| `nH2av` | mean H<sub>2</sub> volume density, using `Robs` | 10<sup>4</sup> cm<sup>-3</sup> |
| `nH2avd` | mean H<sub>2</sub> volume density, using `Rd` | 10<sup>4</sup> cm<sup>-3</sup> |
| `alphaBE` | Bonnor–Ebert mass ratio | — |
| `Coretype` | `starless`, `prestellar`, or `protostellar` | — |
| `Com` | comments, including `no SED fit` | — |

Capital `N` is a column density; lowercase `n` is a volume density. The `av`
columns are averaged over the observed radius `Robs`, the `avd` columns over the
deconvolved radius `Rd`, which corrects for the 18.2-arcsec beam. Cores marked
`no SED fit` were detected in too few bands to fit a temperature and carry an
assigned value of 11.5 K.
