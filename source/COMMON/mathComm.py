#!/usr/bin/env python3

import numpy as np
from itertools import *

def calculate_bl_lengths(stations):

    n = len(stations)
    if n < 2:
        return {}

    pairs = Cnm(range(n),2)
    baselines = {}

    for i,j in pairs:
        dx = stations[i][0] - stations[j][0]
        dy = stations[i][1] - stations[j][1]
        dz = stations[i][2] - stations[j][2]
        distance = np.sqrt(dx**2+dy**2+dz**2)

        baselines[(i,j)] = distance

    return baselines


def Cnm(inputList,num):
    '''
    Get the permutation combination result

    Parameters
    ----------
    inputList : list or array
        the number list or array will to combination.
    num : int
        the combination number.

    Returns
    -------
    TYPE
        Combination array.

    '''
    out = []
    for ii in combinations(inputList,num):
        out.append(list(ii))
        
    return np.array(out)

def calSSE(value):
    '''
    The sum of squares due to error.

    Parameters
    ----------
    value : array
        the value.

    Returns
    -------
    sse : float
        the SSE result.

    '''
    
    meanValue = np.mean(value)
    sse = np.sum((value-meanValue)**2)
    
    return sse

def std(value):
    '''
    The standard deviation.

    Parameters
    ----------
    value : array
        the value.

    Returns
    -------
    valueSTD : float
        the std result.

    '''
    
    meanValue = np.mean(value)
    valueSTD = np.sqrt(np.sum((value-meanValue)**2)/len(value))
    
    return valueSTD

def lagint4v(x,y,a):
    yout = np.zeros(len(a))
    for i in range(len(a)):
        
        out = 0
        temp = np.where(x <= a[i])
        indFirst = np.flip(temp[0])[4]
        temp = np.where(x >= a[i])
        indLast = temp[0][4]
        for m in range(indFirst, indLast+1):
            term = y[m]
            for j in range(indFirst, indLast+1):
                if m != j:
                    term = term*(a[i]-x[j])/(x[m]-x[j])
            out += term
        yout[i] = out
    return yout