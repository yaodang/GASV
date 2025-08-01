#!/usr/bin/env python3

import numpy as np
from scipy import sparse

def reduceSNX(result, snxParam):
    '''
    Reduce the clock and troposphere from normal equation
    
    
    x1: globally estimated parameter
    x2: reduced patameter
    
    N11*x1 + N12*x2 = b1
    N21*x1 + N22*x2 = b2
    
    can be reduce to
    Nreduce = N11 - N12*N22-1*N21
    breduce = b1 - N12*N22-1*b2

    Parameters
    ----------
    result : the struct
        the estimate result.

    Returns
    -------
    The reduce matrix.

    '''
    redcol,estcol = getCol(result, snxParam)
    
    if len(estcol) != 0:
        H = result.Hblk.toarray()
        H[:,estcol] = 0
        
        A = sparse.vstack((result.Ablk,sparse.csr_matrix(H)))
        N = A.T*result.Pc*A
        N = N.toarray()
        
        N11 = N[estcol[0]:estcol[-1]+1,estcol[0]:estcol[-1]+1]
        N12 = N[estcol[0]:estcol[-1]+1,redcol[0]:redcol[-1]+1]
        N21 = N[redcol[0]:redcol[-1]+1,estcol[0]:estcol[-1]+1]
        N22 = N[redcol[0]:redcol[-1]+1,redcol[0]:redcol[-1]+1]
        
        b1 = result.b[estcol]
        b2 = result.b[redcol]
        
        Nsnx = N11 - np.dot(np.dot(N12,np.linalg.inv(N22)),N21)
        bsnx = b1 - np.dot(np.dot(N12,np.linalg.inv(N22)),b2)
        
        result.Nsnx = Nsnx
        result.bsnx = bsnx

        #ytpy = result.o_creal.T@result.preal@result.o_creal
        #ytpy - b2.T@np.linalg.inv(N22)@b2
    
def getCol(result, snxParam):
    '''
    Get the estimate parameter column which will be writed in sinex.

    Parameters
    ----------
    result : the struct
        the estimate result.

    Returns
    -------
    redcol : matrix
        reduce matrix(clock, troposphere).
    estCol : matrix
        estimate matrix(EOP, station, source).

    '''
    
    posit = np.zeros(sum(result.paramNum),dtype=int)
    if len(snxParam) == 2:
        snxParam.extend(['eop','xyz','sou'])
    
    for param in snxParam[2:]:
        if param == 'zwd':
            index = result.paramName.index('zwd')
            startPosit = sum(result.paramNum[0:index])
            stopPosit = startPosit + result.paramNum[index]
        elif param == 'gradient':
            # contain the ngr and egr
            index = result.paramName.index('ngr')
            startPosit = sum(result.paramNum[0:index])
            stopPosit = startPosit + sum(result.paramNum[index:index+2])    
        elif param == 'eop':
            # contain the xpo,ypo,ut1,nutation,lod,xpo rate, ypo rate and lod
            index = result.paramName.index('ut1')
            startPosit = sum(result.paramNum[0:index])
            stopPosit = startPosit + sum(result.paramNum[index:index+8])
        elif param == 'xyz':
            index = result.paramName.index('xyz')
            startPosit = sum(result.paramNum[0:index])
            stopPosit = startPosit + result.paramNum[index]
        elif param == 'sou':
            index = result.paramName.index('sou')
            startPosit = sum(result.paramNum[0:index])
            stopPosit = startPosit + result.paramNum[index]
        
        posit[startPosit:stopPosit] = 1
        
    reduceCol = np.where(posit==0)[0]
    estCol = np.where(posit==1)[0]
                
    return reduceCol, estCol