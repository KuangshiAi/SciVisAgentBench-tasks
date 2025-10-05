# Color mapping of VTK blocks

- Loads the dataset `can.ex2`, applies a blue-gray background, shows it as a surface in a render view, and fits the camera.
- Uses block coloring globally, then overrides one block (/IOSS/element_blocks/block_2) to be colored by the X component of the point-data array ACCL, rescales that block’s transfer function to its data range, shows its scalar bar, and applies the cool-to-warm color map.
- Orients the camera to −Y, refits, and saves a screenshot to `color-blocks-screenshot.png`.
