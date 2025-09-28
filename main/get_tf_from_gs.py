#!/usr/bin/env pvpython

from paraview.simple import *
import os

def load_state_and_inspect_transfer_functions(state_path):
    if not os.path.isfile(state_path):
        raise FileNotFoundError(f"State file not found: {state_path}")

    # Load the ParaView state file
    LoadState(state_path)
    print(f"[✔] Loaded state from: {state_path}")

    # Access the active view
    view = GetActiveViewOrCreate('RenderView')

    # Iterate through all sources to find volume display
    for source in GetSources().values():
        display = GetDisplayProperties(source, view=view)
        if hasattr(display, 'LookupTable') and display.LookupTable:
            lut = display.LookupTable
            otf = display.ScalarOpacityFunction

            print("\n🎨 Color Transfer Function (LUT) — RGBPoints:")
            for i in range(0, len(lut.RGBPoints), 4):
                val = lut.RGBPoints[i]
                r, g, b = lut.RGBPoints[i+1:i+4]
                print(f"  {val:.3f}: R={r:.3f}, G={g:.3f}, B={b:.3f}")

            print("\n🌫️ Opacity Transfer Function (OTF) — Points:")
            for i in range(0, len(otf.Points), 4):
                val = otf.Points[i]
                alpha = otf.Points[i+1]
                print(f"  {val:.3f}: α={alpha:.3f}")

            return lut, otf

    print("❌ No volume rendering transfer function found.")
    return None, None

if __name__ == '__main__':
    base_path = os.path.abspath(os.path.join(__file__, '..'))
    state_file = os.path.join(base_path, 'bonsai_gs.pvsm')
    load_state_and_inspect_transfer_functions(state_file)
