import argparse
from mmcv import load, dump
from collections import Counter

def ntu60_process_pkl_file(input_file, output_file):
    """Loads a pickle file, processes it, and saves the output."""
    data = load(input_file)
    
    print(type(data))
    print(len(data))
    print(data.keys())

    print(type(data['annotations']))
    print(len(data['annotations']))

    # map label
    ntu60_label_mapping = {
        "A001": "Eating_Drinking",
        "A002": "Eating_Drinking",
        "A003": "Hygiene",
        "A004": "Hygiene",
        "A005": "",
        "A006": "",
        "A007": "",
        "A008": "Locomotion",
        "A009": "Locomotion",
        "A010": "Communication",

        "A011": "Leisure",
        "A012": "Manipulation",
        "A013": "",
        "A014": "",
        "A015": "",
        "A016": "Manipulation",
        "A017": "Manipulation",
        "A018": "Manipulation",
        "A019": "Manipulation",
        "A020": "",

        "A021": "",
        "A022": "",
        "A023": "Communication",
        "A024": "",
        "A025": "",
        "A026": "",
        "A027": "",
        "A028": "Communication",
        "A029": "Leisure",
        "A030": "",

        "A031": "Communication",
        "A032": "",
        "A033": "",
        "A034": "",
        "A035": "",
        "A036": "",
        "A037": "",
        "A038": "",
        "A039": "",
        "A040": "",

        "A041": "",
        "A042": "",
        "A043": "",
        "A044": "",
        "A045": "",
        "A046": "",
        "A047": "",
        "A048": "",
        "A049": "",
        "A050": "",

        "A051": "",
        "A052": "",
        "A053": "",
        "A054": "",
        "A055": "Communication",
        "A056": "",
        "A057": "",
        "A058": "Communication",
        "A059": "",
        "A060": ""
    }

    label_number_mapping = {
        "Locomotion": 0,
        "Manipulation": 1,
        "Communication": 2,
        "Hygiene": 3,
        "Eating_Drinking": 4,
        "Leisure": 5,
        "Others": 6,
        "": 6
    }

    for i in range(len(data['annotations'])):
        suf = data['annotations'][i]['frame_dir'][-4:]
        print(suf)
        mapping = ntu60_label_mapping[suf]
        data['annotations'][i]['label'] = label_number_mapping[mapping]

    # Filter 'Others' category
    annotations = data['annotations']
    annotations = [a for a in annotations if a['label']!=6]
    data['annotations'] = annotations
    
    freq = Counter([anno['label'] for anno in data['annotations']])
    
    print(sorted(freq.items()))

    # Save final merged data
    dump(data, output_file)
    print(f"Successfully saved processed data to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Process NTU60 pickle files')
    parser.add_argument('--input_file', type=str, required=True, help='Path to the input .pkl file')
    parser.add_argument('--output_file', type=str, required=True, help='Path to save the processed .pkl file')
    
    args = parser.parse_args()
    ntu60_process_pkl_file(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
