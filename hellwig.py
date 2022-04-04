import chardet
import pandas as pd
import csv
from functions import clearData,Hellwig

#Finding proper encoding
with open('data/PL_StandStats.csv', 'rb') as f:
    enc = chardet.detect(f.read())
    
#Reading all files

PL_StandStats = pd.read_csv('data/PL_StandStats.csv', 
                            encoding = enc['encoding'], delimiter=',', 
                            quoting=csv.QUOTE_NONE)

PL_Creation = pd.read_csv('data/PL_Creation.csv', 
                            encoding = enc['encoding'], delimiter=',', 
                            quoting=csv.QUOTE_NONE)
PL_Creation = PL_Creation.iloc[:,2:]

PL_Passes = pd.read_csv('data/PL_Passes.csv', 
                            encoding = enc['encoding'], delimiter=',', 
                            quoting=csv.QUOTE_NONE)
PL_Passes = PL_Passes.iloc[:,2:]

PL_Shoots = pd.read_csv('data/PL_Shoots.csv', 
                            encoding = enc['encoding'], delimiter=',', 
                            quoting=csv.QUOTE_NONE)
PL_Shoots = PL_Shoots.iloc[:,2:]

PL_Possesion = pd.read_csv('data/PL_Possesion.csv', 
                            encoding = enc['encoding'], delimiter=',', 
                            quoting=csv.QUOTE_NONE)
PL_Possesion = PL_Possesion.iloc[:,2:]

data = pd.concat([PL_StandStats, PL_Creation, PL_Passes, PL_Shoots, PL_Possesion],
                 axis=1)
#Cleaning data
data = clearData(data)

#Filtering out GKs
data = data[data['Pos']!='GK']

#Filtering out players with under 1k mins
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
