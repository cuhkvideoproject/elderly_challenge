import numpy as np
from mmcv import load
import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from collections import Counter
import csv

test_key = 'test'

def get_pred(scores):
    """Get the prediction from scores

    Args:
        scores (list[np.ndarray]): Prediction scores for each class.

    Returns:
        pred: prediction result
    """
    k = 1
    max_1_preds = np.argsort(scores, axis=1)[:, -k:][:, ::-1]
    max_1_preds = [x[0] for x in max_1_preds]
    return max_1_preds

def main():
    parser = argparse.ArgumentParser(description="Load and process prediction scores from a pickle file.")
    parser.add_argument(
        "--result_path",
        type=str,
        required=True,
        help="Path to the result pickle file."
    )
    parser.add_argument(
        "--result2_path",
        type=str,
        required=True,
        help="Path to the result pickle file."
    )
    parser.add_argument(
        "--dataset_path",
        type=str,
        required=True,
        help="Path to the dataset pickle file."
    )
    args = parser.parse_args()

    scores1 = load(args.result_path, file_format='pkl')
    scores2 = load(args.result2_path, file_format='pkl')

    scores_ensemble = []
    for i in range(len(scores1)):
        scores_ensemble.append(scores1[i] + scores2[i])
    preds = get_pred(scores_ensemble)
    
    dataset = load(args.dataset_path, file_format='pkl')
    print('Test keys:', dataset['split'].keys())
    dataset_test_frame_dirs_ls = dataset['split'][test_key]

    if len(dataset_test_frame_dirs_ls) != len(preds):
        print(f"Len not match! {len(dataset_test_frame_dirs_ls)} != {len(preds)}")
    else:
        print(f"Len match: {len(dataset_test_frame_dirs_ls)} {len(preds)}")
        
    # get ground truth
    has_ground_truth = True
    if has_ground_truth:
        test_gts = [anno['label'] for anno in dataset['annotations'] if anno['frame_dir'] in dataset_test_frame_dirs_ls]
        
        def calculate_accuracy(predictions, ground_truths):
            correct = sum(p == gt for p, gt in zip(predictions, ground_truths))
            total = len(ground_truths)
            return (correct / total) * 100 if total > 0 else 0

        acc = calculate_accuracy(preds, test_gts)
        print(f'Accuracy: {acc}')
        
        counter = Counter(test_gts)
        print('Ground truth counter:', counter)
        
        def plot_confusion_matrix(predictions, ground_truths, class_labels=None):
            cm = confusion_matrix(ground_truths, predictions)
            plt.figure(figsize=(6, 5))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=class_labels, yticklabels=class_labels)
            plt.xlabel("Predicted Labels")
            plt.ylabel("True Labels")
            plt.title("Confusion Matrix")
            plt.savefig("confusion_matrix.png")

        plot_confusion_matrix(preds, test_gts, [0,1,2,3,4,5])
    
    def generate_csv(file_name, dataset_test_frame_dirs_ls, preds):
        label_number_mapping = {
            0: "locomotion",
            1: "manipulation",
            2: "communication",
            3: "hygiene",
            4: "eating_drinking",
            5: "leisure",
            6: "others"
        }
        
        with open(file_name, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["video_name", "action_category"])
            for frame_dir, pred in zip(dataset_test_frame_dirs_ls, preds):
                writer.writerow([frame_dir, label_number_mapping[pred]])
        
        print(f"CSV file '{file_name}' generated successfully.")
    
    generate_csv("elderlychallenge_output.csv", dataset_test_frame_dirs_ls, preds)

if __name__ == "__main__":
    main()
