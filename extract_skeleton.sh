#!/bin/bash

# Define variables for file paths
VIDEOS_DIRECTORY="../datasets/elderlychallenge_evaluation_dataset/eval_FO_ids"
VIDEOS_LIST="examples/extract_skeleton/videos.list"
ANNOS_PKL="examples/extract_skeleton/annos.pkl"
NUM_GPUS=4  # Set the number of GPUs

# Run the Python script with the variable path
python3 examples/extract_skeleton/generate_list.py --input-folder "$VIDEOS_DIRECTORY" --output-file "$VIDEOS_LIST"

# Execute the main script with the variable paths and GPU count
bash tools/dist_run.sh tools/data/custom_2d_skeleton.py "$NUM_GPUS" --video-list "$VIDEOS_LIST" --out "$ANNOS_PKL"
