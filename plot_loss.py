import numpy as np
import pandas as pd
import re

def plot_loss(file_path, column_name, write_csv=False):
    txt = open(file_path, 'r').readlines()
    columns = [s for s in txt if re.match('#\s*epoch.*', s)][0].split()[1:]
    extract_loss = [s for s in txt if re.match('\s*\d\s*.*', s)]
    loss = [s.split() for s in extract_loss]
    df = pd.DataFrame(loss)
    df.columns = columns
    for col in df.columns:
        if col == 'epoch':
            df[col] = df[col].astype(int)
        else:
            df[col] = df[col].astype(float)

    df.plot('epoch', column_name, marker='o')
    if write_csv:
        df.to_csv('learning_curve.csv',index=False)
plot_loss('./learing_curve2.out','RMSEpa_Etrain_pu', write_csv=True)
