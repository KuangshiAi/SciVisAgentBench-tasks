# import the simple module from the paraview
from paraview.simple import *

# disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Wavelet'
wavelet1 = Wavelet()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
AssignViewToLayout(renderView1)

# show data in view
wavelet1Display = Show(wavelet1, renderView1)

# reset view to fit data
renderView1.ResetCamera()

# change representation type
wavelet1Display.SetRepresentationType('Surface')

# set scalar coloring
ColorBy(wavelet1Display, ('POINTS', 'RTData'))

# rescale color and/or opacity maps used to include current data range
#wavelet1Display.RescaleTransferFunctionToDataRange(True)

# show color bar/color legend
wavelet1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'RTData'
rTDataLUT = GetColorTransferFunction('RTData')
#rTDataLUT.ApplyPreset('Cool to Warm', True)

# get layout
viewLayout1 = GetLayout()

# split cell
viewLayout1.SplitHorizontal(0, 0.5)

# set active view
SetActiveView(None)

# Create a new 'Histogram View'
histogramView1 = CreateView('XYHistogramChartView')
histogramView1.ViewSize = [500, 780]

# place view in the layout
viewLayout1.AssignView(2, histogramView1)

# set active source
SetActiveSource(wavelet1)

# show data in view
histogram = Show(wavelet1, histogramView1)
# trace defaults for the display properties.
histogram.SelectInputArray = ['POINTS', 'RTData']
histogram.UseColorMapping = True
histogram.LookupTable = rTDataLUT

Render(histogramView1)

# save screenshot
SaveScreenshot('render-histogram/results/{agent_mode}/render-histogram.png', lineChartView1)
