#!/usr/bin/env pvpython

import os
from paraview.simple import *

def create_bonsai_visualization():
    # — Paths & setup —
    base      = os.path.abspath(os.path.join(__file__, '..', '..'))
    raw_file  = os.path.join(base, 'data', 'bonsai_256x256x256_uint8.raw')
    state_dir = os.path.join(base, 'results', 'pvpython_state')
    state     = os.path.join(state_dir, 'bonsai.pvsm')
    os.makedirs(state_dir, exist_ok=True)
    if not os.path.isfile(raw_file):
        raise FileNotFoundError(f"Missing raw: {raw_file}")

    # — 1) Load the RAW image —
    reader = ImageReader(FileNames=[raw_file])
    reader.DataScalarType     = 'unsigned char'
    reader.DataByteOrder      = 'LittleEndian'
    reader.DataExtent         = [0, 255, 0, 255, 0, 255]
    reader.DataSpacing        = [1.0, 1.0, 1.0]
    reader.FileDimensionality = 3
    reader.UpdatePipeline()

    # — 2) Volume render setup —
    view = GetActiveViewOrCreate('RenderView')
    view.BackgroundColorMode = 'Single Color'
    view.Background          = [1, 1, 1]

    disp = Show(reader, view)
    disp.SetRepresentationType('Volume')
    disp.ColorArrayName = ['POINTS', 'ImageFile']
    view.ResetCamera()

    # — 3) Transfer functions from extracted GS state —
    ctf = GetColorTransferFunction('ImageFile')
    ctf.ColorSpace = 'RGB'
    ctf.NumberOfTableValues = 1024
    ctf.RGBPoints = [
        0.000,     0.780, 0.522, 0.000,
        37.564,    0.847, 0.565, 0.000,
        61.402,    0.796, 0.757, 0.722,
        88.853,    0.753, 0.753, 0.753,
        118.470,   0.804, 0.737, 0.694,
        129.306,   0.686, 0.357, 0.047,
        156.756,   0.678, 0.345, 0.024,
        239.108,   0.667, 0.333, 0.000,
        255.000,   0.706, 0.016, 0.149
    ]

    otf = GetOpacityTransferFunction('ImageFile')
    otf.Points = [
        0.000,     0.000, 0.5, 0.0,
        32.507,    0.000, 0.5, 0.0,
        32.507,    0.360, 0.5, 0.0,
        39.731,    0.455, 0.5, 0.0,
        41.176,    0.000, 0.5, 0.0,
        63.569,    0.000, 0.5, 0.0,
        63.569,    0.511, 0.5, 0.0,
        89.575,    0.412, 0.5, 0.0,
        100.411,   0.000, 0.5, 0.0,
        163.980,   0.002, 0.5, 0.0,
        163.980,   0.567, 0.5, 0.0,
        231.161,   0.649, 0.5, 0.0,
        241.275,   0.433, 0.5, 0.0,
        255.000,   1.000, 0.5, 0.0
    ]

    disp.LookupTable           = ctf
    disp.ScalarOpacityFunction = otf

    # — 4) Camera & save —
    cam = view.GetActiveCamera()
    cam.SetPosition(400, 350, 450)
    cam.SetFocalPoint(128, 128, 128)
    cam.SetViewUp(1, 0, 0)
    view.ResetCamera()
    cam.Elevation(15)
    cam.Azimuth(30)
    cam.Zoom(1.0)

    view.StillRender()
    SaveState(state)
    print(f"[✔] Saved gold‑standard PVSM:\n    {state}")

if __name__ == '__main__':
    create_bonsai_visualization()
