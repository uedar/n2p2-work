import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

txt = open('./nnforces.out', 'r').readlines()
forces = np.array([row.split() for row in txt[18:]])
df = pd.DataFrame(forces)
df.columns = ['fx', 
              'fy',
              'fz',
              'fxRef',
              'fyRef',
              'fzRef',
              'fxDiff',
              'fyDiff',
              'fzDiff'
             ]
for col in df.columns:
    df[col] = df[col].astype(float)
nn_force_component = pd.concat([df['fx'],df['fy'], df['fz']]) 
dft_force_component = pd.concat([df['fxRef'],df['fyRef'], df['fzRef']])
diff_force_component = pd.concat([df['fxDiff'],df['fyDiff'], df['fzDiff']])
concat_force_component = pd.concat([nn_force_component,dft_force_component, diff_force_component], axis=1)
concat_force_component.columns = ['nn_force', 'dft_force','diff']
concat_force_component['nn_force'] *= 1000
concat_force_component['dft_force'] *= 1000
concat_force_component['diff'] *= 1000

mae = abs(concat_force_component['diff']).sum() / len(concat_force_component)
print(f'MAE: {mae} mev/Å')
fig = plt.figure()
plt.plot(np.linspace(-300,300), np.linspace(-300,300))
plt.scatter(concat_force_component['dft_force'],concat_force_component['nn_force'])
plt.title(f'MAE: {mae}mev/Å')
plt.xlabel('DFT force components (meV/Å)')
plt.ylabel('NN FF force components (meV/Å)')
fig.savefig('validation')
