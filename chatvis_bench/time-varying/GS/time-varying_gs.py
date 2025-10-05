from paraview.simple import *
import numpy as np
from vtkmodules.numpy_interface import dataset_adapter as dsa

# load the dataset
data = OpenDataFile("time-varying/data/time-varying.ex2")

# set render view direction
renderView1 = GetActiveViewOrCreate('RenderView')
renderView1.ResetActiveCameraToPositiveY()

# color by "EQPS" variable
dataDisplay = Show(data, renderView1)
dataDisplay.Representation = 'Surface'
ColorBy(dataDisplay, ('CELLS', 'EQPS'))
dataDisplay.RescaleTransferFunctionToDataRange(True)
renderView1.ResetCamera()
Render()

# show color legend
dataDisplay.SetScalarBarVisibility(renderView1, True)

# play animation through time steps
animationScene = GetAnimationScene()
animationScene.Play()

# rescale the data range to the last time step
animationScene.GoToLast()
dataDisplay.RescaleTransferFunctionToDataRange(True)

# play the animation again
animationScene.Play()

# apply a temporal interpolator filter to the dataset
temporalInterpolator = TemporalInterpolator(Input=data)

# create a second render view to the right of the first and link the two views
renderView2 = CreateView('RenderView')
layout1 = CreateLayout(name='Layout')
layout1.SplitHorizontal(0, 0.5)
layout1.AssignView(1, renderView1)
layout1.AssignView(2, renderView2)

# display the interpolated data in the second view
temporalDisplay = Show(temporalInterpolator, renderView2)
temporalDisplay.Representation = 'Surface'
ColorBy(temporalDisplay, ('CELLS', 'EQPS'))
temporalDisplay.RescaleTransferFunctionToDataRange(True)
renderView2.ResetCamera()
Render()

# link the two views and play the animation in both views simultaneously
renderView2.CameraPosition = renderView1.CameraPosition
renderView2.CameraFocalPoint = renderView1.CameraFocalPoint
renderView2.CameraViewUp = renderView1.CameraViewUp
animationScene.Play()

# save the animation to file
SaveAnimation("time-varying/results/{agent_mode}/time-varying.avi", layout1)

# for mean, compute sum of EQPS from each timestep
sum_all         = 0.0
sum_first_half  = 0.0
sum_even        = 0.0
num_all         = 0         # number of cells in all timesteps
num_first_half  = 0         # number of cells in first half of timesteps
num_even        = 0         # number of cells in even timesteps
timesteps       = data.TimestepValues
i               = 0
for t in timesteps:
    data.UpdatePipeline(t)
    mb = dsa.WrapDataObject(FetchData(data)[0])
    eqps_0 = mb.CellData['EQPS'].GetArrays()[0]     # [0] is the block index of block_1
    num_cells = eqps_0.GetNumberOfTuples()

    # all timesteps
    sum_all += np.sum(eqps_0)
    num_all += num_cells

    # first half of timesteps
    if i < len(timesteps) / 2:
        sum_first_half += np.sum(eqps_0)
        num_first_half += num_cells

    # even timesteps
    if i % 2 == 0:
        sum_even += np.sum(eqps_0)
        num_even += num_cells

    i += 1

# compute mean
mean_all        = sum_all / num_all
mean_first_half = sum_first_half / num_first_half
mean_even       = sum_even / num_even

# for variance, compute sum of squares of EQPS - mean from each timestep
sumsq_all = 0.0
for t in timesteps:
    animationScene.TimeKeeper.Time = t
    data.UpdatePipeline()
    mb = dsa.WrapDataObject(FetchData(GetActiveSource())[0])
    eqps_0 = mb.CellData['EQPS'].GetArrays()[0]     # [0] is the block index of block_1
    num_cells = eqps_0.GetNumberOfTuples()

    # all timesteps
    for j in range(num_cells):
        sumsq_all += (eqps_0[j] - mean_all) * (eqps_0[j] - mean_all)

# compute variance
var_all = sumsq_all / num_all

# print stats
print("Average EQPS over all time steps:", mean_all)
print("Average EQPS over first half of time steps:", mean_first_half)
print("Average EQPS over even numbered time steps:", mean_even)
print("Variance of EQPS over all time steps:", var_all)

