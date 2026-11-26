# Media specification

## Visual system

The website keeps its existing light and dark themes. The light page is `#F2EADC`; the dark page is `#101211`. Text, navigation, rules and expanded notes inherit the site's theme tokens. The drone follows the PC-case article layout, type scale, numbered headings, captions and disclosure pattern. Geometry images have two rendered variants: `#F2EADC` in light mode and `#101211` in dark mode. Dark display materials receive a restrained contrast lift so small structure remains visible. This is appearance only, not a material or geometry change. No colour threshold removes objects or film. The scientific field palette is unchanged in both modes; its pale regions are data, not background to erase.

The restrained accents are plum `#48252F`, green `#2F4A3A`, bronze `#857861` and muted blue. Plum identifies the torsion bars and selected stiffness comparison; green identifies the fixed setting in the bar chart. Render colours are display choices, not adopted material changes or mass and strength evidence.

The views reuse the actual aircraft and current bench geometry. Diffuse lighting, a soft projected mesh shadow and a 70 mm equivalent perspective are local raster approximations, not path traced photography. Front and stroke views are orthographic. Distal wings are intentionally outside the drive detail frame. The complete aircraft and bench inspection views are not detail crops.

Captions and explanations are live text outside the images. Necessary scientific axes, units, values and colour bars remain inside the charts. No decorative branding is added to the model views.

## Asset dimensions

| Assets | Large | Small | Format |
| --- | --- | --- | --- |
| `hero`, `anatomy`, `drive`, `bench`, `bench-mount` | 1600 × 1200 | 800 × 600 | WebP |
| `card` | 1200 × 900 | Not required | WebP |
| `strokes` | 1800 × 600 | 900 × 300 | WebP |
| `result-bars` | 1600 × 900 | 800 × 450 | SVG and WebP |
| `stiffness-map` | 1600 × 1200 | 800 × 600 | SVG and WebP |
| `motion-poster` | 1280 × 960 | Responsive display | WebP |
| `motion` | 1280 × 960 | Responsive display | MP4 |

Every listed asset has a light and dark variant. WebP figures use responsive `srcset` selection and intrinsic dimensions. The card uses a 4:3 frame. Full SVG chart links remain available because small embedded labels are not the sole mobile explanation. `media/asset-manifest.json` records actual file dimensions, sizes and hashes.

## Motion

Each theme MP4 is H.264, 1280 × 960, 60 frames per second and six seconds, with no audio. It contains two cycles of the exact retained 20 Hz geometric prescription at 60 times slower speed. Each cycle has 60 distinct rendered states; each state is held for three video frames. Fast gear rotation is therefore undersampled. Controls are visible; there is no automatic playback. Motion stops when leaving the article or hiding the tab. Theme changes retain its time and manual playing state where browser policy permits.

The spring bars and wiring are omitted from moving and nonneutral stroke views because no valid deformed sequence is available. The static neutral views retain their authentic geometry. The video does not show solved motor response, wakes, airflow, elastic modes or flight. The stroke strip is ordered left, middle, right for the right front root: approximately +24°, 0°, −24°. Other roots have their prescribed opposite signs. These are root angles, not screen angles. The front projection mainly changes projected span; the perspective clip shows the stroke more clearly.

## Numerical figures

The bar chart reads exact saved mission values. The field chart retains all 1,694 values, 137 negative cases and the original −60 to +60% scale with 12 filled intervals. Its custom blue to neutral to plum palette has matched lightness on its two arms; no certified perceptual uniformity is claimed. Filled contours interpolate the retained samples. They are not additional simulation cases. The numerical readout also provides a separate discrete sampled grid SVG.

To redraw the website charts from the repository root, install NumPy, Matplotlib and Pillow, then run `python3 tools/make_website_plots.py`. These are optional display dependencies, not bundled distributions. The run used NumPy 2.5.4, Matplotlib 3.10.9 and Pillow 13.0.0; the bundled licensed Lato font fixes chart typography without changing data. The numerical readout has its own narrower requirements.

## Inspection views

The bench overview hides selected enclosure panels, cover and door to expose the fixture. The mount detail shows selected existing fixture and fixed frame components, not the complete test article. Neither is an operating arrangement. The STEP bench assembly retains the full geometry. The separate proof bypass is not shown as an alternative normal measurement load path.
