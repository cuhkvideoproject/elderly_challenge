# Generate a list required for skeleton extraction
# Usage: python3 script.py --input-folder /path/to/videos --output-dir /path/to/output/dir

import os
import argparse

# Define the starting label (modifiable inside the script)
START_LABEL = 0  # Change this value as needed
LINES_PER_FILE = 250  # Maximum lines per output file

def generate_video_list(input_folder, output_dir):
    # Ensure the input directory exists
    if not os.path.isdir(input_folder):
        print(f"Error: The directory '{input_folder}' does not exist.")
        return
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of video files in the input directory
    video_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    # Sort files alphabetically for consistency
    video_files.sort()

    # Generate labeled paths using a for loop
    labeled_paths = []
    for f in video_files:
        relative_path = os.path.relpath(os.path.join(input_folder, f), start=os.getcwd())
        labeled_paths.append(f"{relative_path} {START_LABEL}")

    # Split into multiple files
    file_count = 0
    for i in range(0, len(labeled_paths), LINES_PER_FILE):
        chunk = labeled_paths[i:i + LINES_PER_FILE]
        chunk_filename = os.path.join(output_dir, f"videos_list_{file_count}.list")
        with open(chunk_filename, "w") as file:
            file.write("\n".join(chunk) + "\n")
        print(f"File '{chunk_filename}' has been created successfully.")
        file_count += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a list of relative video file paths with a fixed label, splitting output into multiple files.")
    
    parser.add_argument(
        "--input-folder", 
        type=str, 
        required=True, 
        help="Path to the input folder containing video files."
    )
    
    parser.add_argument(
        "--output-dir", 
        type=str, 
        required=True, 
        help="Path to the output directory where files will be stored."
    )

    args = parser.parse_args()
    
    generate_video_list(args.input_folder, args.output_dir)
