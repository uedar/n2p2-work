import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

name = input("file name?  name_testpoints.out    ")

txt = open('./data/' + name + '_testpoints.out', 'r').readlines()
forces = np.array([row.split() for row in txt[12:]])
df = pd.DataFrame(forces)
df.columns = ['index',
              'Eref',
              'Ennp',
              ]

v_max = []

for col in df.columns:
    if col == 'index':
        df[col] =df[col].astype(int)
    else:
        df[col] = df[col].astype(float)
        v_max.append(max(abs(df[col])))
        
x = max(v_max) + 1


#plot
fig = plt.figure()
plt.plot(np.linspace(-x,x),np.linspace(-x,x), color='red', zorder=1)
plt.scatter(df['Eref'], df['Ennp'], zorder=2)
plt.xlabel("Reference potential energy per atom")
plt.ylabel("NNP potential energy per atom")
plt.title(name)
fig.savefig('./fig/' + name + '_validation_P.png')
