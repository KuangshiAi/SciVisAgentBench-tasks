# import the simple module from the paraview
from paraview.simple import *

LoadPalette("BlueGrayBackground")

# create a new 'IOSS Reader'
canex2 = IOSSReader(registrationName='color-blocks.ex2', FileName='color-blocks/data/color-blocks.ex2')

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
canex2Display = Show(canex2, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
canex2Display.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(canex2Display, ('FIELD', 'vtkBlockColors'))

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')

# get opacity transfer function/opacity map for 'vtkBlockColors'
vtkBlockColorsPWF = GetOpacityTransferFunction('vtkBlockColors')

# get 2D transfer function for 'vtkBlockColors'
vtkBlockColorsTF2D = GetTransferFunction2D('vtkBlockColors')

# set block scalar coloring
ColorBlocksBy(canex2Display, ['/IOSS/element_blocks/block_2'], ('POINTS', 'ACCL', 'X'))

# rescale block color and/or opacity maps used to exactly fit the current data range
canex2Display.RescaleBlocksTransferFunctionToDataRange(['/IOSS/element_blocks/block_2'], False, True)

# get color transfer function/color map for 'ACCl'
blockACCLLUT = GetBlockColorTransferFunction('/IOSS/element_blocks/block_2', 'ACCL')

# show block color bar/color legend
canex2Display.SetBlocksScalarBarVisibility(renderView1, ['/IOSS/element_blocks/block_2'], True)

blockACCLLUT.ApplyPreset("Cool to Warm", True)

# reset active camera to negative y
renderView1.ResetActiveCameraToNegativeY()

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# save screenshot
SaveScreenshot('color-blocks/results/{agent_mode}/color-blocks.png', renderView1)
