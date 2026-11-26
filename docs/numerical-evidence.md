# What the numerical comparison supports

I compared a no-spring drive, one fixed spring setting and a three-setting spring menu under the same prescribed motion. The useful result is the size of the remaining advantage: most of the predicted reduction comes from adding a suitable fixed spring, not from the menu.

## Positive mechanical power

The metric is equal-weight mean **positive mechanical input power across both drives** at 17, 18.5 and 20 Hz. Negative work is not credited as electrical regeneration.

| Configuration | Mean positive mechanical power |
| --- | ---: |
| No spring | 2.144117 W |
| Best fixed on the original grid | 1.801764 W |
| Optimised three-setting menu | 1.798176 W |
| Initial three-setting menu | 1.812612 W |

The optimised menu improves on the original grid-best fixed case by **3.588 mW, or 0.19914%**. The initial menu is **10.848 mW worse** than that fixed case. Retaining that result matters: simply offering more settings did not ensure an improvement.

The original fixed multiplier is 1.625. The initial menu uses 0.75, 1 and 1.25; the optimised menu uses 1.375, 1.625 and 1.9. These are abstract spring-torque scalings, not qualified interchangeable modules. The optimised menu contains the three nominal mission-point grid optima by construction; this is not a universal optimum or a demonstrated switching strategy.

The retained finer fixed-grid check moves the best fixed multiplier to 1.63125 and its power to 1.801763 W. Against that result, the frozen menu advantage is **3.587 mW, or 0.19908%**. The two percentages refer to different fixed-grid resolutions, not conflicting estimates.

Sources: [`comparison.csv`](../analysis/data/results/comparison.csv), [`fixed-objective.csv`](../analysis/data/results/fixed-objective.csv) and [`fixed-grid-audit.json`](../analysis/data/results/fixed-grid-audit.json).

## Negative outcomes remain in the evidence

- **1,000 conditional cases, 9 negative menu advantages.** The comparison holds nominal policies fixed while varying hypothetical inertia, drag, spring calibration and damping factors. These are assumed scenarios, not experimentally identified tolerances, population probabilities or empirical confidence intervals.
- **1,694 stiffness-frequency cases, 137 negative savings.** The S3 grid spans 121 stiffness multipliers and 14 frequencies. Savings relative to no spring range from −55.8422% to +16.1347%. A negative value means greater positive mechanical power at that frequency.

The full original tables are retained, not just favourable rows: [`conditional-samples.csv`](../analysis/data/results/conditional-samples.csv) and [`stiffness-frequency-grid.csv`](../analysis/data/results/stiffness-frequency-grid.csv). The new grid figure uses discrete cells and a declared −60% to +60% colour scale; it does not imply additional sampled cases.

## Torque at 20 Hz

| Configuration | Full-cycle absolute peak per drive |
| --- | ---: |
| No spring | 2.324531 mNm |
| Best fixed | 1.677930 mNm |
| Optimised menu | 1.571341 mNm |

These values are **ideal input-shaft equivalents**, obtained by dividing output torque by an ideal gear ratio of 20. They are not measured motor torque, gearbox losses or motor-sizing validation. The readout takes the larger absolute peak across the retained left and right drive histories; the plotted cycle shows the right drive.

The three original 20 Hz NPZ histories retain all 4,097 cycle samples, including angles, rates, accelerations, torque, power components and elastic energy. The readout checks the peaks and integrates the positive, negative and signed power without rerunning dynamics.

## The storage-frequency conflict

The retained pair secant stiffness is approximately 0.071563 Nm/rad. Using \(f=\sqrt{k/I}/(2\pi)\) gives:

- **23.778 Hz** with the reference root inertia alone;
- **14.325 Hz** when the retained added-inertia hypothesis is included.

Neither estimate sits within the stated **16–18 Hz target**, and neither is the selected **20 Hz drive frequency**. These are storage estimates under two inertia assumptions, not an assembled-system resonance measurement or a verified resonance-tuning result. The conflict remains visible rather than being treated as a completed design decision.

Sources: [`model-constants.json`](../analysis/data/inputs/model-constants.json) and [`kinematics.json`](../analysis/data/results/kinematics.json).

## What I can reproduce here

[The readout and tests](../analysis/README.md) reproduce the table arithmetic, all three figures, the three retained 20 Hz history checks and the exact prescribed four-bar geometry. The analytic motion matches the stored angle, rate and acceleration histories within numerical tolerance. It is not a new dynamic simulation or an independently observed trajectory.

The selected files do not reproduce the complete geometry build, mass-property extraction, spring analysis, inverse-dynamics campaign or the generation of conditional cases. The retained numerical quadrature and refinement receipts indicate numerical consistency within the original model; they do not establish physical accuracy.

## Limits on the claim

I treat this as mechanical screening evidence. The motion is prescribed, aerodynamic coefficients and added inertia are unvalidated, and the comparison does not establish equal lift. Motor identification, electrical power, friction, switching losses, spring-module hardware, fatigue qualification and assembled dynamics remain outside this result. There is no experimental, hover, endurance or flight validation, and no demonstrated electrical saving. The small menu advantage must be weighed against those unresolved practical costs before any hardware choice.
