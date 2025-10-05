# Chart plotting

- Opens the dataset `disk_out_ref.ex2`, inspects its point-data arrays, and prints each array’s name, component count, and per-component value ranges.
- Renders the dataset in a 3D view colored by the point-data scalar "Pres" (pressure), updating scalar bars and showing the result.
- Extracts a 1D sampling of the data along a line from (0,0,0) to (0,0,10), and writes that sampled profile to line-plot.csv.
- Displays the line-sample in an XY chart view and saves a screenshot (`line-plot.png`), of the chart view.
