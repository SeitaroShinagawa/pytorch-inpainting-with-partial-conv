#!/bin/bash

export CUDA_VISIBLE_DEVICES=1

python train.py --root "/project/nakamura-lab07/Work/seitaro-s/place2" \
                --mask_root "./masks/256" \
                --batch_size 16 \
                --n_threads 16 \
                --image_size 256 \
