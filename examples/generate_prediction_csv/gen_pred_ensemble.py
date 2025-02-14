import numpy as np
from mmcv import load
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from collections import Counter
import csv

test_key = 'test'

# List of result file paths (replace these with actual paths)
result_files = [
                "work_dirs/ctrgcn/ctrgcn_pyskl_eval_hrnet/j/test_result_groupcam_etrifull_toyota_hrnet_relabel.pkl",
                "work_dirs/msg3d/msg3d_pyskl_groupcamsplit_etrifull_toyota_hrnet/eval_b/test_result_etrifull_toyota_hrnet_relabel.pkl",
                "work_dirs/ctrgcn/ctrgcn_pyskl_eval_hrnet/j/test_result_personsplit_etrifull_toyota_hrnet_relabel.pkl",
                "work_dirs/msg3d/msg3d_pyskl_personsplit_etrifull_toyota_hrnet/eval_b/test_result_etrifull_toyota_hrnet_relabel.pkl",
                ]

dataset_path = "data/elderlychallenge/eval_hrnet.pkl"

def get_pred(scores):
    """Get the prediction from scores.

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
    # Load all result files
    all_scores = [load(file, file_format='pkl') for file in result_files]

    # Ensure all results have the same length
    num_samples = len(all_scores[0])
    assert all(len(scores) == num_samples for scores in all_scores), "Mismatched lengths in result files"

    # Perform ensembling by summing element-wise
    scores_ensemble = [sum(scores[i] for scores in all_scores) for i in range(num_samples)]
    preds = get_pred(scores_ensemble)
    
    dataset = load(dataset_path, file_format='pkl')
    dataset_test_frame_dirs_ls = dataset['split'][test_key]

    if len(dataset_test_frame_dirs_ls) != len(preds):
        print(f"Len not match! {len(dataset_test_frame_dirs_ls)} != {len(preds)}")
    else:
        print(f"Len match: {len(dataset_test_frame_dirs_ls)} {len(preds)}")
        
    # Get ground truth
    has_ground_truth = True
    if has_ground_truth:
        test_gts = [anno['label'] for anno in dataset['annotations'] if anno['frame_dir'] in dataset_test_frame_dirs_ls]

        def calculate_accuracy(predictions, ground_truths):
            correct = sum(p == gt for p, gt in zip(predictions, ground_truths))
            total = len(ground_truths)
            return (correct / total) * 100 if total > 0 else 0

        acc = calculate_accuracy(preds, test_gts)
        print(f'Accuracy: {acc}%')

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

        plot_confusion_matrix(preds, test_gts, [0, 1, 2, 3, 4, 5])

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
                writer.writerow([frame_dir, label_number_mapping.get(pred, "unknown")])
        
        print(f"CSV file '{file_name}' generated successfully.")
    
    generate_csv("submission.csv", dataset_test_frame_dirs_ls, preds)

if __name__ == "__main__":
    main()
