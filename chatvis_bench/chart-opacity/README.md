# Chart plotting with background modification

- Creates a synthetic wavelet volume, shows it as an outline in a 3D render view, then samples it over a line and displays the sampled data both as geometry in 3D and as an XY chart.
- Adds the chart view to the main layout and customizes the chart’s series: sets line thickness to 2, solid style, no markers, reduces opacity for most series while keeping arc_length fully opaque, and makes arc_length, Points_Z, and RTData visible.
- Saves a screenshot of the chart view to `chart-opacity-screenshot.png`.
