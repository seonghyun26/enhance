import os
import wandb
import numpy as np
import argparse
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def parse_args():
    parser = argparse.ArgumentParser(description='Train TBG model')
    parser.add_argument('--date', type=str, default = "debug", help='Date for the experiment')
    parser.add_argument('--method', type=str, default = "DeepLDA", help='Date for the experiment')
    parser.add_argument('--ns', type=int, default = 10, help = "Length of simulation used for dataset")
    
    return parser.parse_args()

args = parse_args()

cv_name = {
    'ref': 'phi',
    'phi': 'phi',
    'AE': 'deep.node-0',
    'TAE': 'deep.node-0',
    'VDE': 'deep.node-0',
    'DeepTDA': 'deep.node-0',
    'DeepLDA': 'deep.node-0',
    'DeepTICA': 'deep.node-0',
    'TBG': 'deep.node-0',
}
bar_labels = {
    'ref': r'$\phi$',
    'phi': r'$\phi$',
    'AE': 'MLCV',
    'TAE': 'MLCV',
    'VDE': 'MLCV',
    'DeepLDA': 'MLCV',
    'TBG': 'MLCV',
    'DeepTDA': 'MLCV',
    'DeepTICA': 'MLCV',
}

wandb.init(
    project="enhanced-sampling",
    entity="eddy26",
    tags = args.tags,
    config = vars(args),
)

methods = [args.method]
dates = []
# base_dir = f'/home/shpark/prj-mlcv/lib/enhance/simulations/aldp'
base_dir = f'{os.getcwd()}/simulations/aldp'

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

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

def load_data(fes_dir, method, i):
    fes_file = os.path.join(fes_dir, 'fes', str(i)+".dat")

    # Load data from the file
    data = np.loadtxt(fes_file, comments='#')
    
    with open(fes_file, 'r') as file:
        first_line = file.readline().strip()
        
    keys = first_line.split()[2:]
    phi_idx = keys.index(cv_name[method])
    free_idx = keys.index('file.free')

    phi = data[:, phi_idx]
    free = data[:, free_idx]
    return phi, free

def load_interp(fes_dir, method, i):
    fes_file = os.path.join(fes_dir, 'fes', str(i)+".dat")
    cv_file = os.path.join(fes_dir, "COLVAR")

    # Load data from the file
    data = np.loadtxt(fes_file, comments='#')
    
    with open(fes_file, 'r') as file:
        first_line = file.readline().strip()
        
    keys = first_line.split()[2:]
    cv_idx = keys.index(cv_name[method])
    free_idx = keys.index('file.free')

    cv_grid = data[:, cv_idx]
    free_grid = data[:, free_idx]

    # Load data from the file
    data = np.loadtxt(cv_file, comments='#')
    
    with open(cv_file, 'r') as file:
        first_line = file.readline().strip()
        
    keys = first_line.split()[2:]
    cv_idx = keys.index(cv_name[method])
    phi_idx = keys.index('phi')

    cv = data[:, cv_idx]
    phi = data[:, phi_idx]

    fes_interp = interp1d(
        cv_grid, 
        free_grid, 
        kind='linear', 
        fill_value="extrapolate"
    )

    free = fes_interp(cv)
    return phi, free
    
    
    


def plot_phi_distribution(method, ns, cv_dir):
    data = np.loadtxt(cv_dir, comments='#')
    with open(cv_dir, 'r') as file:
        first_line = file.readline().strip()
    keys = first_line.split()[2:]
    phi_idx = keys.index('phi')
    cv_idx = keys.index(cv_name[method])
    phi = data[:, phi_idx]
    print(phi.shape)
    cv = data[:,cv_idx]
    time_ns = np.arange(0, 20001) * 0.001  # ns

    cmap = plt.get_cmap('viridis')
    norm = plt.Normalize(cv.min(), cv.max())
    colors = cmap(norm(cv))

    plt.figure(figsize=(12, 6))
    scatter=plt.scatter(time_ns, phi, c=colors, s=10, label=f'{method}')
    cbar=plt.colorbar(scatter)
    cbar.set_label(bar_labels[method],fontsize=20, fontweight="medium")
    cbar.ax.tick_params(labelsize=14)
    scatter.set_clim(cv.min(), cv.max())
    plt.xlabel('Time (ns)', fontsize=20, fontweight="medium")
    plt.ylabel(r'$\phi$', fontsize=20, fontweight="medium")

    plt.xlim(0,20)
    plt.ylim(-np.pi,np.pi)
    plt.xticks(np.arange(0, 21, 5),fontsize=14)  
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)
    plt.tight_layout()
    plt.savefig(f'./fig/phi_distribution_{method}_{ns}.pdf', dpi=300, bbox_inches="tight")
    plt.savefig(f'./fig/phi_distribution_{method}_{ns}.png', dpi=300, bbox_inches="tight")
    print(f'Figure saved at ./fig/phi_distribution_{method}_{ns}')
    plt.show()
    plt.close()

dates.append(args.date)
# for method in methods:
    # date = sorted(os.listdir(os.path.join(base_dir, method, ns, 'log')))[-1]
    # date = "0422033357"
    # dates.append(date)
plot_free_energy_difference(methods, args.ns, dates, base_dir)

cv_dir = os.path.join(base_dir, methods[0], args.ns, 'log', dates[0], '0', 'COLVAR')
plot_phi_distribution(methods[0], args.ns, cv_dir)