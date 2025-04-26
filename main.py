import os
import wandb
import argparse

from src import *

def parse_args():
    parser = argparse.ArgumentParser(description='Train TBG model')
    parser.add_argument('--plumed', type = str, default = "./simulations/aldp/DeepLDA/plumed.dat", help='File to plumed')
    parser.add_argument('--date', type = str, default = "debug", help='Date for the experiment')
    parser.add_argument('--method', type = str, default = "phi", help='Date for the experiment')
    parser.add_argument('--ns', type = int, default = 10, help = "Length of simulation used for dataset")
    parser.add_argument('--seed', type = int, default = 0, help = "Number of seeds")
    parser.add_argument('--tags', nargs = '*', help='Tags for Wandb')
    
    return parser.parse_args()

def parse_plumed_metad(filename):
    """
    plumed.dat 파일에서 METAD 블록 안의 파라미터를 파싱하는 함수
    """
    metad_params = {}
    inside_metad = False

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            if line.startswith("METAD"):
                inside_metad = True
                continue

            if inside_metad and line.startswith("... METAD"):
                break

            if inside_metad and line and not line.startswith("#"):
                if "=" in line:
                    key, value = line.split("=", 1)
                    if key.strip() == 'LABEL':
                        prefix = value.strip()
                    elif key.strip() in ['ARG', 'FILE']:
                        metad_params[prefix + "/" + key.strip()] = value.strip()
                    else:
                        metad_params[prefix + "/" + key.strip()] = float(value.strip())

    return metad_params


args = parse_args()
plumed_params = parse_plumed_metad(args.plumed)

wandb.init(
    project="enhanced-sampling",
    entity="eddy26",
    tags = args.tags,
    config = vars(args),
)
wandb.log(plumed_params)

base_dir = f'{os.getcwd()}/simulations/aldp/{args.method}/{args.ns}'

plot_phi_distribution(args, base_dir)
plot_free_energy_difference(args, base_dir)
plot_fes_over_cv(args, base_dir)