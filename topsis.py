import pandas as pd
from functions import concatData, clearData, TOPSIS

#Reading data
data = concatData()

#Cleaning data
data = clearData(data)

#Filtering out GKs
data = data[data['Pos']!='GK']

#Filtering out players with under 2k mins
data = data[data['Min']>2000]

#TOPSIS
destimulants = ['CrdY', 'CrdR', 'Mis', 'Dis']
topsis = TOPSIS(data, 7, destimulants)

top5 = topsis.iloc[:5,:]

top5 = pd.merge(top5, data, how='left')