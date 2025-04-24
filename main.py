import os
import wandb
import argparse
import matplotlib.pyplot as plt

from .src import *

def parse_args():
    parser = argparse.ArgumentParser(description='Train TBG model')
    parser.add_argument('--date', type=str, default = "debug", help='Date for the experiment')
    parser.add_argument('--method', type=str, default = "DeepLDA", help='Date for the experiment')
    parser.add_argument('--ns', type=int, default = 10, help = "Length of simulation used for dataset")
    
    return parser.parse_args()

args = parse_args()


wandb.init(
    project="enhanced-sampling",
    entity="eddy26",
    tags = args.tags,
    config = vars(args),
)

base_dir = f'{os.getcwd()}/simulations/aldp'
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# TODO: connect the functions
# plot_free_energy_difference()
# plot_phi_distribution()