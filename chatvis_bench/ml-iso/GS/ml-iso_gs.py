from paraview.simple import *

# read the input data
ml100vtk = LegacyVTKReader(registrationName='ml-iso.vtk', FileNames=['ml-iso/data/ml-iso.vtk'])

# create a new contour
contour1 = Contour(registrationName='Contour1', Input=ml100vtk)
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

# save screenshot
SaveScreenshot('ml-iso/results/{agent_mode}/ml-iso.png', renderView, ImageResolution=[1920, 1080])


