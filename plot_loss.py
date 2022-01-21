import numpy as np
import pandas as pd

def plot_loss(file_path, column_name):
    txt = open(file_path, 'r').readlines()
    loss = np.array([row.split() for row in txt[23:]])
    df = pd.DataFrame(loss)
    df.columns = ['epoch', 
                  'RMSEpa_Etrain_pu', 
                  'RMSEpa_Etest_pu', 
                  'RMSE_Etrain_pu', 
                  'RMSE_Etest_pu', 
                  'MAEpa_Etrain_pu', 
                  'MAEpa_Etest_pu',
                  'MAE_Etrain_pu',
                  'MAE_Etest_pu',
                  'RMSE_Ftrain_pu',
                  'RMSE_Ftest_pu',
                  'RMSE_Ftest_pu',
                  'MAE_Ftest_pu'
                 ]

    for col in df.columns:
        if col == 'epoch':
            df[col] = df[col].astype(int)
        else:
            df[col] = df[col].astype(float)

    df.plot('epoch', column_name, marker='o')

plot_loss('./learning-curve.out','RMSEpa_Etrain_pu')
