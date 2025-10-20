#!/usr/bin/env python3

import numpy as np
from scipy import sparse
from COMMON import *
import sys

def correctIono(scanInfo, staObs):
    '''
    Correct the ionosphere influence.

    Parameters
    ----------
    highFreqDelay : array
        the residual delay of high frequency, like X band.
    lowFreqDelay : array
        the residual delay of high frequency, like S band..
    effFreq : array
        the effect Frequency, 2*n, the first row is low freq.

    Returns
    -------
    None.

    '''
    print('    Correct ionosphere...\n')
    usedObsPosit = np.where(scanInfo.Obs2Scan !=0)
    usedBl = scanInfo.Obs2Baseline[usedObsPosit]
    index = [scanInfo.baseInfo[0].index('S'), scanInfo.baseInfo[0].index('X')]
    
    # lowFreqDelay = scanInfo.gd[index[0]][usedObsPosit] + scanInfo.ambigNum[index[0]][usedObsPosit]*scanInfo.baseInfo[2][index[0]][usedObsPosit]
    # highFreqDelay = scanInfo.gd[index[1]][usedObsPosit] + scanInfo.ambigNum[index[0]][usedObsPosit]*scanInfo.baseInfo[2][index[0]][usedObsPosit]
    
    lowFreqDelay = np.array(scanInfo.oc_obs[index[0]])
    highFreqDelay = np.array(scanInfo.oc_obs[index[1]])

    #print(scanInfo.effFreq)
    lowEffFreq = scanInfo.effFreq[index[0]][usedObsPosit]
    highEffFreq = scanInfo.effFreq[index[1]][usedObsPosit]
    
    coeff4GR = lowEffFreq**2/(highEffFreq**2-lowEffFreq**2)
    diff = highFreqDelay - lowFreqDelay
    corrIon = -coeff4GR*diff
    
    sigmas = np.array(scanInfo.pObs[index[0]])**2 - (0.005/const.c)**2
    sigmax = np.array(scanInfo.pObs[index[1]])**2 - (0.005/const.c)**2
    
    # sigmas = np.array(scanInfo.pObs[index[0]])**2
    # sigmax = np.array(scanInfo.pObs[index[1]])**2
    
    ionSigma = coeff4GR*np.sqrt(sigmax*(coeff4GR+2.0)/coeff4GR+sigmas)

    iondl = np.zeros(len(scanInfo.Obs2Scan))
    iondl[usedObsPosit] = corrIon

    iondlSigma = np.zeros(len(scanInfo.Obs2Scan))
    iondlSigma[usedObsPosit] = ionSigma
    
    scanInfo.iondl = iondl
    scanInfo.iondlSig = iondlSigma
    temp = np.sqrt(np.array(scanInfo.pObs[index[1]])**2 + ionSigma**2)
    scanInfo.pObs[index[1]] = temp.tolist()

def correctAmbiguty(staNum, scanInfo, residual, sigma, ambSize, staRefNum):
    '''
    Correct the ambiguity.

    Parameters
    ----------
    staNum : int
        the station number in session.
    scanInfo : struct
        the scan information
    residual : array
        the delay residual.
    sigma : array
        the group delay accuracy of earch observe.
    ambSize : float
        the ambiguity space (ns).
    staRefNum : int
        the index of station which is clock reference in all station.

    Returns
    -------
    ambNum : array
        the number of correct ambiguity .

    '''
    blMJD = scanInfo.blMJD
    blPosit = scanInfo.blResPosit
    blUsed = scanInfo.blUsed
    
    ambNum = np.zeros(len(scanInfo.Obs2Scan))
    useObsP = np.where(scanInfo.Obs2Scan != 0)
    MJD = scanInfo.Obs2MJD[useObsP[0]]
    Obs2Bl = scanInfo.Obs2Baseline[useObsP[0]]
    ambSizeUsed = ambSize[useObsP[0]]
    
    meanResValue = [[],[],[]] # first list is mean gd, second list is mean gdsig, third list is ambiguity size
    for ibl in range(len(blUsed)):
        blObs = blPosit[ibl]
        blRes = residual[blObs]/const.c
        blSig = sigma[blObs]
        blAmbSize = ambSizeUsed[blObs]
        
        resFirst = firstAmbClear(blRes, blSig, blAmbSize, ambNum, useObsP[0][blObs])
        
        temp = np.unique(blAmbSize)
        if len(temp) != 1:
            print('    Error: the baseline of %d-%d has many ambiguity.\n'%(blUsed[ibl][0], blUsed[ibl][1]))
            sys.exit()
        else:
            resSecond = secondAmbClear(resFirst, blMJD[ibl], ambNum, temp[0], useObsP[0][blObs])
            meanValueCalc(resSecond, blSig, temp[0], meanResValue)
            # meanValueCalc(resFirst, blSig, temp[0], meanResValue)
    if len(scanInfo.staUsed) >=3 :   
        thirdAmbClear(blUsed, meanResValue, blPosit, ambNum, useObsP[0], staRefNum)
    
    return ambNum

