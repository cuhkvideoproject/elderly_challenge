from mmcv import load, dump

pkl_list = ["newsplit_etrifull_relabel.pkl", "newsplit_toyota_relabel.pkl"]

annotations = []

output_file = 'merged_newsplit_etri_full_toyota_relabel.pkl'

split = {}

for file in pkl_list:
    with open(file, "rb") as f:
        print(file)
        dataset = load(f, file_format='pkl')  # Load the pickle file correctly
        print("len(dataset['annotations'])", len(dataset['annotations']))
        annotations.extend(dataset['annotations'])

        for sp in dataset['split']:
            print(f"len(dataset['split'][{sp}])", len(dataset['split'][sp]))
            if sp in split:
                split[sp].extend(dataset['split'][sp])
            else:
                split[sp] = dataset['split'][sp]
        
print('len(annotations)', len(annotations))
for sp in split:
    print(f'len(split[{sp}])', len(split[sp]))

# Save final merged data
dump(dict(split=split, annotations=annotations), output_file)
print(f"Successfully saved processed data to {output_file}")
