from paraview.simple import *

LoadPalette("BlueGrayBackground")

wavelet = Wavelet()
SetActiveSource(wavelet)
view = GetActiveViewOrCreate('RenderView')
disp = GetDisplayProperties(wavelet, view)
disp.Representation = "Surface With Edges"
Show(wavelet, view)
direction = [0.5, 1, 0.5]

ResetCameraToDirection(view.CameraFocalPoint, direction)

# save screenshot
SaveScreenshot('reset-camera-direction/results/{agent_mode}/reset-camera-direction.png', renderView1)