# def removeClkBreak(scanInfo, residual):
        
#     staNum = np.unique(scanInfo.blUsed)
    
#     bk = []
#     for ista in staNum:
#         subSta =  scanInfo.blUsed - ista
#         staPosit = np.where(subSta[:,0]*subSta[:,1]==0)[0]
        
#         temp = []
#         for ibl in staPosit:
#             resDiff = np.diff(residual[scanInfo.blResPosit[ibl]])
#             diffSTD = std(resDiff)
            
#             breakP = np.where(np.abs(resDiff) > diffSTD*10)[0]
#             if len(breakP) == 1 and breakP[0] > 20 and breakP[0] < len(resDiff)-20:
#                 temp.append((scanInfo.blMJD[ibl][breakP[0]]+scanInfo.blMJD[ibl][breakP[0]+1])/2)
#             else:
#                 temp.append(-1)
                
#         bk.append(temp)
        
#     print(bk)

def reweight(scanInfo, staObs, result, Pobserv):
    '''
    ! *   The way of calulation is the following:                            *
    ! *                                                                      *
    ! *            chisq_i -  [ n_i - summa ( a_i(T)*V*a_i * w_i**2 ) ]      *
    ! *      q_i = ---------------------------------------------------       *
    ! *            summa ( w_i**2 ) - summa ( a_i(T)*V*a_i * w_i**4 )        *
    ! *                                                                      *
    ! *                                                                      *
    ! *      Where                                                           *
    ! *        a) chisq_i -- chi-square over observations of the i-th        *
    ! *                      baseline;                                       *
    ! *        b) n_i     -- the number of obvservatoins at the i-th         *
    ! *                      baseline;                                       *
    ! *        c) a_i     -- i-th equation of conditions;                    *
    ! *        d) V       -- covariance matrix;                              *
    ! *        e) w_i     -- weight of the i-th observation;                 *
    '''
    
    blNum = len(scanInfo.blUsed)
    reweightInfo = {'Baseline':scanInfo.blUsed,'Value':np.zeros(blNum)}
    index = scanInfo.baseInfo[0].index('X')
    pObs = np.zeros(len(scanInfo.pObs[index]))
    
    for i in range(blNum):
        useBlP = scanInfo.blResPosit[i]
        blObsNum = len(useBlP)
        if blObsNum <= 1:
            continue
        
        chisqi = sum(result.VReal[index][useBlP]**2*Pobserv[useBlP,useBlP])
        
        sumw = sum(Pobserv[useBlP,useBlP])
        
        Ablk = result.Ablk.toarray()[useBlP,:]
        temp = Ablk @ result.covMatrix @ Ablk.T
        sumaw2 = np.sum(np.diag(temp)*Pobserv[useBlP,useBlP])
        sumaw4 = np.sum(np.diag(temp)*Pobserv[useBlP,useBlP]**2)
        
        qi = (chisqi-(blObsNum-sumaw2))/(sumw-sumaw4)
        if qi >= 0:
            reweightInfo['Value'][i] = np.sqrt(qi)/const.c
            pObs[useBlP] = np.sqrt(1 / Pobserv[useBlP, useBlP] + qi) / const.c
        else:
            reweightInfo['Value'][i] = -np.sqrt(-qi)/const.c
            for j in range(len(useBlP)):
                temp = 1 / Pobserv[useBlP[j], useBlP[j]] + qi
                if temp < 0:
                    pObs[useBlP[j]] = np.sqrt(1 / Pobserv[useBlP[j], useBlP[j]]) / const.c
                else:
                    pObs[useBlP[j]] = np.sqrt(1 / Pobserv[useBlP[j], useBlP[j]] + qi) / const.c


    scanInfo.reweightInfo = reweightInfo
    scanInfo.pObs[index] = pObs
            
