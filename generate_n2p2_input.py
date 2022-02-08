import re
import warnings
from ase.units import Hartree, Bohr
import numpy as np
from ase import Atoms
import os
import sys

force_unit = Hartree/Bohr
# directory = sys.argv[1]

def read_state_output(output_file):  
    data = []
    extract = False
    txt = open(output_file, 'r').read()
    r = re.findall(r'^.*CONV.*\s([-|\d]+\.\d+)\s+([-|\d]+\.\d+)\s+([-|\d]+\.\d+)', txt, flags=re.MULTILINE)
    cell = Bohr*np.array(r, dtype=float)
    with open (output_file) as fd:
        lines = fd.readlines()
        if 'The calculation has converged' not in str(lines):
            warnings.warn('The calculation has not converged')
        for line in lines:
            re.search('CONV. LAT. VECTOR(BOHR)', line)
            if re.search('CONVERGED', line):
                extract = True
            if extract:
                data.append (line.split())
                if re.search('EXIT', line):
                    extract = False
    energy, f_max, f_rms = Hartree*float(data[2][1]), force_unit*float(data[2][2]), force_unit*float(data[2][3])
    force_data = []
    positions = []
    species = []
    for line in data[6:]:
        if (line == []):
            break
        species.append (line[2])
        positions.append (line[3:6])
        force_data.append (line[6:9])
    positions = Bohr*np.array(positions, dtype=float)
    structure = Atoms(symbols=species, positions = positions, cell=cell)
    forces = force_unit*np.array(force_data, dtype=float)
    return structure, energy, forces

def n2p2_input_from_state_output(directory):
    paths = [os.path.join(root,file) for root, dirs, files in os.walk(directory) for file in files]

    with open('input.data', 'w') as f:
        for path in paths:
            structure, energy, forces = read_state_output(path)
            print('begin', file=f)
            for cell in structure.cell:
                print('lattice', *cell, file=f)
            for i, j in enumerate(structure):
                print('atom', *j.position, j.symbol,'0.0','0.0',*forces[i], file=f)
            print('energy', energy, file=f)
            print('end', file=f)

# n2p2_input_from_state_output(directory)