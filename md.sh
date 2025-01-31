#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 molecule method ns"
    exit 1
fi

molecule=$1
method=$2
ns=$3

datetime=$(date '+%m%d%H%M%S')

for seed in 0 1 2 3 4 5 6 7; do
    base_dir="./simulations/${molecule}/${method}/${ns}/log/${datetime}/${seed}"
    mkdir -p "${base_dir}/fes"
    cp "./simulations/${molecule}/${method}/plumed.dat" "${base_dir}/plumed.dat"

    # if method is not ref and phi
    if [ "${method}" != "ref" ] && [ "${method}" != "phi" ] && [ "${method}" != "unbiased" ]; then
        cp "./simulations/${molecule}/${method}/${ns}/test.pt" "${base_dir}/test.pt"
    fi

    sed -i "s|FILE=|FILE=${base_dir}/|g" ${base_dir}/plumed.dat
    CUDA_VISIBLE_DEVICES=$seed gmx mdrun -deffnm "./simulations/${molecule}/data/nvt/${seed}" -plumed ${base_dir}/plumed.dat -nsteps 10000000 -ntomp 1 -ntmpi 1 &
done

wait

for seed in 0 1 2 3 4 5 6 7; do
    base_dir="./simulations/${molecule}/${method}/${ns}/log/${datetime}/${seed}"
    plumed sum_hills --bin 100 --hills ${base_dir}/HILLS --stride 100 --outfile ${base_dir}/fes/ &
done

wait