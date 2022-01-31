import numpy as np
import pynnp

def acsf_vector(atoms, energy, forces, pynnp_mode):
    input_lines = 'begin\n'
    for component in atoms.cell:
        input_lines += f'lattice {"".join([" " + str(c) for c in component])}\n'
    for position, symbol, force in zip(atoms.positions, atoms.symbols, forces):
        input_lines += f'atom {"".join([" " + str(p) for p in position])} {symbol} 0.0 0.0 {"".join([" " + str(f) for f in force])}\n'
    input_lines += f'energy {energy}\n'
    input_lines += 'end'
    input_arr = input_lines.split('\n')
    s = pynnp.Structure()
    s.setElementMap(pynnp_mode.elementMap)
    s.readFromLines(input_arr)
    cutoffRadius = pynnp_mode.getMaxCutoffRadius()
    s.calculateNeighborList(cutoffRadius)
    pynnp_mode.calculateSymmetryFunctionGroups(s, False)
    symm_f = np.array([atom.G for atom in s.atoms]).flatten()
    return symm_f