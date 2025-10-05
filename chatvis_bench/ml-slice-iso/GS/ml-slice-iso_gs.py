from paraview.simple import *

# read the input data
ml100vtk = LegacyVTKReader(registrationName='ml-slice-iso.vtk', FileNames=['ml-slice-iso/data/ml-slice-iso.vtk'])

# create a new slice
slice1 = Slice(registrationName='Slice1', Input=ml100vtk)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]
slice1.PointMergeMethod = 'Uniform Binning'

# create a new contour
contour1 = Contour(registrationName='Contour1', Input=slice1)
contour1.ContourBy = ['POINTS', 'var0']
contour1.Isosurfaces = [0.5]
contour1.PointMergeMethod = 'Uniform Binning'

# create new render view
renderView = CreateView('RenderView')
renderView.ViewSize = [1920, 1080]

# create new layout object
layout = CreateLayout(name='Layout')
layout.AssignView(0, renderView)

# show data
contour1Display = Show(contour1, renderView)
contour1Display.ColorArrayName = ['POINTS', '']
contour1Display.DiffuseColor = [1.0, 0.0, 0.0]

# set render view direction
renderView.ResetActiveCameraToPositiveX()
renderView.ResetCamera()

# save screenshot (change path for your machine)
SaveScreenshot('ml-slice-iso/results/{agent_mode}/ml-slice-iso.png', renderView, ImageResolution=[1920, 1080], OverrideColorPalette='WhiteBackground' )

