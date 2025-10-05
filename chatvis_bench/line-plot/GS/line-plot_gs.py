from paraview.simple import *
import os

# — Paths & setup —
base      = os.path.abspath(os.path.join(__file__, '..', '..'))
data_path  = os.path.join(base, 'data', 'line-plot.ex2')
result_dir = os.path.join(base, 'results', 'pvpython')
state     = os.path.join(result_dir, 'line-plot.pvsm')
# read dataset
reader = OpenDataFile(data_path)

# print values
pd = reader.PointData
for ai in pd.values():
   print(ai.GetName(), ai.GetNumberOfComponents(), end=" ")
   for i in range(ai.GetNumberOfComponents()):
      print(ai.GetRange(i), end=" ")
   print()

# color by pressure "Pres"
# readerRep = GetRepresentation()
renderView1 = GetActiveViewOrCreate('RenderView')
dataDisplay = Show(reader, renderView1)
ColorBy(dataDisplay, ("POINTS", "Pres"))
UpdateScalarBars()
Show()
Render()

# create a line plot
plot = PlotOverLine()
plot.Point1 = [0, 0, 0]
plot.Point2 = [0, 0, 10]
writer = CreateWriter(os.path.join(result_dir, "line-plot.csv"))
writer.UpdatePipeline()

# save the plot
plotView = FindViewOrCreate("MyView", viewtype="XYChartView")
Show(plot)
Render()
os.makedirs(result_dir, exist_ok=True)
SaveScreenshot(os.path.join(result_dir, 'line-plot.png'))
SaveState(state)

