#!/bin/bash

export CUDA_VISIBLE_DEVICES=0

python train.py --root "/project/nakamura-lab07/Work/seitaro-s/place2" \
                --mask_root "./masks/256" \
                --batch_size 8 \
                --n_threads 4 \
                --image_size 256 \
                --save_dir "./snapshots/pixelshuffler" \
                --log_dir "./logs/pixelshuffler" \
