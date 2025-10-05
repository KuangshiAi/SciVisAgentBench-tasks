# Time series IO, slicing, VTK blocks

- Opens the dataset `can.ex2` with two hex-element blocks, and extracts a planar slice normal along +X, origin at [0.21706, 4.0, −5.11095].
- Writes the slice over a subseries of timesteps to a VTM file series (timesteps 10, 13, 16, 19) using a filename suffix for the timestep.
- Reads the generated multiblock files back, displays them in a render view, and saves a screenshot to `subseries-of-time-series-screenshot.png`.
