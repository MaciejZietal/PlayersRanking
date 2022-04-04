import pandas as pd
import statistics

def clearData(data):
    #Deleting numbers from Player names
    data['Player'] = data['Player'].str.split('\\').str[0]
    
    #Finding columns with wrong chars
    strCols = list((data.applymap(type)==str).all(0))
    strCols = data.iloc[:,strCols]
    strColsNames = list(strCols.columns)
    
    #Deleting special characters in rows
    for col in strColsNames:
        data[col] = data[col].str.replace('"', '')
    
    #Changing columns names
    strColsNamesNew = [x.replace('"', '') for x in strColsNames] 
    columns = dict(zip(strColsNames,strColsNamesNew))
    data.rename(columns=columns, inplace=True)
    
    #Changing data type to numeric
    data.iloc[:,3:] = data.iloc[:,3:].apply(pd.to_numeric)
    
    #Replacing NaN with 0
    data = data.fillna(0)
    
    return data

def standarize(data):
    nCols = data.shape[1]
    for i in range(nCols):
        m = statistics.mean(data.iloc[:,i])
        std = statistics.stdev(data.iloc[:,i])
        data.iloc[:,i] = (data.iloc[:,i]-m)/std
        
    return data

def findBest(dataStand):
    nCols = dataStand.shape[1]
    bests = []
    for i in range(nCols):
        best = max(dataStand.iloc[:,i])
        bests.append(best)
        
    return bests

def distToBest(dataStand):
    bests = findBest(dataStand)
    distances = dataStand.copy()
    
    for i in range(distances.shape[1]):
        distances.iloc[:,i] = (dataStand.iloc[:,i] - bests[i])**2
        
    distances['Total'] = distances.sum(axis=1)**(1/2)
    return distances

def ranking(distances, names):
    m = statistics.mean(distances.iloc[:,-1])
    std = statistics.stdev(distances.iloc[:,-1])
    d0 = m + 2*std
    
    rank = 1-(distances.iloc[:,-1]/d0)
    
    ranking = pd.DataFrame({'Player':names,'Rank':rank})
    ranking.sort_values(by=['Rank'],inplace=True, ascending=False)
    return ranking
    

def Hellwig(data, startCol):
    names = list(data.iloc[:,1])
    dataStand = standarize(data.iloc[:,startCol:])
    distances = distToBest(dataStand)
    
    ranks = ranking(distances, names)
    return ranks