# Streamline tracing with lat-long to geospatial conversion, tube and glyph rendering, with lighting and specularity

- Reads MPAS-Ocean polydata (`mpas.vtp`), computes a transformed vector field Result with a calculator that combines velocity_X/Y/Z with longitude/latitude (coordsX/coordsY in degrees converted to radians) to produce tangential components (iHat/jHat) on the sphere, zeroing kHat.
- Visualizes vectors with cone glyphs oriented by Result and a tube filter applied to the input polydata; both glyphs and tubes are colored by the velocity magnitude using a cool-to-warm color transfer function  with a visible scalar bar.
- Sets camera to look along −Z, maximizes tube specularity, and saves a high-resolution screenshot on a white background (`soma-screenshot.png`).
