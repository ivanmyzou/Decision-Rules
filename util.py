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

DR = ['maxiMax Value', 'maxiMin Value (Wald)', 'miniMax Regret (Savage)', 
      'Laplace\'s Principle of Insufficient Reason', 'Hurwicz (Mixed Optimistic-Pessimistic)',
      'Bayes (Expected Value)']

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

#%% 4 Laplace (insufficient reason)
def Laplace(DT): #equal likely events
    '''
    Input:
        - DT: decision table
    Output: list of Laplace actions
    '''
    row_sum = DT.sum(axis=1) #to be compared again
    value = max(row_sum)
    return np.where(row_sum == value)[0].tolist()

#%% 5 Hurwicz (with optimism index alpha)
def Hurwicz(DT, alpha):
    '''
    Input:
        - DT: decision table
        - alpha: optimism index (weight on row max), in [0,1]
    Output: list of Hurwicz actions
    '''
    row_max, row_min = DT.max(axis=1), DT.min(axis=1)
    row_weighted = alpha * row_max + (1 - alpha) * row_min
    value = max(row_weighted)
    return np.where(row_weighted == value)[0].tolist()

#%% 6 Bayes
def Bayes(DT, prob_w):
    '''
    Input:
        - DT: decision table
        - prob: probability weights
    Output: list of Bayes actions
    '''
    if any(w < 0 for w in prob_w):
        raise Exception('probability weights cannot be negative')
    if len(prob_w) != len(DT[0]):
        raise Exception('probability weights are not the same length as events')
    prob = np.array(prob_w) / sum(prob_w)
    expected_values = (prob * DT).sum(axis=1)
    value = max(expected_values)
    return np.where(expected_values == value)[0].tolist()    

#%%
def Table_display(T):
    '''
    Input:
        - T: decision table or regret table
    Output: display string of the table
    '''
    T_str_list = str(T).replace('[','').replace(']','').split('\n ')
    display_str = '\n'.join([row.replace(' ', ' '*5) for row in T_str_list])
    return display_str
    
#%%
def diag_intersect(vertices):
    vertices = np.vstack((vertices, vertices[0,]))
    intersects = []
    for i in range(1, vertices.shape[0]): #row
        A, B = vertices[i-1], vertices[i]
        if (A[1] >= A[0] and B[1] <= B[0]) or (A[1] <= A[0] and B[1] >= B[0]):
            # m A0 + (1 - m) B0 = m A1 + (1 - m) B1
            # m (A0 - A1 + B1 - B0) =  B1 - B0
            m = (B[1] - B[0]) / (A[0] - A[1] + B[1] - B[0])
            intersects.append(np.array([m * A[0] + (1 - m) * B[0], 
                                           m * A[1] + (1 - m) * B[1]]))
    return sorted(intersects, key = lambda x: tuple(x))
