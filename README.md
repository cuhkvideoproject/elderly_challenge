# Skeleton-based Elderly Action Recognition

This is the training and evaluation code for Elderly Action Recognition Challenge at WACV2025. 

Parts of this project were adapted from pyskl
 (https://github.com/kennymckormick/pyskl).

## Installation
```shell
git clone https://github.com/cuhkvideoproject/elderly_challenge.git
cd elderly_challenge
conda env create -f pyskl.yaml
conda activate pyskl
pip install -e .
```

## Skeleton Extraction

We utilize HRNet to generate 2D skeletons for every dataset we supported and Kinect 3D skeletons for the NTURGB+D and NTURGB+D 120 dataset. To obtain the human skeleton annotations, please follow the steps:

1. Put all videos into a single folder (e.g. ../datasets/ETRI-Activity3D/merged), then execute generate_list.py(for Toyota Smarthome dataset)/etri_generate_list.py(for Etri-Activity3D dataset) to create video lists for skeleton extraction

```shell
python3 examples/extract_skeleton/etri_generate_list.py --input-folder ../datasets/ETRI-Activity3D/merged --output-dir examples/extract_skeleton/etri_merged4_video_lists
```

2. Execute the script `toyota_extract_skeleton_0.sh` or `etri_merged1_extract_skeleton_0.sh` to obtain skeleton annotations (in pkl format). 

Specifically, change the variable `VIDEOS_LIST_DIR` to the created video lists, `ANNOS_DIR` to the output folder, `NUM_GPUS` to the number of GPUs.

3. Run `examples/extract_skeleton/etri_merge_annos.py` and `examples/extract_skeleton/toyota_merge_annos.py` to merge all extracted pkl annotations into a single pkl file. For example:

```shell
python etri_merge_annos.py --input-directory toyotasmarthome_annos/ --output-pkl toyota_merged.pkl
```

4. Combine etri pkl and toyota pkl into a single pkl using `data/elderlychallenge/merge_dataset_pkls.py`.

First, update the input `pkl_list = ["newsplit_etrifull_relabel.pkl", "newsplit_toyota_relabel.pkl"]` and output `output_file = 'merged_newsplit_etri_full_toyota_relabel.pkl'`, then execute:
```shell
python3 data/elderlychallenge/merge_dataset_pkls.py
```

## Training

Follow the script `groupcamsplit_train.sh` for traning CTR-GCN and `msg3d_groupcamsplit_train.sh` for training Msg3D in group cam split setting. You can also change the `config_file="configs/ctrgcn/elderly/groupcamsplit_etrifull_toyota_j.py"` and 
`num_gpu=2` values inside these scripts to train with other configurations. 

## Evaluation
Follow the script `evaluate.sh` to generate prediction. Change configuration values accordingly:
```
config_file="configs/msg3d/elderly/eval_b.py" # Use configs/ctrgcn/elderly/eval_j.py for toyota, msg3d/elderly/eval_b.py for msg3d
pth="work_dirs/msg3d/msg3d_pyskl_etrifull_toyota_hrnet/b/best_top1_acc_epoch_15.pth" # point to the trained model pth
output_file="work_dirs/msg3d/msg3d_pyskl_etrifull_toyota_hrnet/eval_b/test_result_etrifull_toyota_hrnet_relabel.pkl" # output file

num_gpu=2 # change to the number of GPUs
eval_metric="top_k_accuracy" # keep it
dataset_path="data/elderlychallenge/eval_hrnet.pkl"  # keep it for eval dataset
```

## Ensemble
We also provide a script ``examples/generate_prediction_csv/gen_pred_ensemble.py`` for ensembling predictions from different models.
Update variables `result_files` (pkl files for ensembling) and `dataset_path`, then execute:
```
python3 examples/generate_prediction_csv/gen_pred_ensemble.py
```
