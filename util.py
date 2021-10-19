#Utility

import numpy as np

def Text_to_Matrix(Text):
    '''
    Input:
        - Text: decision table obtained from the text widget
    Output: Numpy array of the decision table matrix
    '''
    L = [[float(n) for n in row.split()
          ] for row in Text.strip().split('\n')
         ]
    if len(set([len(row) for row in L])) > 1:
        raise Exception('inconsistent numbers of elements in rows')
    return np.array(L) #decision table as numpy array

def Regret(DT):
    '''
    Input:
        - DT: decision table
    Output: Numpy array of the regret table matrix
    '''
    col_max = DT.max(axis=0)
    return col_max - DT

#%% 1 maxiMax Value
def maxi_Max(DT):
    '''
    Input:
        - DT: decision table
    Output: list of maxiMax value actions
    '''
    row_max = DT.max(axis=1) #to be compared again
    value = max(row_max)
    return np.where(row_max == value)[0].tolist()

#%% 2 maxiMin Value
def maxi_Min(DT):
    '''
    Input:
        - DT: decision table
    Output: list of maxiMin value actions
    '''
    row_min = DT.min(axis=1) #to be compared again
    value = max(row_min)
    return np.where(row_min == value)[0].tolist()

#%% 3 miniMax Regret
def mini_Max(RT):
    '''
    Input:
        - RT: regret table
    Output: list of miniMax regret actions
    '''
    row_max = RT.max(axis=1) #to be compared again
    value = min(row_max)
    return np.where(row_max == value)[0].tolist()



