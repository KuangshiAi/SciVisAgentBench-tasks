"""
Helper script for taking screenshots from ParaView state files
"""
from paraview.simple import *
import os
import math

def take_screenshots_from_state(state_path, output_dir, prefix="", data_directory=None):
    """
    Load a ParaView state file and take 3 screenshots from different angles
    
    Args:
        state_path (str): Path to the .pvsm state file
        output_dir (str): Directory to save screenshots
        prefix (str): Prefix for screenshot filenames
        data_path (str): Directory of raw data file for state file
    
    Returns:
        list: List of screenshot file paths
    """
    if not os.path.exists(state_path):
        raise FileNotFoundError(f"State file not found: {state_path}")
    
    # Load state file
    if data_directory:
        LoadState(state_path, data_directory=data_directory)
    else:
        LoadState(state_path)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the active view
    renderView = GetActiveViewOrCreate('RenderView')
    
    # Reset camera to fit all data
    renderView.ResetCamera()
    
    # Get current camera position for reference
    camera = renderView.GetActiveCamera()
    original_position = camera.GetPosition()
    original_focal_point = camera.GetFocalPoint()
    
    # Calculate distance from focal point to position
    distance = math.sqrt(sum([(original_position[i] - original_focal_point[i])**2 for i in range(3)]))
    
    # Define three different camera angles
    angles = [
        {
            'name': 'front',
            'position': [original_focal_point[0], original_focal_point[1], original_focal_point[2] + distance],
            'up': [0, 1, 0]
        },
        {
            'name': 'side',
            'position': [original_focal_point[0] + distance, original_focal_point[1], original_focal_point[2]],
            'up': [0, 0, 1]
        },
        {
            'name': 'diagonal',
            'position': [original_focal_point[0] + distance*0.7, original_focal_point[1] + distance*0.7, original_focal_point[2] + distance*0.7],
            'up': [0, 0, 1]
        }
    ]
    
    screenshot_paths = []
    
    # Take screenshots from different angles
    for angle in angles:
        # Set camera position
        camera.SetPosition(angle['position'])
        camera.SetFocalPoint(original_focal_point)
        camera.SetViewUp(angle['up'])
        
        # Reset camera to ensure proper framing
        renderView.ResetCamera()
        
        # Render the view
        Render()
        
        # Save screenshot
        filename = f"{prefix}{angle['name']}_view.png" if prefix else f"{angle['name']}_view.png"
        screenshot_path = os.path.join(output_dir, filename)
        SaveScreenshot(screenshot_path, renderView, ImageResolution=[1920, 1080])
        screenshot_paths.append(screenshot_path)
    
    return screenshot_paths

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Take 3 screenshots from ParaView state files.")
    parser.add_argument('--gs_state_path', type=str, help='Path to ground truth state file (.pvsm)')
    parser.add_argument('--gs_img_path', type=str, help='Directory to save ground truth screenshots')
    parser.add_argument('--result_state_path', type=str, help='Path to result state file (.pvsm)')
    parser.add_argument('--result_img_path', type=str, help='Directory to save result screenshots')
    parser.add_argument('--data_directory', type=str, default=None, help='Directory containing raw data files (optional)')
    args = parser.parse_args()

    # Validate argument pairs
    if args.gs_state_path and not args.gs_img_path:
        parser.error('If --gs_state_path is provided, --gs_img_path must also be provided.')
    if args.gs_img_path and not args.gs_state_path:
        parser.error('If --gs_img_path is provided, --gs_state_path must also be provided.')
    if args.result_state_path and not args.result_img_path:
        parser.error('If --result_state_path is provided, --result_img_path must also be provided.')
    if args.result_img_path and not args.result_state_path:
        parser.error('If --result_img_path is provided, --result_state_path must also be provided.')

    if args.gs_state_path and args.gs_img_path:
        os.makedirs(args.gs_img_path, exist_ok=True)
        print(f"Taking screenshots for ground truth: {args.gs_state_path} -> {args.gs_img_path}")
        take_screenshots_from_state(args.gs_state_path, args.gs_img_path, prefix="gs_", data_directory=args.data_directory)

    if args.result_state_path and args.result_img_path:
        os.makedirs(args.result_img_path, exist_ok=True)
        print(f"Taking screenshots for result: {args.result_state_path} -> {args.result_img_path}")
        take_screenshots_from_state(args.result_state_path, args.result_img_path, prefix="result_", data_directory=args.data_directory)

if __name__ == "__main__":
    main()
