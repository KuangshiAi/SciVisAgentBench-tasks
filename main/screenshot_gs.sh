# !/bin/bash
# Example usage of screenshot_helper.py for the carp dataset, 
# which generates three views (front, side, diagonal) of screenshots for a given ParaView state file
pvpython screenshot_helper.py --gs_state_path carp/GS/carp_gs.pvsm \
    --gs_img_path carp/GS \
    --data_directory carp/data \
    # data_directory is needed to load the data files correctly, otherwise use the data path in the state file
    # --result_state_path carp/results/carp_result.pvsm \
    # --result_img_path carp/results \