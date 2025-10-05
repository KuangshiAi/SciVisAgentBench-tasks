# glTF file writing

- Sets a blue-gray background, creates a wavelet, shows it as a surface colored by RTData, fits the camera, and exports the view to a glTF file (`ExportedGLTF.gltf`).
- Reads the exported glTF back, displays it as a surface, and verifies exported texture coordinates by coloring with the magnitude of TEXCOORD_0 using the cool-to-warm transfer function, with axes hidden and camera reset.
- Saves a screenshot of the reloaded glTF rendering to `export-gltf-screenshot.png`.
