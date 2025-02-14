#!/bin/bash

config_file="configs/ctrgcn/elderly/imbalance_merged_etrifull_toyota_j.py"
num_gpu=2

# Print the values of the variables (for verification)
echo "Config file: $config_file"
echo "Number of GPUs: $num_gpu"

bash tools/dist_train.sh "$config_file" "$num_gpu" --validate --test-last --test-best