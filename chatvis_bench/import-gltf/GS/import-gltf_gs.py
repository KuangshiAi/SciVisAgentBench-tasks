# import the simple module from the paraview
from paraview.simple import *

LoadPalette("BlueGrayBackground")

# disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# import file
ImportView('NestedRings.glb', view=renderView1, NodeSelectors=['/assembly/Axle', '/assembly/OuterRing/Torus002', '/assembly/OuterRing/MiddleRing/InnerRing'])

# get active source.
innerRing_Torus001 = GetActiveSource()

# get display properties
innerRing_Torus001Display = GetDisplayProperties(innerRing_Torus001, view=renderView1)

# get layout
layout1 = GetLayout()

# layout/tab size in pixels
layout1.SetSize(300, 300)

renderView1.ResetActiveCameraToPositiveY()

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# Render all views to see them appears
RenderAllViews()

# save screenshot
SaveScreenshot('import-gltf-screenshot.png', renderView1)
