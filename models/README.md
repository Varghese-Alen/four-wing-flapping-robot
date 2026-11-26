# Exchange models

Two complete STEP assemblies are supplied in millimetres. They are reference geometry, not manufacturing or energisation authority.

| File | Contents | Solids |
| --- | --- | ---: |
| `aircraft-reference-DC1.step` | Current DC1/WM1 aircraft reference, about 42 g planning mass | 540 |
| `bench-assembly-FE1.step` | Current FE1 bench, reduced test article and complete enclosure | 1,096 |

The aircraft neutral-pose bounds are approximately 306.405 × 120.744 × 152.600 mm. The 330 mm design span is a planning envelope, not that pose's projected width. The complete bench bounds are 950.000 × 924.800 × 661.000 mm; these include the complete layout, not only the enclosure floor.

These are new neutral-header derivatives of the retained exchange exports. Geometry data sections are unchanged. Solid counts and bounds were read back and checked; `exchange-checks.json` records those checks. No new collision, structural or fatigue verification is implied. Inspection renders hide selected enclosure panels; this assembly does not.

Hardware licence: [CERN-OHL-P-2.0](../LICENSES/CERN-OHL-P-2.0.txt). Keep the technical description and licence with redistributed models. See [technical notes](../docs/technical-notes.md) before interpreting or using the geometry.
