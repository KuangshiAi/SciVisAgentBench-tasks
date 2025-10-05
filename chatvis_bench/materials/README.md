# Side-by-side comparison of an isovolume featuring clipping, labeling, and color mapping

- Sets up a side-by-side layout with two render views to compare a prediction (`neg10_prediction.vtr`) vs ground-truth (`neg10_ground_truth.vtr`) dataset.
- For each, converts cell data (Intensity, Phase) to point data, extracts an isovolume on Intensity in [0.2, 1.0], then applies a clipping plane at origin (32,32,32), and colors the result by Phase using a Viridis colormap with visible scalar bars.
- Adds text overlays (“NN Prediction” and “Ground Truth”), aligns both cameras to −Z with a 45° yaw for consistent views, and saves a combined screenshot of the layout to `comparison-screenshot.png.`
