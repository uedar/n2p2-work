import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

name = input("file name?  name_testforces.out    ")

txt = open('./data/' + name + '_testforces.out', 'r').readlines()
forces = np.array([row.split() for row in txt[13:]])
df = pd.DataFrame(forces)
df.columns = ['index_a',
              'index_b',
              'Fref',
              'Fnnp',
              ]

df = df.drop(columns=['index_a','index_b'])

v_max = []

for col in df.columns:
    df[col] = df[col].astype(float)
    v_max.append(max(abs(df[col])))
        
x = max(v_max) + 1

#plot
fig = plt.figure()
plt.plot(np.linspace(-x,x),np.linspace(-x,x), color='red', zorder=1)
plt.scatter(df['Fref'], df['Fnnp'], zorder=2)
plt.xlabel("Reference force")
plt.ylabel("NNP force")
plt.title(name)
fig.savefig('./fig/' + name + '_validation_F.png')