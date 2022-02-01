from ase import Atoms
import re
import os
import numpy as np
import re
import warnings
from ase.units import Hartree, Bohr
force_unit = Hartree/Bohr
from ase.calculators.singlepoint import SinglePointCalculator

def get_dft_force(output_file):
    all_data = []
    extract = False
    txt = open(output_file, 'r').read()
    r = re.findall(r'^.*CONV.*(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)', txt, flags=re.MULTILINE)
    cell = Bohr*np.array(r, dtype=float)
    with open (output_file, 'r') as f:
        for line1 in f:
            if (extract == True and (re.search('CHGPRO', line1) or re.search('NEB', line1) or re.search('GDIIS', line1) or re.search('QMD', line1))):
                force_data = []
                positions = []
                species = []
                energy, f_max, f_rms = Hartree*float(data[1][1]), force_unit*float(data[1][2]), force_unit*float(data[1][3])
                for line2 in data[5:]:
                    if (len(line2) == 0):
                        break
                    elif (line2[0] != 'MD:'):
                        break
                    species.append (line2[2])
                    positions.append (line2[3:6])
                    force_data.append (line2[6:9])
                positions = Bohr*np.array(positions, dtype = float)
                force_data = force_unit*np.array(force_data, dtype = float)
                slab = Atoms(species, positions = positions, cell=cell)
                calculator = SinglePointCalculator(slab, forces = force_data,energy=energy)
                slab.set_calculator(calculator)
                all_data.append(slab)
                extract = False
            elif (extract == False and re.search('CONVERGED ENERGY AND FORCES', line1)):
                extract = True
                data = []
            elif (extract == True and not(re.search('CONVERGED ENERGY AND FORCES', line1))):
                data.append(line1.split())
            elif (extract == False and not(re.search('CONVERGED ENERGY AND FORCES', line1))):
                pass
    slab_final = all_data[-1]
    final_forces = slab_final.get_forces()
    final_energy = slab_final.get_potential_energy()
    
    return slab_final, final_energy, final_forces
def n2p2_input_from_state_output(directory):
    paths = [os.path.join(root,file) for root, dirs, files in os.walk(directory) for file in files]

    with open('input.data', 'w') as f:
        for path in paths:
            print(path)
            structure, energy, forces = get_dft_force(path)
            print('begin', file=f)
            for cell in structure.cell:
                print('lattice', *cell, file=f)
            for i, j in enumerate(structure):
                print('atom', *j.position, j.symbol,'0.0','0.0',*forces[i], file=f)
            print('energy', energy, file=f)
            print('end', file=f)

# structure, energy, forces = get_dft_force('./nfout_1_1.5')
n2p2_input_from_state_output('/home/yyamada/database/data')