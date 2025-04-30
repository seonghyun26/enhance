bash experiments.sh DeepTDA DeepTDA-10

# for seed in 0 1 2
# do
#     base_dir="./simulations/aldp/DeepTDA/10/log/0429_091159/${seed}"

#     python3 FES_from_State.py \
#         --state ${base_dir}/STATE \
#         --outfile ${base_dir}/fes \
#         --temp 300 \
#         --all_stored
# done

# python3 main.py \
#     --seed 2 \
#     --plumed ./simulations/aldp/DeepTDA/plumed.dat \
#     --date 0429_091159 \
#     --method DeepTDA