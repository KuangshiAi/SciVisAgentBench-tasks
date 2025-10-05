# import the simple module from the paraview
from paraview.simple import *

# create a new 'Wavelet'
wavelet1 = Wavelet()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
renderView1.ViewSize = [400, 400]

# show data in view
wavelet1Display = Show(wavelet1, renderView1)

# reset view to fit data
renderView1.ResetCamera()

# create a new 'Contour'
contour1 = Contour(Input=wavelet1)
contour1.ContourBy = ['POINTS', 'RTData']
contour1.Isosurfaces = [97.222075, 157.09105, 216.96002500000003, 276.829]
contour1.ComputeScalars = 1
contour1.PointMergeMethod = 'Uniform Binning'

# get color transfer function/color map for 'RTData'
rTDataLUT = GetColorTransferFunction('RTData')

# show data in view
contour1Display = Show(contour1, renderView1)
# trace defaults for the display properties.
contour1Display.ColorArrayName = ['POINTS', 'RTData']
contour1Display.LookupTable = rTDataLUT

# save data
plyfilename = "PLYWriterData.ply"
SaveData(plyfilename,
        proxy=contour1, EnableColoring=1,
)

# # save screenshot
SaveScreenshot('write-ply-screenshot.png', renderView1)
