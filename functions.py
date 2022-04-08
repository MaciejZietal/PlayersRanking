import pandas as pd
import statistics
import csv
import chardet

def concatData():
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
    
    return data

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


def TOPSIS(data, startCol, destimulants):
    
    normalizedM = normalizedMatrix(data, startCol)
    stimulantsM = normalizedM.drop(destimulants, axis=1)
    destimulantsM = normalizedM[destimulants]
    
    sPlus = distToBests(stimulantsM, destimulantsM)
    sMinus = distToWorsts(stimulantsM, destimulantsM)
    
    pi = Pi(sPlus, sMinus)
    
    rank = rankingTOPSIS(pi, data['Player'])
    return rank

def normalizedMatrix(data, startCol):
    sumSquare = list((data.iloc[:,startCol:].pow(2).sum())**(1/2))
    normalizedMatrix = data.iloc[:,7:].div(sumSquare)
    
    return normalizedMatrix

def distToBests(normalizedStimulants, normalizedDestimulants):
    maximum = list(normalizedStimulants.max())
    minimum = list(normalizedDestimulants.min())
    
    bests = maximum + minimum
    normalizedM = pd.concat([normalizedStimulants, normalizedDestimulants], axis=1)
    
    for i in range(normalizedM.shape[1]):
        normalizedM.iloc[:,i] = (normalizedM.iloc[:,i] - bests[i])**2
    
    sPlus = list(normalizedM.sum(axis=1)**(1/2))
    
    return sPlus

def distToWorsts(normalizedStimulants, normalizedDestimulants):
    minimum = list(normalizedStimulants.min())
    maximum = list(normalizedDestimulants.max())
    
    bests = minimum + maximum
    normalizedM = pd.concat([normalizedStimulants, normalizedDestimulants], axis=1)
    
    for i in range(normalizedM.shape[1]):
        normalizedM.iloc[:,i] = (normalizedM.iloc[:,i] - bests[i])**2
    
    sMinus = list(normalizedM.sum(axis=1)**(1/2))
    
    return sMinus

def Pi(sPlus, sMinus):
    suM = [i + j for i, j  in zip(sPlus, sMinus)]
    Pi = [i / j  for i,j in zip(sMinus, suM)]
    
    return Pi

def rankingTOPSIS(pi, players):
    ranking = pd.DataFrame({'Player': players, 'Rank':pi})
    ranking.sort_values(by=['Rank'],inplace=True, ascending=False)
    
    return ranking


    