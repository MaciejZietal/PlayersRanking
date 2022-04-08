import pandas as pd
from functions import clearData,Hellwig, concatData

#Reading data
data = concatData()

#Cleaning data
data = clearData(data)

#Filtering out GKs
data = data[data['Pos']!='GK']

#Filtering out players with under 2k mins
data = data[data['Min']>2000]

#Changing destimulants to stimulants
data['CrdY'] = data['CrdY'] * (-1)
data['CrdR'] = data['CrdR'] * (-1)
data['Mis'] = data['Mis'] * (-1)
data['Dis'] = data['Dis'] * (-1)

#Hellwig
hellwig = Hellwig(data,7)

#Top 5 players
top5 = hellwig.iloc[:5,:]

#Finding top5 players stats
new = pd.merge(top5, data, how='left')

#Saving results to csv
new.to_csv('data/hellwig.csv')
