# Generate a list required for skeleton extraction
# Usage: python3 script.py --input-folder /path/to/videos --output-file videos.list

import os
import argparse

# Define the starting label (modifiable inside the script)
START_LABEL = 0  # Change this value as needed

def generate_video_list(input_folder, output_file):
    # Ensure the input directory exists
    if not os.path.isdir(input_folder):
        print(f"Error: The directory '{input_folder}' does not exist.")
        return

    # Get a list of video files in the input directory
    video_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    # Sort files alphabetically for consistency
    video_files.sort()

    # Generate labeled paths using a for loop
    labeled_paths = []
    for f in video_files:
        relative_path = os.path.relpath(os.path.join(input_folder, f), start=os.getcwd())
        labeled_paths.append(f"{relative_path} {START_LABEL}")

    # Write to output file
    with open(output_file, "w") as file:
        for line in labeled_paths:
            file.write(line + "\n")

    print(f"File '{output_file}' has been created successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a list of relative video file paths with a fixed label.")
    
    parser.add_argument(
        "--input-folder", 
        type=str, 
        required=True, 
        help="Path to the input folder containing video files."
    )
    
    parser.add_argument(
        "--output-file", 
        type=str, 
        required=True, 
        help="Path to the output file (e.g., videos.list)."
    )

    args = parser.parse_args()
    
    generate_video_list(args.input_folder, args.output_file)