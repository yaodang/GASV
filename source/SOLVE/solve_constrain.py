#!/usr/bin/env python3

import sys
import numpy as np
from scipy import sparse
from COMMON import *

def helmertTRF(flag_nnr, flag_nnt, staPosit):

    xyz = staPosit/np.linalg.norm(staPosit)
    # xyz = staPosit
    zeros = np.zeros((3,3))
    B = np.array([[1, 0, 0, 0, xyz[2], -xyz[1]],\
                      [0, 1, 0, -xyz[2], 0, xyz[0]],\
                      [0, 0, 1, xyz[1], -xyz[0], 0]])

    
    if flag_nnr and flag_nnt:
        H = B
    elif flag_nnr and not flag_nnt:
        H = np.hstack((zeros, B[:,3:]))
    elif not flag_nnr and flag_nnt:
        H = np.hstack((B[:,:3],zeros))
    elif not flag_nnr and not flag_nnt:
        H = np.zeros((3,6))
        
    return H

def helmertCRF(flag_nnr, ra, de):
    
    zeros = np.zeros((3,2))
    B = np.array([[-np.cos(de)*np.sin(de)*np.cos(ra),np.sin(ra)],\
                  [-np.cos(de)*np.sin(de)*np.sin(ra),-np.cos(ra)],\
                  [np.cos(de)**2, 0]])
        
    if flag_nnr:
        return B
    else:
        return zeros

def constrainTie(paramNum, Param, scanInfo, stationInfo, estParam):
    '''
    Design matrix, weight matrix and o-c vector for constraints for station tie

    Parameters
    ----------
    Param : TYPE
        DESCRIPTION.
    scanInfo : TYPE
        DESCRIPTION.
    stationInfo : TYPE
        DESCRIPTION.

    Returns
    -------
    Htie:
    Phtie:
    OCtie:

    '''
    Htie = []
    Phtie = []
    OCtie = []

    if Param.Const.tie != 'NO':
        tieBl = []
        
        for ista in range(len(scanInfo.stationAll)-1):
            if scanInfo.stationAll[ista] not in scanInfo.rmSta:
                for jsta in range(ista+1, len(scanInfo.stationAll)):
                    sta1 = stationInfo.stationName.index(scanInfo.stationAll[ista])
                    sta2 = stationInfo.stationName.index(scanInfo.stationAll[jsta])
    
                    blLength = np.sqrt((stationInfo.posit[sta1][0]-stationInfo.posit[sta2][0])**2+\
                                       (stationInfo.posit[sta1][1]-stationInfo.posit[sta2][1])**2+\
                                       (stationInfo.posit[sta1][2]-stationInfo.posit[sta2][2])**2)
                    if blLength <= 1000:
                        tieBl.append([stationInfo.stationName[sta1],stationInfo.stationName[sta2]])
        
        # zwd tie
        # const_tie = Param.Const.tie*1E-12*const.c*100 # [cm]
        const_tie = Param.Const.tie # [cm]

        for i in range(len(tieBl)):
            sta1P = estParam.zwdinfo[0].index(tieBl[i][0])
            sta2P = estParam.zwdinfo[0].index(tieBl[i][1])
            p1 = sum(estParam.zwdinfo[1][:sta1P]) #the posit start for sta1
            p2 = sum(estParam.zwdinfo[1][:sta2P]) #the posit start for sta2
            num1 = estParam.zwdinfo[1][sta1P]
            num2 = estParam.zwdinfo[1][sta2P]
            
            H = creatTieMatrix(estParam, Param, sta1P, sta2P, p1, p2, num1, num2, 'zwd', paramNum)
            
            if i == 0:
                Htie = H
                Phtie = sparse.eye(H.shape[0])*1/const_tie**2
            else:
                Htie = sparse.hstack((Htie, H))
                Phtie = sparse.block_diag((Phtie, sparse.eye(H.shape[0])*1/const_tie**2))
        if len(tieBl) != 0:        
            OCtie = np.zeros(Htie.shape[0])
          
    return Htie,Phtie,OCtie
        
def creatTieMatrix(estParam, Param, sta1P, sta2P,  p1, p2, num1, num2, paramName, paramNum):
    '''
    Create the H,Ph matrix for tie.

    Parameters
    ----------
    estParam : TYPE
        DESCRIPTION.
    Param : TYPE
        DESCRIPTION.
    sta1P : TYPE
        DESCRIPTION.
    sta2P : TYPE
        DESCRIPTION.
    p1 : TYPE
        DESCRIPTION.
    p2 : TYPE
        DESCRIPTION.
    num1 : TYPE
        DESCRIPTION.
    num2 : TYPE
        DESCRIPTION.
    paramName : TYPE
        DESCRIPTION.
    paramNum : TYPE
        DESCRIPTION.

    Returns
    -------
    Htie:
    Phtie:

    '''
    comTime = [[],[]]
    paramPosit = estParam.param.index(paramName)
    
    sta1Time = estParam.tmjd[paramPosit][p1:p1+num1]
    sta2Time = estParam.tmjd[paramPosit][p2:p2+num2]
    
    for itime in range(len(sta1Time)):
        if sta1Time[itime] in sta2Time:
            comTime[0].append(itime)
            comTime[1].append(sta2Time.index(sta1Time[itime]))
            
    
    paramSum = 0
    for i in range(paramPosit):
        paramSum += len(estParam.tmjd[i])
        
    H = np.zeros((len(comTime[0]),paramNum))
    for i in range(len(comTime[0])):
        colP1 = paramSum + p1 + comTime[0][i]
        colP2 = paramSum + p2 + comTime[1][i]
        
        H[i,colP1] =  1
        H[i,colP2] = -1
        
    
    return sparse.csr_matrix(H)
