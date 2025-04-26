#!/bin/bash

molecule="aldp"
method=${1:-DeepLDA}
ns=10
seed=0

export TZ=Asia/Seoul
datetime=$(date '+%m%d_%H%M%S')
datetime=debug
echo $datetime

# base_dir="./simulations/${molecule}/${method}/${ns}/log/${datetime}/${seed}"
# mkdir -p "${base_dir}/fes"
# cp "./simulations/${molecule}/${method}/plumed.dat" "${base_dir}/plumed.dat"

# if [ "${method}" != "ref" ] && [ "${method}" != "phi" ] && [ "${method}" != "unbiased" ]; then
#     cp "./simulations/${molecule}/${method}/${ns}/${method}-${ns}.pt" "${base_dir}/test.pt"
# fi

# sed -i "s|FILE=|FILE=${base_dir}/|g" ${base_dir}/plumed.dat
# CUDA_VISIBLE_DEVICES=$seed gmx mdrun \
#     -s ./simulations/aldp/data/nvt/0.tpr \
#     -deffnm ${base_dir} \
#     -plumed ${base_dir}/plumed.dat \
#     -nsteps 10000000 \
#     -ntomp 1 \
#     -nb gpu \
#     -bonded gpu 

# wait

# base_dir="./simulations/${molecule}/${method}/${ns}/log/${datetime}/${seed}"
# plumed sum_hills \
#     --bin 100 \
#     --hills ${base_dir}/HILLS \
#     --outfile ${base_dir}/fes/ \
#     --stride 100

# wait

python3 main.py \
    --plumed ./simulations/${molecule}/${method}/plumed.dat \
    --date ${datetime} \
    --method ${method}