# Four wing flapping robot

## Opening

**A small aircraft. A useful question about complexity.**

I designed a four wing mechanism and followed its loads from the wing roots through the transmission to a proposed test bench. Along the way, I asked whether selectable springs would earn their extra complexity.

**The useful result:** one well chosen fixed spring captured almost all the calculated power benefit.

Computer designed and analysed. Physical testing is the next stage.

## 1. Start with the interfaces

A wing is only one part of a flapping machine. The bearings, shafts, spring anchors, steering links and wiring all need somewhere to go, without blocking one another.

I developed a compact reference with four 140 mm wings, two independent drives and removable torsion bars. The planning mass is about 42 g. Each drive uses a 20:1 reduction and a four bar linkage. The steering mechanism has a geometric design range of ±17°.

I worked through the small interfaces as well as the overall layout: root bearings, retained shafts, clamp seats, motor mounts, cable paths and access for assembly. Those details make the concept inspectable, even where qualification is still needed.

## 2. Give the reversing wings somewhere to store energy

At the end of each stroke, a wing slows and reverses. A spring can store some of that energy and return it during the next part of the motion.

I integrated four removable formed torsion bars into the drive structure. The reference uses 0.7 mm wire with a 45 mm active length. Removable bars make stiffness a testable design choice rather than a permanent commitment.

The motion below uses the actual linkage geometry. It is a prescribed sequence, not a prediction of how the motors will respond.

## 3. Make the comparison fair

I compared no spring, one fixed setting and three selectable settings across the same prescribed mission: 17, 18.5 and 20 Hz with equal weighting.

The first selectable menu was worse than the best fixed setting. I then optimised both choices against the same objective. That distinction mattered more than the attractive idea of changing stiffness.

The study covered 1,694 stiffness and frequency combinations. I also checked numerical integration and examined 1,000 conditional scenarios to see how dependent the conclusion was on the assumptions.

## 4. One spring gives almost all the benefit

The best fixed spring reduced calculated mechanical input power from about **2.14 W to 1.80 W**, roughly **16%** compared with no spring.

Three selectable settings improved that by only **0.2% compared with the best fixed spring**, or about **3.6 mW**. That is a small margin to spend on selection hardware, mass, friction and service complexity.

At 20 Hz, the peak ideal input shaft equivalent was about 28% lower with the fixed spring and 32% lower with the selected setting, compared with no spring. These are mechanical model results, not battery savings.

## 5. Keep the decision, not just the favourable number

My takeaway is to start with a fixed spring and measure it properly before making the transmission more complicated.

The result depends on how negative mechanical work is treated. With ideal recovery, a conservative spring does not reduce signed cycle work. The stiffness map also includes combinations that make the positive power objective worse. I have kept those outcomes in the downloadable evidence.

## 6. Design a way to measure it

I designed a dedicated bench around a reduced test article, a located fixture and a proposed six axis force sensor. Opposed contacts, liners and keepers locate the article; shims and accessible fasteners support adjustment and inspection.

In the normal measurement arrangement, loads pass through the sensor. A separate severe proof arrangement removes the sensor and its adapters, replacing them with a dedicated bypass. It is not a parallel brace that quietly short circuits the measurement.

I also laid out the enclosure, access door, latch and interlock mounts, cable routes and service access. The inspection view hides selected panels so the load path is visible. It is not an operating configuration, and the enclosure has no containment rating.

## 7. Turn the uncertainty into measurements

The next step is gated bench qualification: characterise the bars, verify retention and fixture stiffness, establish sensor and drive limits, and then measure torque and energy under controlled motion.

I would use those measurements to decide whether the spring benefit survives real losses and whether selectable stiffness is worth revisiting. The purpose of the model is to make that experiment sharper, not to stand in for it.


## Go deeper

[Reference and bench notes](technical-notes.md) · [Numerical evidence](numerical-evidence.md) · [Reproduce the readout](../analysis/README.md)
