#!/usr/bin/env python3

import sys
import numpy as np
from scipy import sparse
from COMMON.time_transfer import modjuldatNew

def matrixInit(Param,sitNum,souNum):
    estNum = 0
    if Param.Global.station[0] == 'YES':
        estNum += sitNum*3
    if Param.Flags.vel[0] == 'YES':
        estNum += sitNum*3
    if Param.Global.source[0] == 'YES':
        estNum += souNum*2
    
    N = np.zeros((estNum,estNum))
    b = np.zeros((estNum,1))
    
    return N,b

def matrixRebuild(Nmatrix,bVector,posit):
    '''
    put the global parameter to first few columns

    Parameters
    ----------
    Nmatrix : array
        normal matrix.
    bVector : array
        normal matrix vector.
    posit : list
        the global parameter posit in session.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    positDiff = np.diff(posit)
    findOne = np.where(positDiff==1)[0]
    if posit[0] == 0 and (len(findOne) == len(posit)-1):
        return Nmatrix,bVector.reshape(len(bVector),1)
    else:
        num = Nmatrix.shape[0]
        index = np.linspace(0, num-1, num, dtype=int)
        
        localPosit = []
        for i in index:
            if i not in posit:
                localPosit.append(i)
                
        globalColumn = Nmatrix[:,posit]
        tempNMatrix = np.hstack((globalColumn, Nmatrix[:,localPosit]))
        globalRow = tempNMatrix[posit,:]
        NmatrixNew = np.vstack((globalRow, tempNMatrix[localPosit,:]))
        
        bVectorColumn = bVector.reshape(len(bVector),1)
        bRow = bVectorColumn[posit,:]
        bVectorNew = np.vstack((bRow, bVectorColumn[localPosit,:]))
            
        return NmatrixNew, bVectorNew

def matrixReduce(Nmatrix,Nvertor,posit):
    '''
    reduce the matrix for global parameter

    Parameters
    ----------
    Nmatrix : array
        normal matrix.
    Nvertor : array
        normal matrix vector.
    posit : int
        the number of global parameter cloumn.

    Returns
    -------
    Nr : TYPE
        reduced normal matrix.
    br : TYPE
        reduced normal matrix vector.

    '''
    
    N11 = Nmatrix[:posit,:posit]
    N12 = Nmatrix[:posit,posit:]
    N21 = Nmatrix[posit:,:posit]
    N22 = Nmatrix[posit:,posit:]
    
    b1 = Nvertor[:posit]
    b2 = Nvertor[posit:]
    
    Nr = N11 - N12 @ np.linalg.inv(N22) @ N21
    br = b1 - N12 @ np.linalg.inv(N22) @ b2
    vtpv_reduce = b2.T @ np.linalg.inv(N22) @ b2
    
    return Nr,br,vtpv_reduce,len(b2)


def matrixExtendNew(Napri, bapri, Param, sitPositInGlob, sitVelInGlob, numAll, numAdd, sitEstNum):
    '''
    create the global matrix for all station and source.

    Parameters
    ----------
    Napri : array
        normal matrix to Add.
    bapri : array
        normal matrix vertor to add.
    Param : class
        the setup in cnt file .
    flag : int
        1-station part;
        2-source part;
        3-eop part;
        4-other part.
    addNum : int
        DESCRIPTION.
    paramNum : int
        the station or source or eop or other number.

    Returns
    -------
    None.

    '''
    '''
    estNum = 0
    if Param.Global.station[0] == 'YES':
        estNum += numAll[0] * 3
    if Param.Flags.vel[0] == 'YES':
        estNum += numAll[0] * 3
    '''
    estNum = sum(sitEstNum)*3
    if Param.Global.source[0] == 'YES':
        estNum += numAll[1] * 2

    N = np.zeros((estNum, estNum))
    b = np.zeros((estNum, 1))

    posit = numAll - numAdd

    positInGlob = []

    #sitAllEstNum = len(sitPositInGlob) + len(sitVelInGlob)
    sitAllEstNum = sum(sitEstNum)*3
    if Param.Flags.vel[0] == 'YES':
        psit = [sitPositInGlob[i] for i in range(posit[0]*3)]
        vsit = [sitVelInGlob[i] for i in range(posit[0]*3)]

        temp = []
        for value in vsit:
            if value not in temp:
                temp.append(value)
        psit.extend(temp)
        #psit.extend(list(set(vsit)))
        positInGlob.extend(psit)

        for i in range(posit[1]):
            positInGlob.extend([sitAllEstNum + 2 * i, sitAllEstNum + 2 * i + 1])
    else:
        positInGlob.extend([sitPositInGlob[i] for i in range(posit[0]*3)])

        for i in range(posit[1]):
            positInGlob.extend([sitAllEstNum + 2 * i, sitAllEstNum + 2 * i + 1])

    if len(positInGlob) == 0:
        print('Error: no add parameter')
        sys.exit()
    else:
        matrixStack(N, Napri, b, bapri, positInGlob)
        #checkMatrix()
        return N, b

def matrixExtend(Napri,bapri,Param,numAll,numAdd):
    '''
    

    Parameters
    ----------
    NAdd : array
        normal matrix to Add.
    bAdd : array
        normal matrix vertor to add.
    Param : class
        the setup in cnt file .
    flag : int
        1-station part;
        2-source part;
        3-eop part;
        4-other part.
    addNum : int
        DESCRIPTION.
    paramNum : int
        the station or source or eop or other number.

    Returns
    -------
    None.

    '''
    
    estNum = 0
    if Param.Global.station[0] == 'YES':
        estNum += numAll[0]*3
    if Param.Flags.vel[0] == 'YES':
        estNum += numAll[0]*3
    if Param.Global.source[0] == 'YES':
        estNum += numAll[1]*2        
    
    N = np.zeros((estNum,estNum))
    b = np.zeros((estNum,1))
    
    posit = numAll - numAdd 
    
    positInGlob = []
    # if Param.Flags.vel[0] == 'YES':
    #     if numAdd[0] != 0:
    #         temp1 = []
    #         temp2 = []
    #         for i in range(posit[0]):
    #             temp1.extend([i*3,i*3+1,i*3+2])
    #             temp2.extend([numAll[0]*3+i*3,numAll[0]*3+i*3+1,numAll[0]*3+i*3+2])
    #             # positInGlob.extend([3*i,3*i+1,3*i+2,\
    #             #                     numAll[0]*3+3*i,numAll[0]*3+3*i+1,numAll[0]*3+3*i+2])
    #         temp1.extend(temp2)
    #         positInGlob.extend(temp1)
    #     else:
    #         if numAdd[1] != 0:
    #             for i in range(posit[1]):
    #                 positInGlob.extend([numAll[0]*6+2*i,numAll[0]*6+2*i+1])
    # else:
    #     if numAdd[0] != 0:
    #         for i in range(posit[0]):
    #             positInGlob.extend([3*i,3*i+1,3*i+2])
    #     else:
    #         if numAdd[1] != 0:
    #             for i in range(posit[1]):
    #                 positInGlob.extend([numAll[0]*3+2*i,numAll[0]*3+2*i+1])
    if Param.Flags.vel[0] == 'YES':
        temp1 = []
        temp2 = []
        for i in range(posit[0]):
            temp1.extend([i*3,i*3+1,i*3+2])
            temp2.extend([numAll[0]*3+i*3,numAll[0]*3+i*3+1,numAll[0]*3+i*3+2])

        temp1.extend(temp2)
        positInGlob.extend(temp1)

        for i in range(posit[1]):
            positInGlob.extend([numAll[0]*6+2*i,numAll[0]*6+2*i+1])
    else:
        for i in range(posit[0]):
            positInGlob.extend([3*i,3*i+1,3*i+2])

        for i in range(posit[1]):
            positInGlob.extend([numAll[0]*3+2*i,numAll[0]*3+2*i+1])
                    
    if len(positInGlob) == 0:
        print('Error: no add parameter')
        sys.exit()
    else:
        matrixStack(N,Napri,b,bapri,positInGlob)
        return N,b

def matrixStack(N,NAdd,b,bAdd,paramIndex):
    '''
    Normal matrix stacking.

    Parameters
    ----------
    N : array
        final normal matrix
    NAdd : array
        session normal matrix to add
    b : array
        final normal vector
    bAdd : array
        session normal vector to add
    paramIndex : array
        the global parameter of session position in global estmate parameter

    '''
    for i in range(len(paramIndex)):
        b[paramIndex[i]] += bAdd[i]
        N[paramIndex[i],paramIndex] += NAdd[i,:]

def matrixTransfer(Ns,bs,sitObsEpoch,checkNum,Param,flag):
    
    # velocity
    if Param.Flags.vel[0] == 'YES':
        if len(Param.Flags.xyz) == 3:
            temp = list(filter(None,Param.Flags.xyz[2].split(".")))
            refMJD = modjuldatNew(int(temp[0]),int(temp[1]),int(temp[2]))
        else:
            refMJD = modjuldatNew(2015,1,1)
              
        NNew,bNew = matrixLinear(Ns,bs,sitObsEpoch,refMJD,checkNum,Param,flag)
    else:
        NNew = Ns
        bNew = bs
    
    return NNew,bNew
    # station non linear
    

def matrixLinear(N,b,sitObsEpoch,refMJD,checkNum,Param,flag):
    '''
    Transfer the station offset to station offset and station velocity refer to base frame.

    Parameters
    ----------
    Nold : array
        DESCRIPTION.
    bold : TYPE
        DESCRIPTION.
    sitObsEpoch : TYPE
        DESCRIPTION.
    refMJD : TYPE
        DESCRIPTION.
    Param : TYPE
        DESCRIPTION.

    Returns
    -------
    Nnew2 : TYPE
        DESCRIPTION.
    bnew : TYPE
        DESCRIPTION.

    '''
    unitMatrix = np.eye(3)
    sortPosit = []
    for i in range(len(sitObsEpoch)):
        TT0 = (sitObsEpoch[i] - refMJD)/365.25
        tempMatrix = np.hstack((unitMatrix, unitMatrix*TT0))
        sortPosit.extend([6*i,6*i+1,6*i+2])
        
        if i == 0:
            TMatrix = tempMatrix
        else:
            TMatrix = sparse.block_diag((TMatrix, tempMatrix))
    
    if checkNum[1] != 0:
        TMatrix = sparse.block_diag((TMatrix, np.eye(checkNum[1])))
    
    Nnew1 = TMatrix.T@N@TMatrix
    bnew1 = TMatrix.T@b
    
    if flag == 0:
        Nnew2,bnew2 = matrixRebuild(Nnew1,bnew1,sortPosit)
        return Nnew2,bnew2
    else:
        return Nnew1,bnew1
    
    
# ab = np.array([[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]])
# NmatrixNew = matrixRebuild(ab,[1])