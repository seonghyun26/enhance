import os
import wandb
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm

from .constant import *


def plot_phi_distribution(args, base_dir):
    wandb_image_list = []
    
    for seed in tqdm(
        range(0, args.seed + 1),
        desc="Plotting phi distribution",
        total=args.seed + 1
    ):
        # Load COLVAR data
        cv_dir = os.path.join(base_dir, 'log', args.date, str(seed), 'COLVAR')
        data = np.loadtxt(cv_dir, comments='#')
        
        # Read data
        with open(cv_dir, 'r') as file:
            first_line = file.readline().strip()
            keys = first_line.split()[2:]
        time_horizon = int(data[:, keys.index('time')][-1])
        phi = data[:, keys.index('phi')]
        cv = data[:,keys.index(cv_name[args.method])]
        time_ns = np.arange(0, time_horizon + 1) * 0.001
        
        # Plotting
        cmap = plt.get_cmap('viridis')
        norm = plt.Normalize(cv.min(), cv.max())
        colors = cmap(norm(cv))
        
        # Plot data        
        plt.figure(figsize=(12, 6))
        scatter = plt.scatter(time_ns, phi, c=colors, s=10)
        # cbar = plt.colorbar(scatter)
        # cbar.set_label(bar_labels[args.method],fontsize=20, fontweight="medium")
        # cbar.ax.tick_params(labelsize=14)
        scatter.set_clim(cv.min(), cv.max())
        
        # Count phi
        phi_negative = phi[phi < 0].shape[0] / phi.shape[0]
        phi_positive = phi[phi > 0].shape[0] / phi.shape[0]
        print(phi.shape)
        print(phi_positive, phi_negative)
        
        # Customize plot
        plt.xlabel('Time (ns)', fontsize=FONTSIZE, fontweight="medium")
        plt.ylabel(r'$\phi$', fontsize=FONTSIZE, fontweight="medium")
        plt.xlim(0,20)
        plt.ylim(-np.pi,np.pi)
        plt.xticks(np.arange(0, 21, 5),fontsize=FONTSIZE_SMALL)  
        plt.yticks(fontsize=FONTSIZE_SMALL)
        # plt.title(f'{args.method}', fontsize=20, fontweight="medium")
        plt.tight_layout()
        plt.savefig(f'./fig/phi_{args.method}_{args.ns}_{seed}.png', dpi=300, bbox_inches="tight")
        plt.savefig(f'./fig/phi_{args.method}_{args.ns}_{seed}.pdf', dpi=300, bbox_inches="tight")
        wandb.log({
            f"phi_distribution/{seed}": wandb.Image(f"./fig/phi_{args.method}_{args.ns}_{seed}.png"),
            f"phi_positive/{seed}": phi_positive,
            f"phi_negative/{seed}": phi_negative,
        })
        print(f'Figure saved at ./fig/phi_{args.method}_{args.ns}.png')
        plt.close()
        
    return wandb_image_list