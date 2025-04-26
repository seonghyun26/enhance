import os
import wandb
import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d

from .constant import *

def load_fes_data(log_dir, method, idx):
    # Load file
    fes_file = os.path.join(log_dir, 'fes', str(idx)+".dat")
    fes_data = np.loadtxt(fes_file, comments='#')
    with open(fes_file, 'r') as file:
        first_line = file.readline().strip()

    # Load keys
    keys = first_line.split()[2:]
    phi_idx = keys.index(cv_name[method])
    free_idx = keys.index('file.free')
    
    # Loda data
    if method in ['phi','ref']:
        phi = fes_data[:, phi_idx]
        free = fes_data[:, free_idx]
        return phi, free
    
    else:
        # Load grid information
        cv_idx = keys.index(cv_name[method])
        cv_grid = fes_data[:, cv_idx]
        free_grid = fes_data[:, free_idx]
        
        # Load colvar data
        cv_file = os.path.join(log_dir, "COLVAR")
        with open(cv_file, 'r') as file:
            first_line = file.readline().strip()
            colvar_keys = first_line.split()[2:]
        colvar_cv_idx = colvar_keys.index(cv_name[method])
        colvar_phi_idx = colvar_keys.index('phi')
        cv_data = np.loadtxt(cv_file, comments='#')
        cv = cv_data[:, colvar_cv_idx]
        phi = cv_data[:, colvar_phi_idx]

        # Compute FES
        fes_interp = interp1d(
            cv_grid, 
            free_grid, 
            kind='linear', 
            fill_value="extrapolate"
        )
        free = fes_interp(cv)
        
        return phi, free


def calculate_delta_f(phi, free):    
    # Filter data based on conditions
    A = free[phi < 0]
    B = free[(phi > 0) & (phi < 2.2)]
    
    # Calculate free energies
    fesA = -2.49 * np.logaddexp.reduce(-1 / 2.49 * A)
    fesB = -2.49 * np.logaddexp.reduce(-1 / 2.49 * B)
    if np.isnan(fesB-fesA) or np.isinf(fesB-fesA):
        return np.nan
    return fesB - fesA


def plot_free_energy_difference(args, base_dir):
    # Load time information
    cv_dir = os.path.join(base_dir, 'log', args.date, '0', 'COLVAR')
    data = np.loadtxt(cv_dir, comments='#')
    with open(cv_dir, 'r') as file:
        first_line = file.readline().strip()
        keys = first_line.split()[2:]
    time_horizon = int(data[:, keys.index('time')][-1]) // 200
    times = np.linspace(0, 20, time_horizon + 1)
    
    # Compute FES
    seed_delta_fs = []
    for seed in range(0, args.seed + 1):
        log_dir = os.path.join(base_dir, 'log', args.date, str(seed))
        delta_fs = []
        
        # Compute delta F over time
        for HILLS_idx in range(time_horizon + 1):
            phi, free = load_fes_data(log_dir, args.method, HILLS_idx)
            fes = calculate_delta_f(phi, free)
            delta_fs.append(fes)
        wandb.log({f"delta_f/{seed}": delta_fs})
        seed_delta_fs.append(delta_fs)
    delta_fs = np.array(seed_delta_fs)
    mean_delta_fs = np.nanmean(delta_fs, axis=0)
    std_delta_fs = np.nanstd(delta_fs, axis=0)
    
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    c = colors.pop(0)
    mask = ~np.isnan(mean_delta_fs)
    plt.figure(figsize=(10, 6))
    if mask.sum() == 0:
        plt.plot(times, np.zeros_like(times), alpha=0.0)
    else:
        plt.plot(times[mask], mean_delta_fs[mask], color=c)
        plt.fill_between(times[mask], mean_delta_fs[mask] - std_delta_fs[mask], mean_delta_fs[mask] + std_delta_fs[mask], alpha=0.2, color=c)

    plt.xlim(0,20)
    plt.ylim(-20,50)
    plt.axhline(y=9.04, color='r', linestyle='--', label='GT')
    plt.fill_between(times, 9.04 - 0.33, 9.37, color='r', alpha=0.2)
    plt.xlabel('Time (ns)', fontsize=20, fontweight="medium")
    plt.ylabel(r'$\Delta F$'+' (kJ/mol)', fontsize=20, fontweight="medium")
    plt.title(r'$\Delta F$' + f' over {args.method}', fontsize=20, fontweight="medium")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'./fig/deltaf_{args.method}_{args.ns}.pdf', dpi=300, bbox_inches="tight")
    plt.savefig(f'./fig/deltaf_{args.method}_{args.ns}.png', dpi=300, bbox_inches="tight")
    wandb.log({
        f"delta_f": wandb.Image(f'./fig/deltaf_{args.method}_{args.ns}.png'),
        f"delta_f_mean": mean_delta_fs,
        f"delta_f_std": std_delta_fs,
    })
    print(f'Figure saved at ./fig/deltaf_{args.method}_{args.ns}.png')
    plt.show()
    plt.close()
    
    return 