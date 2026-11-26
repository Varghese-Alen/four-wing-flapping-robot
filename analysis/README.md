# Numerical readout

I have kept a small set of original inputs, result tables and numerical histories so the headline comparisons can be checked without rerunning the study. These are computational results, not experimental measurements.

## Run from the repository root

Required: Python 3.11 or newer and NumPy. The tested environment was Python 3.13.15 with NumPy 2.4.4. No plotting library, geometry application, solver or network access is used by these commands.

```sh
python3 -B analysis/reproduce.py --output analysis/reproduced
python3 -B -m unittest discover -s analysis -p 'test_*.py' -v
```

`requirements.txt` pins the tested NumPy version. If it is not installed, an optional environment preparation step is `python3 -m pip install -r analysis/requirements.txt`; this may need network access and is separate from reproduction. No dependency distributions are bundled.

The first command prints the numerical summary and writes five files:

- `reproduced/summary.json`: recalculated comparisons, grid counts, history integrals and motion checks.
- `reproduced/power-summary.svg`: mission positive mechanical power.
- `reproduced/torque-cycle.svg`: all 4,097 right-drive samples for each retained 20 Hz history.
- `reproduced/stiffness-grid.svg`: all 1,694 original sampled cases, including negative outcomes; no contour interpolation.
- `reproduced/prescribed-kinematics.csv`: 257 equally spaced cycle samples at 20 Hz, including both endpoints. Change the sampling density with `--samples 1025` if useful.

The second command runs 12 regression tests. It checks sealed numerical values, the complete stiffness-grid array digest, retained-history power and torque, spring input consistency, prescribed motion, storage estimates and SVG structure. It does not rerun numerical convergence studies or validate physical performance. Floating-point comparisons use explicit tolerances; the grid digest additionally requires exact little-endian float64 values in stiffness-major order.

## What is retained

All 14 files under `data/` are unchanged originals from the prescribed-motion study.

| Files | Purpose |
| --- | --- |
| `inputs/experiment-config.json` | Mission weights, menus, grid and conditional scenario definitions. The historical filename does not mean a physical experiment took place. |
| `inputs/model-constants.json` | Four-bar dimensions, phase, inertia assumptions and spring torque samples. |
| `inputs/formed_states.csv` | Original computational spring input table, including coarse/fine and signed loading cases. The `formed_fine_pos` rows supply the retained positive spring samples. |
| `results/comparison.csv`, `results/fixed-objective.csv` | Method comparisons and the fixed-spring mission objective. |
| `results/stiffness-frequency-grid.csv` | All 121 multipliers at 14 frequencies; negative results remain. |
| `results/conditional-samples.csv` | All 1,000 conditional cases with frozen nominal policies; not measured population tolerances. |
| `results/summary.json`, `results/kinematics.json` | Original study summaries. Historical runtime fields are not the runtime of this readout. |
| `results/fixed-grid-audit.json`, `results/quadrature-checks.csv` | Retained refinement and quadrature receipts; not newly executed checks. Some history receipts refer to files outside this selected subset. |
| `results/history-f20-*.npz` | Three complete 20 Hz histories: no spring, best fixed and optimised menu. Each has 12 numeric arrays and 4,097 samples. |

## Equations and scope

The new `reproduce.py` is a readout tool, not the original dynamics engine. It uses only these local files. The prescribed-motion function independently implements the study's exact geometric closure and analytic derivatives using the retained dimensions and assembly branch, rather than fitting a sine wave or interpolating an animation.

For cycle phase \(u\), crank angle is \(\theta=\theta_0+2\pi u\). With crank length \(r\), ground separation \(g\), coupler length \(c\) and rocker length \(a\), define the crank tip \(v=(-g+r\cos\theta,r\sin\theta)\), \(d=|v|\), \(x=(a^2-c^2+d^2)/(2d)\), and \(h=\sqrt{a^2-x^2}\). The selected rocker tip is \((xv+h\,\mathrm{perp}(v))/d\). Its polar angle minus the retained mean gives front departure; rear departure has the opposite sign. Analytic first and second derivatives give rate and acceleration at constant crank speed. The full stroke is approximately 48 degrees. No aerodynamic interaction is computed by this geometry function.

History power is integrated over dimensionless phase, so the full-cycle integral is mean power in watts. Positive and negative portions are separated before integration. Torque is an ideal input-shaft equivalent: retained output torque divided by 20, not a measured motor result. The stiffness map compares positive mechanical power with the no-spring case at the same frequency.

This subset reproduces arithmetic, figures and prescribed geometry. It does **not** regenerate spring analysis, mass properties, geometry, inverse dynamics, uncertainty samples, parameter searches or the underlying refinement runs. Only the three selected 20 Hz histories can be independently re-integrated here; mission means at 17 and 18.5 Hz are read from the retained table. The geometric motion match is a consistency check, not independent validation of the original physical model.

The original menu is labelled `selectable prescribed` in the data; the later menu is labelled `selectable optimized`. Original identifiers and numbers are preserved. The finer fixed-grid result is a retained receipt, not a new search. See [the evidence note](../docs/numerical-evidence.md) for interpretation and limitations.

## Licensing and dependencies

See the repository-level licence and notices. No third-party fonts, palettes, publication figures or software distributions are included in this subset. SVGs use a system font and a new three-colour scale. NumPy is an external runtime dependency; its installed distribution retains its own licence notices.
