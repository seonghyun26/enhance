#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 molecule method"
    exit 1
fi

molecule=$1
method=$2

CUDA_VISIBLE_DEVICES=0 gmx mdrun -deffnm "./simulations/${molecule}/${method}/data/nvt/0" -nsteps 100000000 -ntomp 1 -ntmpi 1 -plumed "./simulations/${molecule}/${method}/plumed_pos.dat"