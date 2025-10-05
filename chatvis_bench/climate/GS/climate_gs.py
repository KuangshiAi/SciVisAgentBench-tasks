from paraview.simple import *

# create a new 'XML PolyData Reader'
mpasvtp = XMLPolyDataReader(registrationName='climate.vtp', FileName=['climate/data/climate.vtp'])

# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=mpasvtp)
calculator1.Function = '(-velocity_X*sin(coordsX*0.0174533) + velocity_Y*cos(coordsX*0.0174533)) * iHat + (-velocity_X * sin(coordsY*0.0174533) * cos(coordsX*0.0174533) - velocity_Y * sin(coordsY*0.0174533) * sin(coordsX*0.0174533) + velocity_Z * cos(coordsY*0.0174533)) * jHat + 0*kHat'

# create a new 'Tube'
tube1 = Tube(registrationName='Tube1', Input=mpasvtp)
tube1.Scalars = ['POINTS', 'Result']
tube1.Vectors = ['POINTS', 'Result']
tube1.Radius = 0.05

# create a new 'Glyph'
glyph1 = Glyph(registrationName='Glyph1', Input=calculator1, GlyphType='Cone')
glyph1.OrientationArray = ['POINTS', 'Result']
glyph1.ScaleFactor = 0.5
glyph1.GlyphType.Resolution = 10
glyph1.GlyphType.Radius = 0.15
glyph1.GlyphType.Height = 0.5

# create new render view
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [2294, 1440]

# create new layout object
layout1 = CreateLayout(name='Layout')
layout1.AssignView(0, renderView1)

# get color transfer function/color map for 'velocity'
velocityLUT = GetColorTransferFunction('velocity')
velocityLUT.ApplyPreset("Cool to Warm", True)

# show data from glyph1
glyph1Display = Show(glyph1, renderView1, 'GeometryRepresentation')
glyph1Display.Representation = 'Surface'
glyph1Display.ColorArrayName = ['POINTS', 'velocity']
glyph1Display.LookupTable = velocityLUT
glyph1Display.RescaleTransferFunctionToDataRange()

# show data from tube1
tube1Display = Show(tube1, renderView1, 'GeometryRepresentation')
tube1Display.Representation = 'Surface'
tube1Display.ColorArrayName = ['POINTS', 'velocity']
tube1Display.LookupTable = velocityLUT
tube1Display.Specular = 1.0
tube1Display.RescaleTransferFunctionToDataRange()

# get color legend/bar for velocityLUT in view renderView1
velocityLUTColorBar = GetScalarBar(velocityLUT, renderView1)
velocityLUTColorBar.Title = 'velocity'
velocityLUTColorBar.ComponentTitle = 'Magnitude'
velocityLUTColorBar.Visibility = 1

# set camera direction
renderView1.ResetActiveCameraToNegativeZ()
renderView1.ResetCamera(True, 0.9)

SaveScreenshot("climate/results/{agent_mode}/climate.png", renderView1, ImageResolution=[2294, 1440], OverrideColorPalette='WhiteBackground')
