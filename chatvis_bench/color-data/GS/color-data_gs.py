# import the simple module from the paraview
from paraview.simple import *

# disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

LoadPalette("BlueGrayBackground")

# create a new 'Wavelet'
wavelet1 = Wavelet()

# set active source
SetActiveSource(wavelet1)

# create a new 'Calculator'
calculator1 = Calculator(Input=wavelet1)
calculator1.Function = ''

# Properties modified on calculator1
calculator1.Function = 'RTData*iHat + ln(RTData)*jHat + coordsZ*kHat'

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
renderView1.ViewSize = [1158, 833]

# show data in view
calculator1Display = Show(calculator1, renderView1)

# trace defaults for the display properties.
calculator1Display.Representation = 'Outline'
calculator1Display.ColorArrayName = ['POINTS', '']

# get color transfer function/color map for 'Result'
ResultLUT = GetColorTransferFunction('Result')

# get opacity transfer function/opacity map for 'Result'
ResultPWF = GetOpacityTransferFunction('Result')

# change representation type
calculator1Display.SetRepresentationType('Surface')

# set scalar coloring
ColorBy(calculator1Display, ('POINTS', 'Result', 'X'))

# rescale color and/or opacity maps used to include current data range
calculator1Display.RescaleTransferFunctionToDataRange(True)

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# Update a scalar bar component title.
UpdateScalarBarsComponentTitle(ResultLUT, calculator1Display)

ResultLUT.ApplyPreset("Cool to Warm", True)

# current camera placement for renderView1
renderView1.CameraPosition = [0.0, 0.0, 82.35963323102031]
renderView1.CameraParallelScale = 21.57466795392812

Render(renderView1)

# save screenshot
SaveScreenshot('color-data/results/{agent_mode}/color-data.png', renderView1)
