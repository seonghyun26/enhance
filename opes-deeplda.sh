# bash experiments.sh DeepLDA DeepLDA-10 3

# for seed in 0
# do
#     base_dir="./simulations/aldp/DeepLDA/10/log/0427_073734_0.4/${seed}"

#     python3 FES_from_State.py \
#         --state ${base_dir}/STATE \
#         --outfile ${base_dir}/fes/fes.dat \
#         --temp 300 \
#         --all_stored
# done

python3 main.py \
    --seed 3 \
    --plumed ./simulations/aldp/DeepLDA/plumed.dat \
    --date 0430_042954 \
    --method DeepLDA