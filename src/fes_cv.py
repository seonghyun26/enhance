import os
import wandb
import numpy as np
import matplotlib.pyplot as plt


from .constant import *


def marginalize(free):    
    # Filter data based on conditions
    free = free.reshape(51,51)
    
    # Calculate free energies
    free = -2.49 * np.logaddexp.reduce(-1 / 2.49 * free, 0)
    return free


def plot_fes_over_cv(args, base_dir):
    pmfs = []

    for seed in range(0, args.seed + 1):
        fes_file = os.path.join(base_dir, 'log', args.date, str(seed), "fes/100.dat")
        
        with open(fes_file, 'r') as file:
            first_line = file.readline().strip()
        keys = first_line.split()[2:]

        data = np.loadtxt(fes_file, comments='#')
        cv_idx = keys.index(cv_name[args.method])
        free_idx = keys.index('file.free')
        cv = data[:, cv_idx]
        free = data[:, free_idx]
        
        if args.method == 'ref':
            free = marginalize(free)
            cv = np.arange(-np.pi, np.pi, 2*np.pi/51)

        pmfs.append(free)
        
    pmfs = np.array(pmfs)
    mean_pmf = np.mean(pmfs, axis=0)
    mean_pmf = mean_pmf - mean_pmf.min()
    std_pmf = np.std(pmfs, axis=0)

    plt.plot(cv, mean_pmf)
    plt.title('FES over CV', fontsize=20, fontweight="medium")
    plt.fill_between(cv, mean_pmf - std_pmf, mean_pmf + std_pmf, alpha=0.2)
    plt.xlabel(bar_labels[args.method], fontsize=20, fontweight="medium")
    plt.ylabel('FES', fontsize=20, fontweight="medium")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlim(cv.min(), cv.max())
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'./fig/fes_{args.method}_{args.ns}.png', dpi=300, bbox_inches="tight")
    plt.savefig(f'./fig/fes_{args.method}_{args.ns}.pdf', dpi=300, bbox_inches="tight")
    wandb.log({f"fes": wandb.Image(f'./fig/fes_{args.method}_{args.ns}.png')})
    plt.show()
    plt.close()
    
    return


# def plot_fes_over_cv(args, base_dir):

#     for seed in range(0, args.seed + 1):
#         fes_file = os.path.join(base_dir, 'log', args.date, str(seed), "fes-raw.dat")

#     return