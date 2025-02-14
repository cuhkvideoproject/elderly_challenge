#!/bin/bash

# Set fixed values inside the script
# config_file="configs/ctrgcn/elderly/eval_j.py"
# pth="work_dirs/ctrgcn/ctrgcn_pyskl_imbalance_merged_etrifull_toyota_hrnet/j/best_top1_acc_epoch_15.pth"
# output_file="work_dirs/ctrgcn/ctrgcn_pyskl_eval_hrnet/j/test_result_imbalance_etrifull_toyota_hrnet_relabel.pkl"

config_file="configs/msg3d/elderly/eval_b.py"
pth="work_dirs/msg3d/msg3d_pyskl_etrifull_toyota_hrnet/b/best_top1_acc_epoch_15.pth"
output_file="work_dirs/msg3d/msg3d_pyskl_etrifull_toyota_hrnet/eval_b/test_result_etrifull_toyota_hrnet_relabel.pkl"

num_gpu=2
eval_metric="top_k_accuracy"
dataset_path="data/elderlychallenge/eval_hrnet.pkl"  # Set your dataset path here

# Print the values of the variables (for verification)
echo "Config file: $config_file"
echo "Path: $pth"
echo "Number of GPUs: $num_gpu"
echo "Evaluation Metric: $eval_metric"
echo "Output file: $output_file"
echo "Dataset path: $dataset_path"

# Execute the dist_test.sh script with the fixed arguments
bash tools/dist_test.sh "$config_file" "$pth" "$num_gpu" --eval "$eval_metric" --out "$output_file"

# Execute the Python script with the necessary arguments
python3 examples/generate_prediction_csv/gen_pred.py --dataset_path "$dataset_path" --result_path "$output_file"
# python3 examples/generate_prediction_csv/gen_pred_ensemble.py --dataset_path "$dataset_path" --result_path "$output_file" --result2_path "$output_file"
