# Reference and bench notes

### Reference and interfaces

The displayed aircraft is the DC1/WM1 reference. Its planning mass is 41.945526 g, including allocated provisions; it is not a weighed prototype. The approximately 330 mm design span is a planning envelope, not a claim that every neutral pose has that projected tip distance. The reference contains 495 geometric leaves and 540 solids. The later 42.236532 g correction candidate was not adopted.

Interface work includes upper and lower drive packaging, root bearing seats, shaft retention, spring clamps and anchors, steering links and servo allocation, battery and board provisions, wiring clearance and fastener access. Finite prescribed rigid pose checks do not prove flexible wing or spring clearance in operation. Strength, joint retention and fatigue qualification remain unresolved.

### Power and stiffness comparison

The objective is mean positive mechanical input power for both drives, equally weighted across 17, 18.5 and 20 Hz. No spring: 2.144117426002209 W. Best fixed grid setting: 1.8017642926779402 W at stiffness multiplier 1.625. Optimised menu: 1.7981761969290264 W, with multipliers 1.375, 1.625 and 1.900. Its advantage over the fixed grid setting is 0.19914345974638506%, or 3.588095748913833 mW.

The separate refined fixed search used multiplier 1.63125 and found a menu advantage of 0.19908046589902756%, or 3.5869584841936586 mW. The original menu was 10.848150059460826 mW worse than the best fixed grid setting. Nine of the 1,000 conditional scenarios gave a negative menu advantage. These are hypothetical conditional cases, not a measured population or confidence interval.

The settings are abstract spring torque scalings, not qualified parts or an implemented switching mechanism. The map retains all 1,694 sampled cases, including 137 with negative savings, and the original −60 to +60% colour scale. Pair stiffness is twice the single bar secant stiffness times the multiplier. The circle at 20 Hz and 135.96958824333598 N·mm/rad marks a sampled reference with 16.134411225375423% saving versus no spring at that frequency, not a feasible design optimum. The dashed line is a simplified storage frequency estimate, not an assembled modal result.

At 20 Hz, absolute cycle peak ideal input shaft equivalents per drive are 2.3245311158525084, 1.677929889047573 and 1.571341065517272 mN·m for no spring, fixed and selected settings. These are output torques divided by the ideal 20:1 ratio, not measured motor torque.

### Model limits and the next physical gate

Motion is imposed and aerodynamic loads are unvalidated. The work does not establish electrical efficiency, equal lift performance, endurance, hover, full cycle converged airflow, or strength and life qualification. The simple reference storage estimate is 23.7779 Hz dry and 14.3254 Hz with the legacy added inertia hypothesis. The selected multiplier 1.9 at 20 Hz also misses the earlier 16–18 Hz storage target. Material properties, retention, fatigue and assembled frequency need measurement.

All ten physical qualification holds remain open. The bench model has 1,096 solids, including the complete enclosure. The proposed sensor and its overload path are not qualified by the rendering. Severe proof through the measurement sensor is prohibited. Neither the exchange models nor the inspection images authorise manufacture, energisation or an unguarded test.