def firstAmbClear(res, sigma, ambSpace, ambNum, blPosit):
    '''
    Remove the ambiguity reference nuSolve.

    Parameters
    ----------
    residual : array
        the baseline observe residual.
    sigma : array
        the sigma of baseline observe residual.
    ambSpace : float
        the ambiguity space.
    blPosit : array
        the baseline observe positon in Obs2Scan.
    ambNum : array
        the correct ambiguity number of all observe.

    Returns
    -------
    Update ambNum.

    '''
    residual = res + 0
    nsigma = sigma + 10E-12
    numUp = np.where(residual > 0.0)
    numDown = np.where(residual < 0.0)
    
    if len(numUp[0]) > len(numDown[0]):
        n = numUp[0]
    else:
        n = numDown[0]
    
    if len(n) > 4:
        SA = np.sum(1/nsigma[n]**2)
        SB = np.sum(residual[n]/nsigma[n]**2)
        
        meanRes = SB/SA
        num = np.round((residual-meanRes)/ambSpace)
        residual = residual - num*ambSpace
        ambNum[blPosit] -= num
    else:
        num = np.zeros(len(residual))
        for i in range(len(residual)-1):
            num[i+1] = np.round((residual[i+1]-residual[i])/ambSpace[i+1])
            residual[i+1] -= num[i+1]*ambSpace[i+1]
        ambNum[blPosit] -= num
            
    return residual

def secondAmbClear(res, MJD, ambNum, ambSpace, blPosit):
    '''
    Check break point and clear the break ambiguity.

    Parameters
    ----------
    res : array
        the baseline observe residual.
    MJD : array
        the baseline obseve Modified Julian Date.
    ambNum : array
        the correct ambiguity number of all observe.
    ambSpace : array
        the ambiguty size.
    blPosit : array
        the baseline observe positon in Obs2Scan.

    Returns
    -------


    '''
    residual = res + 0
    obsNum = len(residual)
    
    if obsNum > 20:
        diff = np.diff(residual)
        mse = np.sqrt(calSSE(diff)/len(diff))
        
        breakP = np.where(np.abs(diff) > 3*mse)[0]
        if len(breakP) == 1:
            lenBefore = breakP[0] + 1
            lenAfter = obsNum - lenBefore
            
            if lenBefore > 2 and lenAfter > 2:
                polyBefore = np.linspace(0, breakP[0], lenBefore, dtype=int)
                polyAfter = np.linspace(breakP[0]+1, obsNum-1, lenAfter, dtype=int)
                
                # if the point is the false break point 
                valueBefore = fitting(MJD[polyBefore], residual[polyBefore], MJD[breakP[0]+1], 1)
                valueAfter = fitting(MJD[polyAfter], residual[polyAfter], MJD[breakP[0]], 1)
                
                if abs(residual[breakP[0]]-valueAfter) < 0.5*ambSpace or abs(residual[breakP[0]+1]-valueBefore) < 0.5*ambSpace:
                    return residual
                
                if lenBefore >= lenAfter:
                    polyIndex = polyBefore
                else:
                    polyIndex = polyAfter
                    
                xMJD = MJD[polyIndex]
                yRes = residual[polyIndex]
                nyRes = fitting(xMJD, yRes, MJD, 1)
                
                num = np.round((residual-nyRes)/ambSpace)
                residual = residual - num*ambSpace
                ambNum[blPosit] -= num
                
    return residual
    
