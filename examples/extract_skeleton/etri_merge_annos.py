import argparse
import glob
import os
from mmcv import load, dump
from collections import Counter
from sklearn.model_selection import train_test_split

def process_pkl_files(input_directory, output_file):
    """Loads all .pkl files in the specified input directory, processes them, and saves the output."""

    # Load all .pkl files in the given input directory and its subdirectories
    annotations = []
    for file in glob.glob(os.path.join(input_directory, "**", "*.pkl"), recursive=True):
        with open(file, "rb") as f:
            print(file)
            anno = load(f, file_format='pkl')  # Load the pickle file correctly
            annotations.extend(anno)

    # print(annotations[1234])
    print('len(annotations)', len(annotations))

    # Count occurance
    # frame_dir_list = []
    # for a in annotations:
    #     frame_dir_list.append(a['frame_dir'])


    def count_occurrences(string_list):
        string_counter = Counter(string_list)

        # Sort alphabetically and print results
        for string in sorted(string_counter.keys()):
            print(f'"{string}": {string_counter[string]}')

    # frame_dir_list = [s.split('_')[0] if '_' in s else s for s in frame_dir_list]
    # count_occurrences(frame_dir_list)

    # map label
    etri_label_mapping = {
        "A001": "Eating_Drinking",
        "A002": "",
        "A003": "Hygiene",
        "A004": "Eating_Drinking",
        "A005": "Manipulation",
        "A006": "Manipulation",
        "A007": "Manipulation",
        "A008": "Manipulation",
        "A009": "Manipulation",
        "A010": "Hygiene",
        "A011": "Hygiene",
        "A012": "Hygiene",
        "A013": "Hygiene",
        "A014": "",
        "A015": "",
        "A016": "Hygiene",
        "A017": "",
        "A018": "",
        "A019": "",
        "A020": "Manipulation",
        "A021": "Manipulation",
        "A022": "Manipulation",
        "A023": "Manipulation",
        "A024": "Manipulation",
        "A025": "Manipulation",
        "A026": "Manipulation",
        "A027": "Manipulation",
        "A028": "",
        "A029": "",
        "A030": "Manipulation",
        "A031": "",
        "A032": "Leisure",
        "A033": "Leisure",
        "A034": "Manipulation",
        "A035": "Communication",
        "A036": "Communication",
        "A037": "Leisure",
        "A038": "",
        "A039": "Communication",
        "A040": "",
        "A041": "Leisure",
        "A042": "Leisure",
        "A043": "Hygiene",
        "A044": "",
        "A045": "Communication",
        "A046": "Communication",
        "A047": "Communication",
        "A048": "",
        "A049": "Communication",
        "A050": "Communication",
        "A051": "Communication",
        "A052": "Locomotion",
        "A053": "",
        "A054": "Locomotion",
        "A055": "Locomotion"
    }

    label_number_mapping = {
        "Locomotion": 0,
        "Manipulation": 1,
        "Communication": 2,
        "Hygiene": 3,
        "Eating_Drinking": 4,
        "Leisure": 5,
        "": 6
    }

    six_prefix = []
    six_people = []

    for i in range(len(annotations)):
        prefix = annotations[i]['frame_dir'][:4]
        # print(annotations[i]['frame_dir'], prefix)

        text_label = etri_label_mapping[prefix]
        annotations[i]['label'] = label_number_mapping[text_label]

        if annotations[i]['label'] == 6:
            if prefix not in six_prefix:
                six_prefix.append(prefix)
            person = annotations[i]['frame_dir'][5:9]
            if person not in six_people:
                six_people.append(person)

    # print('six_prefix', six_prefix)
    # print('six_people', six_people)

    # labels_before_filter = [d["label"] for d in annotations]
    # count_occurrences(labels_before_filter)

    # Filter empty or 'Others' category
    annotations = [a for a in annotations if a['label']!=6]

    # Train test split by label
    frame_dirs = [d["frame_dir"] for d in annotations]
    labels = [d["label"] for d in annotations]

    # Stratified train-test split
    train_label_split_dirs, test_label_split_dirs = train_test_split(frame_dirs, test_size=0.2, random_state=42, stratify=labels)
    train_subj_split_dirs = []
    test_subj_split_dirs = []

    groupcam_labels = []
    person_labels = []

    for a in annotations:
        fd = a['frame_dir']
        fd = fd.split('.')[0]
        activity, person, group, camera = fd.split('_')
        activity = a['label']
        groupcam_labels.append(f'{activity}_{group}_{camera}')
        person_labels.append(f'{activity}_{person}')
        person = int(person[1:])
        if person%3 == 0:
            test_subj_split_dirs.append(fd)
        else:
            train_subj_split_dirs.append(fd)
        # if person == 'P001':
        #     print(fd, activity, person, group, camera)

    count_occurrences(labels)

    count_occurrences(groupcam_labels)

    count_occurrences(person_labels)

    train_groupcamlabel_split_dirs, test_groupcamlabel_split_dirs = train_test_split(frame_dirs, test_size=0.1, random_state=42, stratify=groupcam_labels)
    train_personlabel_split_dirs, test_personlabel_split_dirs = train_test_split(frame_dirs, test_size=0.1, random_state=42, stratify=person_labels)

    split = {
        'all': frame_dirs,
        'train_label_split': train_label_split_dirs,
        'test_label_split': test_label_split_dirs,
        'train_groupcamlabel_split': train_groupcamlabel_split_dirs,
        'test_groupcamlabel_split': test_groupcamlabel_split_dirs,
        'train_subj_split': train_subj_split_dirs,
        'test_subj_split': test_subj_split_dirs,
        'train_personlabel_split': train_personlabel_split_dirs,
        'test_personlabel_split': test_personlabel_split_dirs
    }

    print("len(split['all'])", len(split['all']))
    print("len(split['train_label_split']), len(split['test_label_split'])", len(split['train_label_split']), len(split['test_label_split']))
    print("len(split['train_groupcamlabel_split']), len(split['test_groupcamlabel_split'])", len(split['train_groupcamlabel_split']), len(split['test_groupcamlabel_split']))
    print("len(split['train_subj_split']), len(split['test_subj_split'])", len(split['train_subj_split']), len(split['test_subj_split']))
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
