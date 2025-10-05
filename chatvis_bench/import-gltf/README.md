# glTF file reading and window resizing

- Applies a blue-gray background, disables auto camera reset, and gets a render view, then imports a subset of a glTF scene (`NestedRings.glb`) into that view to load only specific nodes: /assembly/Axle, /assembly/OuterRing/Torus002, and /assembly/OuterRing/MiddleRing/InnerRing.
- Retrieves the active source and its display properties, resizes the layout to 300×300, orients the camera to +Y, fits the view, renders, and saves a screenshot to `import-gltf-screenshot.png`.
