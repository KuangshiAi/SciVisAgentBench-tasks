from paraview.simple import *

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [900, 1400]

# Create a new 'Render View'
renderView2 = CreateView('RenderView')
renderView2.ViewSize = [900, 1400]

SetActiveView(None)

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.SplitHorizontal(0, 0.500000)
layout1.AssignView(1, renderView1)
layout1.AssignView(2, renderView2)
layout1.SetSize(1800, 1400)

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'XML Rectilinear Grid Reader'
ground_truthvtr = XMLRectilinearGridReader(registrationName='materials_ground_truth.vtr', FileName=['materials/data/materials_ground_truth.vtr'])
# ground_truthvtr = XMLRectilinearGridReader(registrationName='ground_truth.vtr', FileName=['/Users/tpeterka/software/ChatVis-full-paper/examples/science-cases/materials/neg10_ground_truth.vtr'])
ground_truthvtr.CellArrayStatus = ['Intensity', 'Phase']

# create a new 'Cell Data to Point Data'
cellDatatoPointData2 = CellDatatoPointData(registrationName='CellDatatoPointData2', Input=ground_truthvtr)
cellDatatoPointData2.CellDataArraytoprocess = ['Intensity', 'Phase']

# create a new 'Iso Volume'
isoVolume2 = IsoVolume(registrationName='IsoVolume2', Input=cellDatatoPointData2)
isoVolume2.InputScalars = ['POINTS', 'Intensity']
isoVolume2.ThresholdRange = [0.2, 1.0]

# create a new 'XML Rectilinear Grid Reader'
predictionvtr = XMLRectilinearGridReader(registrationName='materials_prediction.vtr', FileName=['materials/data/materials_prediction.vtr'])
# predictionvtr = XMLRectilinearGridReader(registrationName='prediction.vtr', FileName=['/Users/tpeterka/software/ChatVis-full-paper/examples/science-cases/materials/neg10_prediction.vtr'])
predictionvtr.CellArrayStatus = ['Intensity', 'Phase']

# create a new 'Cell Data to Point Data'
cellDatatoPointData1 = CellDatatoPointData(registrationName='CellDatatoPointData1', Input=predictionvtr)
cellDatatoPointData1.CellDataArraytoprocess = ['Intensity', 'Phase']

# create a new 'Iso Volume'
isoVolume1 = IsoVolume(registrationName='IsoVolume1', Input=cellDatatoPointData1)
isoVolume1.InputScalars = ['POINTS', 'Intensity']
isoVolume1.ThresholdRange = [0.2, 1.0]

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=isoVolume1)
clip1.ClipType = 'Plane'

# init the 'Plane' selected for 'ClipType'
clip1.ClipType.Origin = [32.0, 32.0, 32.0]

# create a new 'Text'
text1 = Text(registrationName='Text1')
text1.Text = 'NN Prediction'

# create a new 'Text'
text2 = Text(registrationName='Text2')
text2.Text = 'Ground Truth'

# create a new 'Clip'
clip2 = Clip(registrationName='Clip2', Input=isoVolume2)
clip2.ClipType = 'Plane'

# init the 'Plane' selected for 'ClipType'
clip2.ClipType.Origin = [32.0, 32.0, 32.0]

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# get color transfer function/color map for 'Phase'
phaseLUT = GetColorTransferFunction('Phase')
phaseLUT.ApplyPreset("Viridis (matplotlib)")

# show data from clip1
clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')
clip1Display.ColorArrayName = ['POINTS', 'Phase']
clip1Display.LookupTable = phaseLUT
clip1Display.RescaleTransferFunctionToDataRange(True)
clip1Display.SetScalarBarVisibility(renderView1, True)

# show data from text1
text1Display = Show(text1, renderView1, 'TextSourceRepresentation')
text1Display.Color = [0.0, 0.0, 0.0]
text1Display.FontFamily = 'Times'
text1Display.FontSize = 60

# get color legend/bar for phaseLUT in view renderView1
phaseLUTColorBar = GetScalarBar(phaseLUT, renderView1)
phaseLUTColorBar.WindowLocation = 'Any Location'
phaseLUTColorBar.Position = [0.8175077041602465, 0.01181592039800995]
phaseLUTColorBar.Title = 'Phase'
phaseLUTColorBar.ComponentTitle = ''
phaseLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
phaseLUTColorBar.TitleFontFamily = 'Times'
phaseLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
phaseLUTColorBar.LabelFontFamily = 'Times'
phaseLUTColorBar.Visibility = 1

# ----------------------------------------------------------------
# setup the visualization in view 'renderView2'
# ----------------------------------------------------------------

# show data from clip2
clip2Display = Show(clip2, renderView2, 'UnstructuredGridRepresentation')
clip2Display.ColorArrayName = ['POINTS', 'Phase']
clip2Display.LookupTable = phaseLUT
clip2Display.RescaleTransferFunctionToDataRange(True)
clip2Display.SetScalarBarVisibility(renderView2, True)

# show data from text2
text2Display = Show(text2, renderView2, 'TextSourceRepresentation')
text2Display.Color = [0.0, 0.0, 0.0]
text2Display.FontFamily = 'Times'
text2Display.FontSize = 60

# get color legend/bar for phaseLUT in view renderView2
phaseLUTColorBar_1 = GetScalarBar(phaseLUT, renderView2)
phaseLUTColorBar_1.Title = 'Phase'
phaseLUTColorBar_1.ComponentTitle = ''
phaseLUTColorBar_1.TitleColor = [0.0, 0.0, 0.0]
phaseLUTColorBar_1.TitleFontFamily = 'Times'
phaseLUTColorBar_1.LabelColor = [0.0, 0.0, 0.0]
phaseLUTColorBar_1.LabelFontFamily = 'Times'
phaseLUTColorBar_1.Visibility = 1

# set camera direction
SetActiveView(renderView1)
renderView1.ResetActiveCameraToNegativeZ()
camera = GetActiveCamera()
camera.Yaw(45)
renderView1.ResetCamera(True, 0.9)

SetActiveView(renderView2)
renderView2.ResetActiveCameraToNegativeZ()
camera = GetActiveCamera()
camera.Yaw(45)
renderView2.ResetCamera(True, 0.9)

# ----------------------------------------------------------------
# save screenshot
# ----------------------------------------------------------------

SaveScreenshot("materials/results/{agent_mode}/materials.png", layout1)
