import pandas as pd
import statistics
import csv
import chardet

def concatData():
    """
    A function that reads and connect data for further analysis.

    Returns
    -------
    data : pandas Data Frame
        A data frame with connected data

    """
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
    """
    A function that clears data.

    Parameters
    ----------
    data : pandas Data Frame
        A data frame with players statistics

    Returns
    -------
    data : pandas Data Frame
        A cleared data frame, ready for further analysis

    """
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
    """
    A function that make a standardization  of a data frame

    Parameters
    ----------
    data : pandas Data Frame
        A data frame with columns to standarization

    Returns
    -------
    data : pandas Data Frame
        A data frame with standarized columns

    """
    nCols = data.shape[1]
    for i in range(nCols):
        m = statistics.mean(data.iloc[:,i])
        std = statistics.stdev(data.iloc[:,i])
        data.iloc[:,i] = (data.iloc[:,i]-m)/std
        
    return data

def findBest(dataStand):
    """
    A function that is finding best value in each column

    Parameters
    ----------
    dataStand : pandas Data Frame
        Standarized data frame.

    Returns
    -------
    bests : list
        A list containing highest values in each column

    """
    nCols = dataStand.shape[1]
    bests = []
    for i in range(nCols):
        best = max(dataStand.iloc[:,i])
        bests.append(best)
        
    return bests

def distToBest(dataStand):
    """
    A function calculating distance to best values of each player

    Parameters
    ----------
    dataStand : pandas Data Frame
        Standarized data frame

    Returns
    -------
    distances : pandas Data Frame
        Data Frame with calculated total distance to best values.

    """
    bests = findBest(dataStand)
    distances = dataStand.copy()
    
    for i in range(distances.shape[1]):
        distances.iloc[:,i] = (dataStand.iloc[:,i] - bests[i])**2
        
    distances['Total'] = distances.sum(axis=1)**(1/2)
    return distances

def ranking(distances, names):
    """
    A function calculating Hellwig ranking

    Parameters
    ----------
    distances : pandas Data Frame
        A data frame containing total distance to best values of each player.
    names : list
        A list of players names.

    Returns
    -------
    ranking : pandas Data Frame
        A data frame containing Hellwig ranking.

    """
    m = statistics.mean(distances.iloc[:,-1])
    std = statistics.stdev(distances.iloc[:,-1])
    d0 = m + 2*std
    
    rank = 1-(distances.iloc[:,-1]/d0)
    
    ranking = pd.DataFrame({'Player':names,'Rank':rank})
    ranking.sort_values(by=['Rank'],inplace=True, ascending=False)
    return ranking
    

def Hellwig(data, startCol):
    """
    A function calculating Hellwig ranking.

    Parameters
    ----------
    data : pandas Data Frame
        A data frame with players names and statistics.
    startCol : integer
        Index of the first column containing statistics.

    Returns
    -------
    ranks : pandas Data Frame
        A data frame with Hellwig ranking.

    """
    names = list(data.iloc[:,1])
    dataStand = standarize(data.iloc[:,startCol:])
    distances = distToBest(dataStand)
    
    ranks = ranking(distances, names)
    return ranks


def TOPSIS(data, startCol, destimulants):
    """
    A function calculating TOPSIS ranking.

    Parameters
    ----------
    data : pandas Data Frame
        A data frame containing players names and statistics.
    startCol : integer
        Index of the first column containing statistics.
    destimulants : list
        A list containing columns with destimulants.

    Returns
    -------
    ranks : pandas Data Frame
        A data frame with TOPSIS ranking.

    """
    normalizedM = normalizedMatrix(data, startCol)
    stimulantsM = normalizedM.drop(destimulants, axis=1)
    destimulantsM = normalizedM[destimulants]
    
    sPlus = distToBests(stimulantsM, destimulantsM)
    sMinus = distToWorsts(stimulantsM, destimulantsM)
    
    pi = Pi(sPlus, sMinus)
    
    rank = rankingTOPSIS(pi, data['Player'])
    return rank

def normalizedMatrix(data, startCol):
    """
    A function normalizing data.

    Parameters
    ----------
    data : pandas Data Frame
    A data frame containing players names and statistics.
    startCol : integer
        Index of the first column containing statistics.

    Returns
    -------
    normalizedMatrix : pandas Data Frame
        A data frame containing normalized players statistics.

    """
    sumSquare = list((data.iloc[:,startCol:].pow(2).sum())**(1/2))
    normalizedMatrix = data.iloc[:,7:].div(sumSquare)
    
    return normalizedMatrix

def distToBests(normalizedStimulants, normalizedDestimulants):
    """
    A function calculating each player distance to the best statistics.

    Parameters
    ----------
    normalizedStimulants : pandas Data Frame
        A data frame containing normalized stimulants
    normalizedDestimulants : pandas Data Frame
        A data frame containing normalized destimulants

    Returns
    -------
    sPlus : list
        A list containing calculated S Plus value for each player.

    """
    maximum = list(normalizedStimulants.max())
    minimum = list(normalizedDestimulants.min())
    
    bests = maximum + minimum
    normalizedM = pd.concat([normalizedStimulants, normalizedDestimulants], axis=1)
    
    for i in range(normalizedM.shape[1]):
        normalizedM.iloc[:,i] = (normalizedM.iloc[:,i] - bests[i])**2
    
    sPlus = list(normalizedM.sum(axis=1)**(1/2))
    
    return sPlus

def distToWorsts(normalizedStimulants, normalizedDestimulants):
    """
    A function calculating each player distance to the worsts statistics.

    Parameters
    ----------
    normalizedStimulants : pandas Data Frame
        A data frame containing normalized stimulants
    normalizedDestimulants : pandas Data Frame
        A data frame containing normalized destimulants

    Returns
    -------
    sMinus : list
        A list containing calculated S Minus value for each player.

    """
    minimum = list(normalizedStimulants.min())
    maximum = list(normalizedDestimulants.max())
    
    bests = minimum + maximum
    normalizedM = pd.concat([normalizedStimulants, normalizedDestimulants], axis=1)
    
    for i in range(normalizedM.shape[1]):
        normalizedM.iloc[:,i] = (normalizedM.iloc[:,i] - bests[i])**2
    
    sMinus = list(normalizedM.sum(axis=1)**(1/2))
    
    return sMinus

def Pi(sPlus, sMinus):
    """
    A function calculating Pi value for each player

    Parameters
    ----------
    sPlus : list
        A list containing calculated S Plus value for each player.
    sMinus : list
        A list containing calculated S Minus value for each player.

    Returns
    -------
    Pi : list
        A list containing calculated pi value for each player.

    """
    suM = [i + j for i, j  in zip(sPlus, sMinus)]
    Pi = [i / j  for i,j in zip(sMinus, suM)]
    
    return Pi

def rankingTOPSIS(pi, players):
    """
    A function calculating TOPSIS ranking

    Parameters
    ----------
    pi : list
        A list containing calculated pi value for each player.
    players : list
        A list with players names.

    Returns
    -------
    ranking : pandas Data Frame
        A data frame with TOPSIS ranking.

    """
    ranking = pd.DataFrame({'Player': players, 'Rank':pi})
    ranking.sort_values(by=['Rank'],inplace=True, ascending=False)
    
    return ranking


    