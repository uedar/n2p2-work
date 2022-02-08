import re
from ase.units import Hartree, Bohr
import numpy as np
from ase import Atoms

def read_state_trajectory(output_file):
    force_unit = Hartree/Bohr
    full_text = open(output_file, 'r').read()
    cell = Bohr*np.array(re.findall(r'^.*CONV.*\s([-|\d]+\.\d+)\s+([-|\d]+\.\d+)\s+([-|\d]+\.\d+)', full_text, flags=re.MULTILINE), dtype=float)
    energy = Hartree*np.array([p.split()[1] for p in re.findall(r'CONVERGED ENERGY AND FORCES(.*\n){3}', full_text)], dtype=float)
    trajectory = [f[0] for f in re.findall(r'ATOM\s*COORDINATES\s*FORCES\nMD.*\n((MD.*\n)*)',full_text)]
    ase_traj = []
    forces = []
    for atoms in trajectory:
        atoms_array = atoms.strip().split('\n')
        species = np.array([atom_str.split()[2] for atom_str in d1])
        positions = Bohr*np.array([atom_str.split()[3:6] for atom_str in atoms_array], dtype=float)
        structure = Atoms(symbols=species, positions = positions, cell=cell)
        ase_traj.append(structure)
        forces.append([atom_str.split()[6:9] for atom_str in atoms_array])
    return ase_traj, energy, force_unit*np.array(forces, dtype=float)

with open('input.data', 'w') as f:
    for idx in range(15):
        traj, energy, forces = read_state_trajectory(f'/home/ueda/for-UEDA/nfout_md{idx+1}')
        for i, atoms in enumerate(traj):
            for cell in atoms.cell:
                print('lattice', *cell, file=f)
            for j, k in enumerate(atoms):
                print('atom', *k.position, k.symbol,'0.0','0.0',*forces[i][j], file=f)
            print('energy', energy, file=f)
            print('end', file=f)