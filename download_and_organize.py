import json
import os
import subprocess
import time
import zipfile

# Load dataset information
with open('datasets_info.json', 'r') as f:
    datasets = json.load(f)

# Filter datasets under 512MB, excluding existing ones
existing_datasets = []
datasets_to_download = [d for d in datasets if d['size_mb'] < 512 and d['id'] not in existing_datasets]

print(f"Will download and organize {len(datasets_to_download)} datasets")

# Process each dataset
for i, dataset in enumerate(datasets_to_download):
    dataset_id = dataset['id']
    print(f"\n[{i+1}/{len(datasets_to_download)}] Processing {dataset_id}...")
    
    # Create directory structure
    os.makedirs(f"sci_volume_data/{dataset_id}/data", exist_ok=True)
    
    # Download the dataset
    url = dataset['download_url']
    output_file = f"sci_volume_data/{dataset_id}/data/{dataset['filename']}"
    
    if not os.path.exists(output_file):
        print(f"  Downloading {dataset['filename']} ({dataset['size_str']})...")
        result = subprocess.run(['curl', '-o', output_file, url], capture_output=True)
        if result.returncode != 0:
            print(f"  ERROR downloading {dataset_id}")
            continue
        time.sleep(0.5)  # Be nice to the server
    else:
        print(f"  File already exists, skipping download")
    
    # Create metadata file
    metadata_file = f"sci_volume_data/{dataset_id}/data/{dataset_id}.txt"
    with open(metadata_file, 'w') as f:
        f.write(f"{dataset['name']}\n")
        f.write(f"Description: {dataset['description']}\n")
        f.write(f"Data Type: {dataset['data_type']}\n")
        f.write(f"Data Byte Order: little Endian\n")
        f.write(f"Data Spacing: {dataset['spacing']}\n")
        f.write(f"Data Extent: {dataset['dimensions']}\n")
    
    print(f"  Created directory structure and metadata")

print(f"\nCompleted processing {len(datasets_to_download)} datasets")

# Download BBBC012 dataset for napari_mcp_evals
print(f"\nDownloading BBBC012 dataset for napari_mcp_evals...")

# Create the napari_mcp_evals/data directory
napari_data_dir = "napari_mcp_evals/data"
os.makedirs(napari_data_dir, exist_ok=True)

# Download the BBBC012 dataset
bbbc_url = "https://data.broadinstitute.org/bbbc/BBBC012/BBBC012_v1_images.zip"
bbbc_zip_file = os.path.join(napari_data_dir, "BBBC012_v1_images.zip")

if not os.path.exists(os.path.join(napari_data_dir, "BBBC012_v1_images")):
    print(f"  Downloading BBBC012_v1_images.zip...")
    result = subprocess.run(['curl', '-o', bbbc_zip_file, bbbc_url], capture_output=True)
    
    if result.returncode == 0:
        print(f"  Download completed successfully")
        
        # Unzip the file
        print(f"  Extracting BBBC012_v1_images.zip...")
        try:
            with zipfile.ZipFile(bbbc_zip_file, 'r') as zip_ref:
                zip_ref.extractall(napari_data_dir)
            print(f"  Extraction completed")
            
            # Delete the zip file
            os.remove(bbbc_zip_file)
            print(f"  Cleaned up zip file")
            
        except zipfile.BadZipFile:
            print(f"  ERROR: Downloaded file is not a valid zip archive")
        except Exception as e:
            print(f"  ERROR during extraction: {e}")
    else:
        print(f"  ERROR downloading BBBC012 dataset")
else:
    print(f"  BBBC012 dataset already exists, skipping download")

print(f"\nAll processing completed!")