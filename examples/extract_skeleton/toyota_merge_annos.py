import argparse
import glob
import os
from mmcv import load, dump
from collections import Counter
from sklearn.model_selection import train_test_split

def process_pkl_files(input_directory, output_file):
    """Loads all .pkl files in the specified input directory, processes them, and saves the output."""

    # Load all .pkl files in the given input directory
    annotations = []
    for file in glob.glob(os.path.join(input_directory, "*.pkl")):
        with open(file, "rb") as f:
            print(file)
            anno = load(f, file_format='pkl')  # Load the pickle file correctly
            annotations.extend(anno)

    # print(annotations[1234])
    # print('len(annotations)', len(annotations))

    # Count occurance
    # frame_dir_list = []
    # for a in annotations:
    #     frame_dir_list.append(a['frame_dir'])


    # def count_occurrences(string_list):
    #     string_counter = Counter(string_list)

    #     # Sort alphabetically and print results
    #     for string in sorted(string_counter.keys()):
    #         print(f'"{string}": {string_counter[string]}')

    # frame_dir_list = [s.split('_')[0] if '_' in s else s for s in frame_dir_list]
    # count_occurrences(frame_dir_list)

    # map label
    toyota_label_mapping = {
        "Cook": "Manipulation",
        "Cutbread": "Manipulation",
        "Drink": "Eating_Drinking",
        "Eat": "Eating_Drinking",
        "Enter": "Locomotion",
        "Getup": "Locomotion",
        "Laydown": "Locomotion",
        "Leave": "Locomotion",
        "Makecoffee": "Manipulation",
        "Maketea": "Manipulation",
        "Pour": "Others",
        "Readbook": "Leisure",
        "Sitdown": "Locomotion",
        "Takepills": "Hygiene",
        "Uselaptop": "Leisure",
        "Usetablet": "Leisure",
        "Usetelephone": "Communication",
        "Walk": "Locomotion",
        "WatchTV": "Leisure"
    }

    label_number_mapping = {
        "Locomotion": 0,
        "Manipulation": 1,
        "Communication": 2,
        "Hygiene": 3,
        "Eating_Drinking": 4,
        "Leisure": 5,
        "Others": 6
    }

    for i in range(len(annotations)):
        if '_' in annotations[i]['frame_dir']:
            prefix = annotations[i]['frame_dir'].split('_')[0]
        else:
            prefix = annotations[i]['frame_dir']

        text_label = toyota_label_mapping[prefix]
        annotations[i]['label'] = label_number_mapping[text_label]

    # Filter 'Others' category
    annotations = [a for a in annotations if a['label']!=6]

    # Assign random frame_dir
    for i in range(len(annotations)):
        annotations[i]['frame_dir'] = str(i)

    # Train test split by label
    frame_dirs = [d["frame_dir"] for d in annotations]
    labels = [d["label"] for d in annotations]

    # Stratified train-test split
    train_dirs, test_dirs = train_test_split(frame_dirs, test_size=0.2, random_state=42, stratify=labels)

    split = {
        'train': train_dirs,
        'test': test_dirs
    }

    print(len(train_dirs), len(test_dirs))
    print(train_dirs[:10])
    print(test_dirs[:10])

    # Save final merged data
    dump(dict(split=split, annotations=annotations), output_file)
    print(f"Successfully saved processed data to {output_file}")

if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Process all .pkl files in an input directory.")
    parser.add_argument("--input-directory", type=str, required=True, help="Input directory containing .pkl files")
    parser.add_argument("--output-pkl", type=str, required=True, help="Output .pkl file name")

    args = parser.parse_args()

    # Run the processing function
    process_pkl_files(args.input_directory, args.output_pkl)
