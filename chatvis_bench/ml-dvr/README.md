# Direct volume rendering

- Loads the dataset `ml-100.vtk`, fetches the range of the first point-data array var0, and builds custom transfer functions: a color map transitioning from blue (min) to gray (mid) to red (max), and an opacity map ramping from transparent at min to opaque at max.
- Creates a 1920×1080 render view with a specified camera, displays the dataset using volume rendering, applies the var0 color and opacity transfer function, and saves a screenshot (`ml-dvr-screenshot.png`).
