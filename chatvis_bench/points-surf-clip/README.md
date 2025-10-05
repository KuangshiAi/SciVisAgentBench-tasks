# Delaunay triangulation followed by clipping

- Loads the dataset `can_points.ex2`, generates a 3D tetrahedralization, then applies a plane clip at the origin with normal along +X (cutting to one side of x=0).
- Sets up a render view with a specified camera, displays the clipped tetrahedral mesh in wireframe, and saves a 1920×1080 screenshot to `points-surf-clip-screenshot.png`.
