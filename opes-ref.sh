bash experiments.sh ref dummy 3

# for seed in 0 1 2
# do
#     base_dir="./simulations/aldp/TBG/10/log/0429_105517_0.025/${seed}"

#     python3 FES_from_State.py \
#         --state ${base_dir}/STATE \
#         --outfile ${base_dir}/fes/fes.dat \
#         --temp 300 \
#         --all_stored
# done

# python3 main.py \
#     --seed 0 \
#     --plumed ./simulations/aldp/TBG/plumed.dat \
#     --date 0429_105517_0.025 \
#     --method TBG