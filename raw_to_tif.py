import os
import re
import numpy as np
from PIL import Image
import glob
from pathlib import Path


def parse_txt_file(txt_file_path):
    """
    Parse the accompanying txt file to extract metadata.
    Expected format:
    - Name (Scalar/Vector)
    - Data Scalar Type: unsigned char/unsigned short/float
    - Data Byte Order: little Endian/big Endian
    - Data Spacing: 1x1x1 (optional)
    - Data Extent: 256x256x256
    - Number of Scalar Components: 1/3 (for vector data)
    """
    txt_file_path = Path(txt_file_path)
    
    if not txt_file_path.exists():
        raise FileNotFoundError(f"Text file not found: {txt_file_path}")
    
    metadata = {}
    
    with open(txt_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            if line.endswith('(Scalar)') or line.endswith('(Vector)'):
                metadata['name'] = line.split(' (')[0]
                metadata['data_type'] = line.split(' (')[1].rstrip(')')
            elif not metadata.get('name') and not line.startswith('Description:') and not line.startswith('Data '):
                # Handle case where first line is just the name without (Scalar)/(Vector)
                metadata['name'] = line
                metadata['data_type'] = 'Scalar'  # Default assumption
            elif line.startswith('Data Scalar Type:'):
                scalar_type = line.split(': ')[1]
                metadata['scalar_type'] = scalar_type
            elif line.startswith('Data Type:'):
                # Handle format like "Data Type: uint8"
                dtype_str = line.split(': ')[1]
                # Map numpy dtype strings to scalar type strings
                dtype_to_scalar_mapping = {
                    'uint8': 'unsigned char',
                    'uint16': 'unsigned short',
                    'uint32': 'unsigned int',
                    'int8': 'char',
                    'int16': 'short',
                    'int32': 'int',
                    'float32': 'float',
                    'float64': 'double',
                }
                scalar_type = dtype_to_scalar_mapping.get(dtype_str, dtype_str)
                metadata['scalar_type'] = scalar_type
            elif line.startswith('Data Byte Order:'):
                byte_order = line.split(': ')[1]
                metadata['byte_order'] = byte_order
            elif line.startswith('Data Spacing:'):
                spacing = line.split(': ')[1]
                metadata['spacing'] = spacing
            elif line.startswith('Data Extent:'):
                extent = line.split(': ')[1]
                # Parse dimensions from extent (e.g., "256x256x256")
                dimensions = [int(x) for x in extent.split('x')]
                metadata['width'] = dimensions[0]
                metadata['height'] = dimensions[1]
                metadata['depth'] = dimensions[2]
            elif line.startswith('Number of Scalar Components:'):
                components = int(line.split(': ')[1])
                metadata['scalar_components'] = components
    
    return metadata


def get_numpy_dtype(scalar_type, byte_order='little Endian'):
    """Convert string scalar type to numpy dtype with endianness."""
    # Map scalar types to numpy dtypes
    dtype_mapping = {
        'unsigned char': np.uint8,
        'unsigned short': np.uint16,
        'unsigned int': np.uint32,
        'char': np.int8,
        'short': np.int16,
        'int': np.int32,
        'float': np.float32,
        'double': np.float64,
    }
    
    if scalar_type not in dtype_mapping:
        raise ValueError(f"Unsupported scalar type: {scalar_type}")
    
    base_dtype = dtype_mapping[scalar_type]
    
    # Handle endianness - create a dtype object first, then set byte order
    if byte_order.lower() == 'little endian':
        return np.dtype(base_dtype).newbyteorder('<')
    elif byte_order.lower() == 'big endian':
        return np.dtype(base_dtype).newbyteorder('>')
    else:
        # Default to little endian
        return np.dtype(base_dtype).newbyteorder('<')


def parse_filename_fallback(filename):
    """
    Parse filename to extract dimensions and channel information as fallback.
    Expected format: name_widthxheightxdepth_datatype[_scalarN].raw
    Examples:
    - bonsai_256x256x256_uint8.raw (1 channel)
    - tornado_64x64x64_float32_scalar3.raw (3 channels)
    """
    # Remove .raw extension
    name_without_ext = filename.replace('.raw', '')
    
    # Pattern to match: name_widthxheightxdepth_datatype[_scalarN]
    pattern = r'(.+)_(\d+)x(\d+)x(\d+)_(.+?)(?:_scalar(\d+))?$'
    match = re.match(pattern, name_without_ext)
    
    if not match:
        raise ValueError(f"Filename {filename} doesn't match expected pattern")
    
    name, width, height, depth, dtype, scalar_components = match.groups()
    
    # Default to 1 component if not specified
    if scalar_components is None:
        scalar_components = 1
    else:
        scalar_components = int(scalar_components)
    
    return {
        'name': name,
        'width': int(width),
        'height': int(height),
        'depth': int(depth),
        'dtype': dtype,
        'scalar_components': scalar_components
    }


def convert_raw_to_tif(raw_file_path, output_dir=None):
    """
    Convert a raw file to TIFF format.
    
    Args:
        raw_file_path (str): Path to the raw file
        output_dir (str): Directory to save the TIFF file. If None, saves in same directory as raw file.
    
    Returns:
        str: Path to the created TIFF file
    """
    raw_file_path = Path(raw_file_path)
    
    if not raw_file_path.exists():
        raise FileNotFoundError(f"Raw file not found: {raw_file_path}")
    
    # Find the accompanying txt file
    # The txt file is named after the parent's parent folder (e.g., bonsai/data/bonsai.txt)
    txt_file_path = raw_file_path.parent / f"{raw_file_path.parent.parent.name}.txt"
    
    # Try to parse txt file first, but fall back to filename if needed
    metadata = {}
    use_filename_fallback = False
    
    if txt_file_path.exists():
        try:
            metadata = parse_txt_file(txt_file_path)
        except Exception as e:
            print(f"Warning: Could not parse txt file {txt_file_path}: {e}")
            use_filename_fallback = True
    else:
        print(f"Warning: Text file not found: {txt_file_path}")
        use_filename_fallback = True
    
    # Read raw file
    with open(raw_file_path, 'rb') as f:
        raw_data = f.read()
    
    # Get dimensions and dtype - try txt file first, fall back to filename
    if use_filename_fallback:
        print(f"Using filename fallback for {raw_file_path.name}")
        file_info = parse_filename_fallback(raw_file_path.name)
        width, height, depth = file_info['width'], file_info['height'], file_info['depth']
        scalar_components = file_info['scalar_components']
        
        # Map filename dtype to scalar type for consistency
        dtype_mapping = {
            'uint8': 'unsigned char',
            'uint16': 'unsigned short', 
            'uint32': 'unsigned int',
            'int8': 'char',
            'int16': 'short',
            'int32': 'int',
            'float32': 'float',
            'float64': 'double',
        }
        scalar_type = dtype_mapping.get(file_info['dtype'], 'float')
        byte_order = 'little Endian'  # Default assumption
    else:
        width, height, depth = metadata['width'], metadata['height'], metadata['depth']
        scalar_components = metadata.get('scalar_components', 1)
        scalar_type = metadata['scalar_type']
        byte_order = metadata.get('byte_order', 'little Endian')
    
    # Convert to numpy array with proper dtype and endianness
    numpy_dtype = get_numpy_dtype(scalar_type, byte_order)
    array = np.frombuffer(raw_data, dtype=numpy_dtype)
    
    # Calculate expected array size
    expected_size = width * height * depth * scalar_components
    
    # Check if file size matches expected dimensions
    if len(array) != expected_size:
        if not use_filename_fallback:
            print(f"File size mismatch with txt file dimensions. Expected {expected_size}, got {len(array)}")
            print(f"Falling back to filename parsing for {raw_file_path.name}")
            file_info = parse_filename_fallback(raw_file_path.name)
            width, height, depth = file_info['width'], file_info['height'], file_info['depth']
            scalar_components = file_info['scalar_components']
            
            # Recalculate expected size
            expected_size = width * height * depth * scalar_components
            
            if len(array) != expected_size:
                raise ValueError(f"File size doesn't match filename dimensions either. "
                                f"Expected {expected_size} elements, got {len(array)}")
        else:
            raise ValueError(f"File size doesn't match expected dimensions. "
                            f"Expected {expected_size} elements, got {len(array)}")
    
    # Reshape array based on dimensions and components
    if scalar_components == 1:
        # Scalar data: reshape to 3D
        volume = array.reshape((depth, height, width))
        volumes = [volume]  # Single volume
    else:
        # Vector data: reshape to 4D (depth, height, width, components)
        volume_4d = array.reshape((depth, height, width, scalar_components))
        # Split into separate channels
        volumes = [volume_4d[:, :, :, ch] for ch in range(scalar_components)]
    
    # Determine output directory
    if output_dir is None:
        output_dir = raw_file_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create output filenames
    base_filename = raw_file_path.stem
    output_paths = []
    
    # Process each volume (channel)
    for ch_idx, volume in enumerate(volumes):
        if scalar_components > 1:
            output_filename = f"{base_filename}_ch{ch_idx}.tif"
        else:
            output_filename = f"{base_filename}.tif"
        
        output_path = output_dir / output_filename
        
        # Convert to PIL Image and save as TIFF
        # For 3D data, we'll save as a multi-page TIFF
        images = []
        
        for i in range(depth):
            # Extract 2D slice
            slice_2d = volume[i, :, :]
            
            # Normalize data to 0-255 range for display
            if use_filename_fallback:
                scalar_type = scalar_type  # Already set from filename parsing
            else:
                scalar_type = metadata['scalar_type']
            if scalar_type == 'float':
                # Normalize float data
                if slice_2d.max() > slice_2d.min():
                    slice_normalized = ((slice_2d - slice_2d.min()) / 
                                      (slice_2d.max() - slice_2d.min()) * 255).astype(np.uint8)
                else:
                    slice_normalized = np.zeros_like(slice_2d, dtype=np.uint8)
            elif scalar_type == 'unsigned short':
                # Scale uint16 to uint8
                slice_normalized = (slice_2d / 256).astype(np.uint8)
            elif scalar_type == 'unsigned char':
                # uint8 data, use as is
                slice_normalized = slice_2d.astype(np.uint8)
            else:
                # For other types, normalize to 0-255
                if slice_2d.max() > slice_2d.min():
                    slice_normalized = ((slice_2d - slice_2d.min()) / 
                                      (slice_2d.max() - slice_2d.min()) * 255).astype(np.uint8)
                else:
                    slice_normalized = np.zeros_like(slice_2d, dtype=np.uint8)
            
            # Convert to PIL Image
            img = Image.fromarray(slice_normalized, mode='L')
            images.append(img)
        
        # Save as multi-page TIFF
        if images:
            images[0].save(
                output_path,
                save_all=True,
                append_images=images[1:],
                compression='tiff_deflate'  # Use deflate compression instead of LZW for better napari compatibility
            )
        
        output_paths.append(str(output_path))
        
        # Print conversion info for this channel
        if scalar_components > 1:
            print(f"Converted {raw_file_path.name} -> {output_path.name} (Channel {ch_idx})")
        else:
            print(f"Converted {raw_file_path.name} -> {output_path.name}")
    
    # Print summary info
    if use_filename_fallback:
        print(f"  Name: {file_info['name']}")
        print(f"  Data Type: {'Vector' if scalar_components > 1 else 'Scalar'}")
        print(f"  Scalar Type: {scalar_type}")
        print(f"  Byte Order: {byte_order}")
    else:
        print(f"  Name: {metadata['name']}")
        print(f"  Data Type: {metadata['data_type']}")
        print(f"  Scalar Type: {metadata['scalar_type']}")
        print(f"  Byte Order: {metadata.get('byte_order', 'little Endian')}")
    
    print(f"  Dimensions: {width}x{height}x{depth}")
    if scalar_components > 1:
        print(f"  Scalar Components: {scalar_components}")
        print(f"  Output files: {len(output_paths)} channels")
    print(f"  Output: {output_paths}")
    
    return output_paths


def main():
    """
    Main function to scan a folder and convert all raw files to TIFF.
    """
    # Get the current directory (SciVisAgentBench-tasks)
    input_folder = r"D:\Development\SciVisAgentBench-tasks"
    
    print(f"Scanning directory: {input_folder}")
    
    # Find all raw files recursively
    raw_files = list(Path(input_folder).rglob("*.raw"))
    
    if not raw_files:
        print("No raw files found in the directory tree.")
        return
    
    print(f"Found {len(raw_files)} raw files:")
    for raw_file in raw_files:
        print(f"  - {raw_file}")
    
    print("\nStarting conversion...")
    
    converted_count = 0
    failed_count = 0
    
    for raw_file in raw_files:
        try:
            convert_raw_to_tif(raw_file)
            converted_count += 1
        except Exception as e:
            print(f"Error converting {raw_file}: {e}")
            failed_count += 1
    
    print(f"\nConversion complete!")
    print(f"Successfully converted: {converted_count} files")
    print(f"Failed conversions: {failed_count} files")


if __name__ == "__main__":
    main()
