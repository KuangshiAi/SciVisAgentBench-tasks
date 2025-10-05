# Streamline tracing

- Loads the dataset `disk.ex2` and computes extents to position a camera centered on the domain and offset along −X with Z-up.
- Builds streamlines from the point-data vector field V using a point cloud seeder (specified center/radius and maximum length).
- Uses tubes along the streamlines for thickened paths, and places cone glyphs along them oriented/scaled by V to show flow direction and magnitude.
- Renders both tubes and glyphs colored by the scalar Temp (rescaled to data range) and saves a 1920×1080 screenshot at `stream-glyph-screenshot.png`.