def thirdAmbClear(blUsed, mValue, blPosit, ambNum, useObsP, staRefNum):
    '''
    Correct the baseline triangles misclosure. Reference the nuSolve.

    '''
    
    blNum = len(blUsed)
    staJoin = np.unique(blUsed)
    triangleList = Cnm(staJoin, 3)
    
    A = []
    Ptri = []
    oc = []
    for itr in range(len(triangleList)):
        bl1 = [triangleList[itr,0],triangleList[itr,1]]
        bl2 = [triangleList[itr,0],triangleList[itr,2]]
        bl3 = [triangleList[itr,1],triangleList[itr,2]]
    
        ibl = [-1,-1,-1]
        xbl = np.zeros(3, dtype=int)
        ires = np.zeros((3,3)) # first row is residual, second row is sigma, third is ambiguity size
        
        findAndSetBl(blUsed, bl1, 0, ibl, xbl, mValue, ires)
        findAndSetBl(blUsed, bl2, 1, ibl, xbl, mValue, ires)
        findAndSetBl(blUsed, bl3, 2, ibl, xbl, mValue, ires)
        
        if sum(ibl) == 3:
            tempA = np.zeros(blNum)
            tempSig = np.sqrt(sum(ires[1,:]**2))
            tempoc = ires[0,1]-ires[0,0]-ires[0,2]
            # tempA[xbl] = [-ires[2,0],ires[2,1],-ires[2,2]]
            tempA[xbl] = [ires[2,0],-ires[2,1],ires[2,2]]
            
            A.append(tempA)
            Ptri.append(tempSig)
            oc.append(tempoc)
            
    # constrain for reference station
    subBlRef = np.array(blUsed) - (staRefNum+1)
    staRefPosit = np.where(subBlRef[:,0]*subBlRef[:,1]==0)[0]
    lenStaRef = len(staRefPosit)
    
    och = np.zeros(lenStaRef)
    sigmaPh = 1/(1E-13**2)
    Ph = np.ones(lenStaRef)*sigmaPh
    PAll = np.hstack((Ptri, Ph))
    H = np.zeros((lenStaRef, blNum))
    for i in range(lenStaRef):
        H[i, staRefPosit[i]] = 1.0
                
    sparseA = sparse.vstack((A,H))
    sparseP = sparse.csr_matrix(np.diag(PAll))
    sparseOC = sparse.hstack((oc,och))
    
    N = sparseA.T*sparseP*sparseA
    Qxx = np.linalg.inv(N.toarray())
    b = sparseA.T*sparseP*sparseOC.T
    
    paramOffset = Qxx@b
    
    num = np.round(paramOffset.reshape([blNum,]))
    clearP = np.where(np.abs(num)>=1)[0]
    
    for ic in clearP:
        ambNum[useObsP[blPosit[ic]]] += num[ic]

def fitting(x, y, nx, order):
    '''
    Polynomial fitting.

    '''
    
    polynomial = np.polyfit(x, y, order)
    polyCoef = np.poly1d(polynomial)
    ny = polyCoef(nx)
    
    return ny
    
def meanValueCalc(res, sigma, ambSize, mValue):
    '''
    Get the mean value of baseline.

    '''
    
    nsigma = sigma + 5E-12
    residual = res + 0
    SA = np.sum(1/nsigma**2)
    SB = np.sum(residual/nsigma**2)
    SC = np.sum(residual**2/nsigma**2)
    
    meanRes = SB/SA
    meanResSig = (SC-SB)/SA
    
    mValue[0].append(meanRes)
    mValue[1].append(meanResSig)
    mValue[2].append(ambSize)
    
def findAndSetBl(blUsed, bl, num, ibl, xbl, mValue, ires):
    '''
    Find the triangles baseline and set the its value.

    '''
    
    signFlag = 0
    if bl in blUsed:
        signFlag = 1
        tempbl = bl
    elif [bl[1],bl[0]] in blUsed:
        signFlag = -1
        tempbl = [bl[1],bl[0]]
        
    if signFlag != 0:
        ibl[num] = 1
        xbl[num] = blUsed.index(tempbl)
        ires[0,num] = signFlag*mValue[0][xbl[num]]
        ires[1,num] = mValue[1][xbl[num]]
        ires[2,num] = signFlag*mValue[2][xbl[num]]