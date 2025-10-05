from paraview.simple import *

# create a sphere object
sphere = Sphere()

# create a shrink filter
shrink = Shrink()

# double the sphere resolution
sphere.ThetaResolution = sphere.ThetaResolution * 2;

# halve the shrink factor
shrink.ShrinkFactor = shrink.ShrinkFactor / 2;

# extract a wireframe of the sphere
wireframe = ExtractEdges(Input=sphere)

# group the shrink filter and wireframe outputs
group = GroupDatasets(Input=[shrink, wireframe])
Show()
Render()

# save screenshot
SaveScreenshot('shrink-sphere/results/{agent_mode}/shrink-sphere.png', ImageResolution=[1920, 1080], OverrideColorPalette='WhiteBackground')


