import argparse
import glob
import os
from mmcv import load, dump

def process_pkl_files(input_directory, output_file):
    """Loads all .pkl files in the specified input directory, processes them, and saves the output."""

    # Load all .pkl files in the given input directory
    annotations = []
    for file in glob.glob(os.path.join(input_directory, "*.pkl")):
        with open(file, "rb") as f:
            anno = load(f)  # Load the pickle file correctly
        annotations.extend(anno)

    # Train test split
    train = load('Diving48_V2_train.json')
    test = load('Diving48_V2_test.json')
    split = {
        'train': [x['vid_name'] for x in train],
        'test': [x['vid_name'] for x in test]
    }

    # Save final merged data
    dump(dict(split=split, annotations=annotations), output_file)
    print(f"Successfully saved processed data to {output_file}")

if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Process all .pkl files in an input directory.")
    parser.add_argument("input_directory", type=str, help="Input directory containing .pkl files")
    parser.add_argument("--output", type=str, default="diving48_hrnet.pkl", help="Output file name")

    args = parser.parse_args()

    # Run the processing function
    process_pkl_files(args.input_directory, args.output)
