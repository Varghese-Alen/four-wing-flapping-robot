# Theme-matched media

Copyright © 2026 Alen Mammen Varghese. Original rendered media and numerical figures: CC-BY-4.0. See `../LICENSES/`, `../LICENSING.md` and the retained third-party credits in `../NOTICE.md`.

Appearance-only refresh: light background `#F2EADC`, dark background `#101211`. Both themes use the same cached geometry, poses and cameras. The dark theme lifts charcoal and plum-bar surface contrast; it does not remove dark parts. Film remains 80% opaque with per-pixel depth ordering. Soft shadows come from the projected geometry, not cut-outs or colour-key replacement. No geometry, scientific values or prescribed motion was changed.

## Files

Each `{theme}` is `light` or `dark`.

- `hero-{theme}-{1600,800}.webp`, `anatomy-{theme}-{1600,800}.webp`, `drive-{theme}-{1600,800}.webp`, `bench-{theme}-{1600,800}.webp`, `bench-mount-{theme}-{1600,800}.webp`: 1600 × 1200 and 800 × 600.
- `card-{theme}.webp`: 1200 × 900.
- `strokes-{theme}-{1800,900}.webp`: 1800 × 600 and 900 × 300; the three retained top, mid and bottom prescribed states, not invented deformation.
- `motion-{theme}.mp4` and `motion-poster-{theme}.webp`: 1280 × 960.
- `result-bars-{theme}-{1600,800}.webp`: 1600 × 900 and 800 × 450; matching `result-bars-{theme}.svg`.
- `stiffness-map-{theme}-{1600,800}.webp`: 1600 × 1200 and 800 × 600; matching `stiffness-map-{theme}.svg`.

The front anatomy image is unlabelled. The refined drive camera uses distance 250 with no depth softness. The bench retains the existing inspection-panel selection, not an operating configuration. The mount view retains only the existing mount and fixed sideplate selection, with the original slight depth softness.

## Motion and numerical limits

Each silent clip has 360 display frames at 60 fps: six seconds, two cycles, 60 prescribed phase states per cycle, each held for three display frames. It depicts the retained 20 Hz prescription at 60× slowdown. Fast gears are temporally undersampled and may appear stationary or reverse. Elastic bars and wiring are omitted from the motion and stroke strip because no valid deformation sequence exists. There is no invented wing warping or wake, and no claim of measured or flight behaviour.

The chart generator is `../tools/make_website_plots.py`. Lato text, exterior backgrounds, ticks and labels follow the themes. The field retains its neutral/blue/plum palette and all 1,694 values (121 × 14), including 137 negative cases, on the unchanged −60 to +60 scale with 12 intervals. Units, baselines, field lines and reference markers are retained. The saving-field digest is `fc8ad6a1589ef62882287f25dbd3abb460a0699fc48eb29c5b2f57d8245a9831` (row-major little-endian 64-bit values). These are conditional calculated mechanical results, not electrical or experimental measurements.

`fonts/Lato-Regular.ttf` is the retained Lato typeface, distributed under `../LICENSES/OFL-Lato.txt`. The chart script registers it explicitly; vector lettering uses glyph outlines for consistent display.
