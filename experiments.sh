#!/bin/bash

molecule="aldp"
method=$1
ckpt=$2
max_seed=$3
ns=10
seed=0

export TZ=Asia/Seoul
datetime=$(date '+%m%d_%H%M%S')
# datetime=0430_042652
echo $datetime

gpuidx=0

# for (( seed=0; seed<=max_seed; seed++ )); do
#     base_dir="./simulations/${molecule}/${method}/${ns}/log/${datetime}/${seed}"
#     mkdir -p "${base_dir}/fes"

#     cp "./simulations/${molecule}/${method}/plumed.dat" "${base_dir}/plumed.dat"

#     if [[ ! "$method" =~ ^(ref|phi|unbiased)$ ]]; then
#         echo "Not ref"
#         sed -i "/deep: PYTORCH_MODEL/,/^\.\.\./ s|FILE=test\.pt|FILE=./simulations/${molecule}/${method}/${ns}/${ckpt}.pt|g" ${base_dir}/plumed.dat
#         sed -i "/deep: PYTORCH_MODEL/,/^\.\.\./! s|FILE=|FILE=${base_dir}/|g" ${base_dir}/plumed.dat
#     elif [[ "$method" == "ref" ]]; then
#         echo "Ref"
#         sed -i "s|FILE=|FILE=${base_dir}/|g" ${base_dir}/plumed.dat
#     fi
#     cat ${base_dir}/plumed.dat


#     CUDA_VISIBLE_DEVICES=$(( seed + gpuidx )) gmx mdrun \
#         -s ./simulations/aldp/data/nvt/0.tpr \
#         -deffnm ${base_dir} \
#         -plumed ${base_dir}/plumed.dat \
#         -nsteps 10000000 \
#         -ntomp 1 \
#         -nb gpu \
#         -bonded gpu &
    
#     sleep 1

# done

wait
echo "All GROMACS Finished!"


for (( seed=0; seed<=max_seed; seed++ )); do
    base_dir="./simulations/${molecule}/${method}/${ns}/log/${datetime}/${seed}"
    
    python3 FES_from_State.py \
        --state ${base_dir}/STATE \
        --outfile ${base_dir}/fes/fes.dat \
        --temp 300 \
        --all_stored
done

wait
echo "All post-processing done!"


python3 main.py \
    --seed $max_seed \
    --plumed ./simulations/${molecule}/${method}/plumed.dat \
    --date ${datetime} \
    --method ${method}

echo "Plots done!"