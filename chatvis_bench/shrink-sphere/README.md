# Shrink filter and wireframe rendering

- Creates a sphere source, applies a shrink filter to the active sphere (then halves the shrink factor to shrink pieces more) and doubles the sphere’s resolution for finer longitudinal tessellation.
- Extracts a wireframe from the original sphere surface, then groups the shrunken surface and the wireframe together so both render simultaneously.
- Shows the grouped output, renders, and saves a white‑background screenshot to `shrink-sphere.png` at 1920×1080.
