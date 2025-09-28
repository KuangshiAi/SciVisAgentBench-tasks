# SciVisAgentBench Tasks

This repository is a secondary repo of [SciVisAgentBench](https://github.com/KuangshiAi/SciVisAgentBench), contains scientific visualization datasets and tasks for benchmarking scientific visualization agents.

## Download Volume Datasets
`download_and_organize.py` downloads and organizes datasets under 512MB. Make sure you run the following script before you evaluate your agents through [SciVisAgentBench](https://github.com/KuangshiAi/SciVisAgentBench):
```shell
python download_and_organize.py
```

## Data Organization

All the volume datasets from http://klacansky.com/open-scivis-datasets/ have been organized into a consistent structure.

### Directory Structure

The datasets and tasks for ParaView-MCP and ChatVis are organized into the `main` and `sci_volume_data` folders, while `napari_mcp_evals` holds tasks and datasets for napari-MCP.


Each dataset in the `main` and `sci_volume_data` folders follows this structure:
```
dataset_name/
├── data/
│   ├── dataset_file.raw         # The actual data file
│   └── dataset_name.txt         # Metadata about the dataset
├── GS/                          # Ground truth folder (ParaView state + pvpython code)
├── task_description.txt         # ParaView visualization task
└── visualization_goals.txt      # Evaluation criteria for the visualization
```

### Available Volume Datasets

- **37 datasets under 512MB** are suggested to be downloaded
- **18 datasets over 512MB** are listed but not downloaded

See `datasets_list.md` for a complete list with specifications. And `datasets_info.json` is the complete JSON file with all dataset metadata.

### Task Descriptions

Each dataset has:
1. **Task descriptions** - Based on dataset type (medical, simulation, molecular, etc.)
2. **Visualization goals** - Evaluation criteria tailored to the dataset characteristics
3. **Ground Truth** - Ground truth pvpython code, ParaView state and screenshots

## Acknowledgement

SciVisAgentBench was mainly created by Kuangshi Ai (kai@nd.edu), Shusen Liu (liu42@llnl.gov), and Haichao Miao (miao1@llnl.gov). Some of the test cases are provided by Kaiyuan Tang (ktang2@nd.edu). We sincerely thank the open-source community for their invaluable contributions. This project is made possible thanks to the following outstanding projects:

- [ParaView-MCP](https://github.com/LLNL/paraview_mcp)
- [Napari-MCP](https://github.com/LLNL/napari-mcp)

## License

© 2025 University of Notre Dame.  
Released under the [License](./LICENSE).