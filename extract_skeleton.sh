#!/bin/bash

# Define variables for file paths
VIDEOS_DIRECTORY="../datasets/elderlychallenge_evaluation_dataset/eval_FO_ids"
VIDEOS_LIST_DIR="examples/extract_skeleton/eval_video_lists"
ANNOS_DIR="examples/extract_skeleton/eval_annos"  # Output directory for annotations
NUM_GPUS=3  # Set the number of GPUs

# Ensure the output directory exists
rm -rf "$VIDEOS_LIST_DIR"
mkdir -p "$VIDEOS_LIST_DIR"
mkdir -p "$ANNOS_DIR"

# Run the Python script to generate video lists
python3 examples/extract_skeleton/generate_list.py --input-folder "$VIDEOS_DIRECTORY" --output-dir "$VIDEOS_LIST_DIR"

# Loop through each video list file in the directory
for VIDEO_LIST in "$VIDEOS_LIST_DIR"/*; do
    # Extract filename without extension
    BASE_NAME=$(basename "$VIDEO_LIST" .txt)
    
    # Define output path for this specific video list
    ANNOS_PKL="$ANNOS_DIR/${BASE_NAME}.pkl"
    
    # Execute the main script for each video list
    bash tools/dist_run.sh tools/data/custom_2d_skeleton.py "$NUM_GPUS" --video-list "$VIDEO_LIST" --out "$ANNOS_PKL"
    
    # Print message when processing of a video list is done
    echo "Processing of video list '$BASE_NAME' is done"
done
