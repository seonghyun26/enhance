import numpy as np

# FES 파일 불러오기
fes = np.loadtxt("fes.dat", comments="#")

# phi (rad 단위), free energy (kJ/mol)
phi = fes[:, 0]
free = fes[:, 1]

# ΔF 계산할 두 상태 (예: -1.5와 +1.5 부근)
def window_mask(center, width=0.1):
    return (phi > center - width) & (phi < center + width)

mask_A = window_mask(-1.5)
mask_B = window_mask(+1.5)

F_A = np.mean(free[mask_A])
F_B = np.mean(free[mask_B])
deltaF = F_B - F_A

print(f"Mean F_A (phi ≈ -1.5): {F_A:.3f} kJ/mol")
print(f"Mean F_B (phi ≈ +1.5): {F_B:.3f} kJ/mol")
print(f"ΔF = F_B - F_A = {deltaF:.3f} kJ/mol")