import sys
from paraview.simple import *

dataFile = 'can.ex2'

# create a new 'ExodusIIReader'
canex2 = ExodusIIReader(FileName=[dataFile])

# Properties modified on canex2
canex2.ElementBlocks = ['Unnamed block ID: 1 Type: HEX', 'Unnamed block ID: 2 Type: HEX']

renderView1 = GetActiveViewOrCreate('RenderView')

# create a new 'Slice'
slice1 = Slice(Input=canex2)
slice1.SliceType = 'Plane'

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [0.21706008911132812, 4.0, -5.110947132110596]
slice1.SliceType.Normal = [1.0, 0.0, 0.0]
slice1.SliceType.Offset = 0.0

# save data
from os.path import join
SaveData('canslices.vtm', proxy=slice1, Writetimestepsasfileseries=1,
    Firsttimestep=10,
    Lasttimestep=20,
    Timestepstride=3,
    Filenamesuffix='_%d',
    DataMode='Appended',
    HeaderType='UInt64',
    EncodeAppendedData=0,
    CompressorType='None')

# create a new 'XML MultiBlock Data Reader'
canslices = XMLMultiBlockDataReader(FileName=['canslices_10.vtm',
                                              'canslices_13.vtm',
                                              'canslices_16.vtm',
                                              'canslices_19.vtm'])

#canslices.UpdatePipeline()

Show(canslices, renderView1)
SaveScreenshot('subseries-of-time-series-screenshot.png', renderView1)
