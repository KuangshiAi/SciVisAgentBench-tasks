# Color mapping and calculator functions

- Generates a synthetic wavelet volume, then uses a calculator filter to create a vector field, Result = (RTData, ln(RTData), coordsZ).
- Renders the dataset as a surface in a render view with a blue-gray background, colors by the X component of Result, rescales the transfer functions, shows the scalar bar, and applies the cool-to-warm color map.
- Sets the camera, renders, and saves a screenshot to `color-data-screenshot.png`.

