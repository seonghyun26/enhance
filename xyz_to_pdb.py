import os
import numpy as np

def read_xyz(filename, frame):
    with open(filename, 'r') as file:
        lines = file.readlines()
        num_atoms = int(lines[0].strip())
        frames = len(lines) // (num_atoms + 2)
        if frame >= frames:
            raise ValueError("Frame number exceeds the total number of frames in the file.")
        start = frame * (num_atoms + 2) + 2
        end = start + num_atoms
        positions = []
        for line in lines[start:end]:
            parts = line.split()
            positions.append([float(parts[1]), float(parts[2]), float(parts[3])])
        return 10*np.array(positions) # Convert from nm to Angstrom

def update_pdb(xyz_positions, pdb_filename, output_filename):
    with open(pdb_filename, 'r') as file:
        pdb_lines = file.readlines()
    
    atom_index = 0
    with open(output_filename, 'w') as file:
        for line in pdb_lines:
            if line.startswith(('ATOM', 'HETATM')):
                parts = line.split()
                parts[6] = f"{xyz_positions[atom_index][0]:8.3f}"
                parts[7] = f"{xyz_positions[atom_index][1]:8.3f}"
                parts[8] = f"{xyz_positions[atom_index][2]:8.3f}"
                file.write("{:<6}{:>5} {:<4} {:<3} {:<1}{:>4}    {:>8}{:>8}{:>8} {:>6} {:>6}           {:<2}\n".format(*parts))
                atom_index += 1
            else:
                file.write(line)

def process_all_frames(xyz_filename, pdb_filename, output_dir):
    with open(xyz_filename, 'r') as file:
        lines = file.readlines()
        num_atoms = int(lines[0].strip())
        frames = len(lines) // (num_atoms + 2)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for frame in range(frames):
        xyz_positions = read_xyz(xyz_filename, frame)
        output_filename = os.path.join(output_dir, f"{frame}.pdb")
        update_pdb(xyz_positions, pdb_filename, output_filename)

molecule = 'aldp'

xyz_filename = f'/home/guest_sky/enhance/data/{molecule}/enhance.xyz'
pdb_filename = f'/home/guest_sky/enhance/data/{molecule}/init.pdb'
output_dir = f'/home/guest_sky/enhance/data/{molecule}/frames'

process_all_frames(xyz_filename, pdb_filename, output_dir)