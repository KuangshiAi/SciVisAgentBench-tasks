# Temporal interpolation and animation rendering

- Loads the dataset `can.ex2`, shows it in a render view colored by the cell scalar EQPS with a visible scalar bar, orients the camera to +Y, and plays the time animation.
- Jumps to the last timestep to rescale the color transfer function and replays the animation.
- Builds a temporal interpolator, creates a side-by-side second render view, displays the interpolated data colored by EQPS, links the two cameras, plays both views in sync, and saves the animation to `time-varying.avi`.
- Iterates over all timesteps to fetch EQPS cell data and computes statistics: mean over all timesteps, mean over the first half, mean over even timesteps, and the variance over all timesteps, which are printed at the end.
