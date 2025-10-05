from paraview.simple import *

# create a new 'Wavelet'
wavelet1 = Wavelet(registrationName='Wavelet1')

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
wavelet1Display = Show(wavelet1, renderView1, 'UniformGridRepresentation')

# set scalar coloring
ColorBy(wavelet1Display, ('POINTS', 'RTData'))

# change representation type
wavelet1Display.SetRepresentationType('Surface')

# hide color bar/color legend
wavelet1Display.SetScalarBarVisibility(renderView1, False)

# get layout
layout1 = GetLayout()

# layout/tab size in pixels
layout1.SetSize(300, 300)

# current camera placement for renderView1
renderView1.CameraPosition = [30.273897726939246, 40.8733980301544, 43.48927935675712]
renderView1.CameraViewUp = [-0.3634544237682163, 0.7916848767068606, -0.49105594165731975]
renderView1.CameraParallelScale = 17.320508075688775

# save screenshot
SaveScreenshot('save-transparent/results/{agent_mode}/save-transparent.png', renderView1, ImageResolution=[300, 300], TransparentBackground=1)

