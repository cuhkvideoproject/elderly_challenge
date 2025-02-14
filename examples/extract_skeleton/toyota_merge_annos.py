import argparse
import glob
import os
from mmcv import load, dump
from collections import Counter
from sklearn.model_selection import train_test_split
import numpy as np

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

    groupcam_labels = []
    person_labels = []

    for i in range(len(annotations)):
        fd = annotations[i]['frame_dir'][:-4]
        activity_full, person, r, v, camera = fd.split('_')
        print('fd', fd)
        

        if '.' in activity_full:
            activity = activity_full.split('.')[0]
        else:
            activity = activity_full

        print('activity_full, activity, person, r, v, camera', activity_full, activity, person, r, v, camera)

        text_label = toyota_label_mapping[activity]
        annotations[i]['label'] = label_number_mapping[text_label]

    # Filter 'Others' category
    annotations = [a for a in annotations if a['label']!=6]

    for i in range(len(annotations)):
        fd = annotations[i]['frame_dir'][:-4]
        activity_full, person, r, v, camera = fd.split('_')

        if '.' in activity_full:
            activity = activity_full.split('.')[0]
        else:
            activity = activity_full

        # groupcam_labels.append(f'{activity}_{r}_{v}_{camera}')
        groupcam_labels.append(f'{activity}_{camera}')
        person_labels.append(f'{activity}_{person}')
        
    # Train test split by label
    frame_dirs = [d["frame_dir"] for d in annotations]
    labels = [d["label"] for d in annotations]

    # Stratified train-test split
    train_label_split_dirs, test_label_split_dirs = train_test_split(frame_dirs, test_size=0.2, random_state=42, stratify=labels)

    def count_occurrences(string_list):
        string_counter = Counter(string_list)

        # Sort alphabetically and print results
        for string in sorted(string_counter.keys()):
            print(f'"{string}": {string_counter[string]}')

    count_occurrences(labels)

    count_occurrences(groupcam_labels)

    count_occurrences(person_labels)

    def train_test_split_safe(frame_dirs, test_size=0.2, random_state=42, stratify=None):
        """Performs stratified train-test split but ensures that classes with only one sample go to the training set."""
        frame_dirs = np.array(frame_dirs)

        if stratify is None:
            return train_test_split(frame_dirs, test_size=test_size, random_state=random_state)

        stratify = np.array(stratify)
        
        # Count occurrences of each class
        label_counts = Counter(stratify)
        
        # Find classes with only one sample
        single_sample_classes = {label for label, count in label_counts.items() if count == 1}
        
        # Indices of samples with only one occurrence
        single_sample_indices = [i for i, label in enumerate(stratify) if label in single_sample_classes]
        multiple_sample_indices = [i for i in range(len(stratify)) if i not in single_sample_indices]

        # Perform stratified split only on classes with multiple samples
        if multiple_sample_indices:
            train_split_dirs, test_split_dirs = train_test_split(
                frame_dirs[multiple_sample_indices],
                test_size=test_size,
                random_state=random_state,
                stratify=stratify[multiple_sample_indices]  # Stratify only valid labels
            )
        else:
            # If all classes have a single sample, put everything into training
            train_split_dirs = frame_dirs
            test_split_dirs = np.array([])  # Empty test set

        # Add back single-sample classes to the training set
        train_split_dirs = np.concatenate([train_split_dirs, frame_dirs[single_sample_indices]])

        return train_split_dirs, test_split_dirs

    train_groupcamlabel_split_dirs, test_groupcamlabel_split_dirs = train_test_split_safe(frame_dirs, test_size=0.1, random_state=42, stratify=groupcam_labels)
    train_personlabel_split_dirs, test_personlabel_split_dirs = train_test_split_safe(frame_dirs, test_size=0.1, random_state=42, stratify=person_labels)

    split = {
        'all': frame_dirs,
        'train_label_split': train_label_split_dirs,
        'test_label_split': test_label_split_dirs,
        'train_groupcamlabel_split': train_groupcamlabel_split_dirs,
        'test_groupcamlabel_split': test_groupcamlabel_split_dirs,
        'train_personlabel_split': train_personlabel_split_dirs,
        'test_personlabel_split': test_personlabel_split_dirs
    }   

    print("len(split['all'])", len(split['all']))
    print("len(split['train_label_split']), len(split['test_label_split'])", len(split['train_label_split']), len(split['test_label_split']))
    print("len(split['train_groupcamlabel_split']), len(split['test_groupcamlabel_split'])", len(split['train_groupcamlabel_split']), len(split['test_groupcamlabel_split']))
    print("len(split['train_personlabel_split']), len(split['test_personlabel_split'])", len(split['train_personlabel_split']), len(split['test_personlabel_split']))

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
