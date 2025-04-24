#!/bin/bash

molecule=aldp
method=DeepLDA
ns=10
repeat_num=1

datetime=$(date '+%m%d%H%M%S')
datetime=debug

for ((seed=0; seed<repeat_num; seed++))
do
    base_dir="./simulations/${molecule}/${method}/${ns}/log/${datetime}/${seed}"
    mkdir -p "${base_dir}/fes"
    cp "./simulations/${molecule}/${method}/plumed.dat" "${base_dir}/plumed.dat"

    if [ "${method}" != "ref" ] && [ "${method}" != "phi" ] && [ "${method}" != "unbiased" ]; then
        cp "./simulations/${molecule}/${method}/${ns}/test.pt" "${base_dir}/test.pt"
    fi

    sed -i "s|FILE=|FILE=${base_dir}/|g" ${base_dir}/plumed.dat
    CUDA_VISIBLE_DEVICES=$seed gmx mdrun \
        -s ./simulations/aldp/data/nvt/0.tpr \
        -deffnm ${base_dir} \
        -plumed ${base_dir}/plumed.dat \
        -nsteps 10000000 \
        -ntomp 1 \
        -nb gpu \
        -bonded gpu &
done

wait

for ((seed=0; seed<repeat_num; seed++))
do
    base_dir="./simulations/${molecule}/${method}/${ns}/log/${datetime}/${seed}"
    plumed sum_hills --bin 100 --hills ${base_dir}/HILLS --stride 100 --outfile ${base_dir}/fes/ &
done

wait

python3 plot.py \
    --date ${datetime} \
    --method ${method}