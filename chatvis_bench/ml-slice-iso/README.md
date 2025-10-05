# Slicing followed by contouring

- Loads the dataset `ml-100.vtk`, slices it with a plane (at offset 0) to produce a 2D cut, then applies a contour filter on the slice to extract the var0 isovalue 0.5 (yielding isolines on the slice).
- Creates a 1920×1080 render view, displays the contour with no scalar coloring (solid red), orients the camera to the +X direction and fits the view, and saves a white‑background screenshot to `ml-slice-iso-screenshot.png`.
