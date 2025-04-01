#!/usr/bin/env python3

import sys,time
import numpy as np
from scipy import sparse

from INIT import *
from COMMON import *
from SOLVE.solve_constrain import *


def firstSolution(scanInfo, stationInfo, P_obs, oc_obs, staObs):
    """
    Remove the clock errors before the main estimation
    ---------------------
    input: 
        scanInfo        : the scan struct, see read_vgosDB define
        stationInfo     : the station struct, see read_station define
        P_obs           : the weight matrix of observations
        oc_obs          : the o-c vector of real observations
    output: 
        stationInfo     : STATION class
    ---------------------
    """
    ocObs = 1*oc_obs
    A_clkzwd,A_clk,firstStaClockNum = cbFun(scanInfo, staObs)
    
    Q_clk = np.linalg.inv(A_clkzwd.T@P_obs@A_clkzwd)
    b_clk = A_clkzwd.T@P_obs@ocObs
    
    # Q_clk = np.linalg.inv(np.dot(np.dot(A_clk.T, P_obs),A_clk))
    # b_clk = np.dot(np.dot(A_clk.T, P_obs),ocObs)
    
    clkzwd_val = np.dot(Q_clk,b_clk)    # [s]
    
    ocObs -= np.dot(A_clk,clkzwd_val[0:A_clk.shape[1]])
    # ocObs -= np.dot(A_clk, clkzwd_val)
    
    temp = clkzwd_val[0:A_clk.shape[1]]
    # temp = clkzwd_val
    clkPolyCoeff = np.reshape(temp, (3,int(len(temp)/3)))
    
    staClkPoly = []
    for i in range(len(firstStaClockNum)):
        staClkPoly.append([])
        
    sumNum = 0
    for i in range(len(firstStaClockNum)):
        num = firstStaClockNum[i]
        if num != 0:
            temp = []
            for j in range(num):
                tempOffset = clkPolyCoeff[0][sumNum+j]
                tempRate = clkPolyCoeff[1][sumNum+j]
                tempQuad = clkPolyCoeff[2][sumNum+j]
                temp.append(np.array([tempOffset,tempRate,tempQuad]))
                
            staClkPoly[i].extend(temp)
            sumNum += num

    scanInfo.staClkPoly = staClkPoly
    # scanInfo.firstStaClockNum = firstStaClockNum
    
    return ocObs
    
def cbFun(scanInfo, staObs):
    """
    Forming the clock break function and zwd offset
    ---------------------
    input: 
        scanInfo        : the scan struct, see read_vgosDB define
        staObs          : 
    output: 
        stationInfo     : STATION class
    ---------------------
    """
    
    firstStaClockNum = []
    clockBreak = []
    staNum = len(scanInfo.stationAll)
    obsNum = sum(scanInfo.scanObsNum)
    
    # station with clock break
    for i in range(staNum):
        if scanInfo.clkBrk.brkFlag[i] == 0:
            clockBreak.append([scanInfo.scanMJD[0],scanInfo.scanMJD[-1]])
            firstStaClockNum.append(1)
        else:
            temp = [scanInfo.scanMJD[0]]
            temp.extend(scanInfo.clkBrk.brkMJD[i])
            temp.append(scanInfo.scanMJD[-1])
            clockBreak.append(temp)
            firstStaClockNum.append(len(temp)-1)
            
        if (scanInfo.stationAll[i] == scanInfo.refclk) or (scanInfo.stationAll[i] in scanInfo.rmSta):
            firstStaClockNum[i] = 0
        
    c_offset = []
    c_rate = []
    c_quad = []
    
    for i in range(staNum):
        for j in range(len(clockBreak[i])-1):
            offset = np.zeros(obsNum).tolist()
            rate = np.zeros(obsNum).tolist()
            quad = np.zeros(obsNum).tolist()
            
            for k in range(len(staObs.mjd[i])):
                mjd = staObs.mjd[i][k]
                first = staObs.first[i][k]
                
                if mjd >= clockBreak[i][j] and mjd <= clockBreak[i][j+1]:
                    offset[staObs.oc_nob[i][k]] = first
                    rate[staObs.oc_nob[i][k]] = first * (mjd - clockBreak[i][j])
                    quad[staObs.oc_nob[i][k]] = first * (mjd - clockBreak[i][j])**2
                    
            if (scanInfo.stationAll[i] != scanInfo.refclk) and (not scanInfo.stationAll[i] in scanInfo.rmSta):
                c_offset.append(offset)
                c_rate.append(rate)
                c_quad.append(quad)
                
    zwd_offset = []
    for i in range(staNum):
        zwd = np.zeros(obsNum).tolist()
        for j in range(len(staObs.mjd[i])):
            zwd[staObs.oc_nob[i][j]] = staObs.first[i][j]*staObs.mf[i][j]
        
        if not scanInfo.stationAll[i] in scanInfo.rmSta:
            zwd_offset.append(zwd)
            
    A_clk = np.hstack((np.array(c_offset).T,np.array(c_rate).T,np.array(c_quad).T))
    A_clkzwd = np.hstack((np.array(c_offset).T,np.array(c_rate).T,\
                       np.array(c_quad).T, np.array(zwd_offset).T))
    
    return A_clkzwd,A_clk,firstStaClockNum

def LSQSolution(estPara, Ablk, Hblk, P_obs, oc, oc_obs, staNNTR, souNNR, nobs, result, bandIndex):
    
    A = sparse.vstack((Ablk,Hblk))
    N = A.T*P_obs*A
    
    Qxx = np.linalg.inv(N.toarray())

    # if staNNTR.nntrFlag or souNNR.nnrFlag:
        # Qxx = Qxx[0:A.shape[1],0:A.shape[1]]

    
    n = A.T*P_obs*oc
    x = np.dot(Qxx,n)
    
    v = A*x - oc
    v_real = v[:nobs]
    vTPv = np.dot(np.dot(v.T,P_obs.toarray()),v)
    vTPv_real = np.dot(np.dot(v_real.T,P_obs.toarray()[:nobs,:nobs]),v_real)
    mo = np.sqrt(vTPv/(len(oc_obs)+Hblk.shape[0]-len(x)))
    weightsum = sum(sum(P_obs.toarray()[:nobs,:nobs]))
    wrms = np.sqrt(vTPv_real/weightsum)/const.c*10**12  # [ps]

    print('    chi-square: %6.2f'%mo)
    print('    Main solve: The wrms of post-fit residuals is: %.3f ps'%(wrms))
    
    mi = mo*np.sqrt(np.diag(Qxx))
    tempA = A.toarray()
    tempP = P_obs.toarray()
    Qvv = np.linalg.inv(tempP[:nobs,:nobs])-tempA[:nobs,:]@Qxx@tempA[:nobs,:].T
    result.SReal[bandIndex] = np.sqrt(mo**2*np.diag(Qvv))
    
    # save the result
    result.paramName = estPara.param
    result.paramNum = estPara.num
    result.paramMJD = estPara.tmjd
    result.clkEstInfo = estPara.clkinfo
    result.zwdEstInfo = estPara.zwdinfo
    result.Pc = P_obs
    result.N = N
    result.Ablk = Ablk
    result.covMatrix = Qxx
    result.Hblk = Hblk
    result.V = v
    result.vTPv = vTPv
    result.dof = len(oc_obs)+Hblk.shape[0]-len(x)
    result.VReal[bandIndex] = v_real
    result.flag[bandIndex] = 1
    result.b = n
    result.nConst = Hblk.shape[0]
    result.nEst = N.shape[0]
    result.chis = mo
    result.wrms = wrms
    result.para = x
    result.err = mi
        
