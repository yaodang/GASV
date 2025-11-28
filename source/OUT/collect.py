# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 20:15:47 2022

@author: yaodang
"""


import numpy as np
import sys

sys.path.append('../COMMON/')
sys.path.append('../MOD/')

from MOD.mod_eop import *
from INIT.init import *
from COMMON.time_transfer import *


def collectResult(param, scanInfo, stationInfo, sourceInfo, staObs, eopApri, result):
    out = OUTRESULT()

    paramS = result.paramName.index('ut1')
    estP = np.where(result.paramNum[paramS:] > 0)
    out.estFlag[estP[0]] = 1
    
    for i in range(len(estP[0])):
        temp = sum(result.paramNum[0:paramS+estP[0][i]])
        out.estValue[estP[0][i]] = result.para[temp:temp+result.paramNum[estP[0][i]+paramS]]
        out.formalErr[estP[0][i]] = result.err[temp:temp+result.paramNum[estP[0][i]+paramS]]
    
    if param.Flags.pm[0] == 'YES' or param.Flags.ut1[0] == 'YES' or param.Flags.nut[0] == 'YES':
        if param.Flags.type == 'SEGMENT':
            eopindex = []
            mjd0 = np.floor(scanInfo.scanMJD[0])
            eopmMJD = mjd0 + np.array(result.paramMJD[paramS])/1440
        
        if param.Flags.type == 'POLY':
            eopmMJD = np.array([scanInfo.refMJD])
        
        meanEOP = interpEOP(eopApri, eopmMJD, param.Map.heopm, 0)
        
        
        temp = result.paramName.index('ut1')
        out.aprioriValue[temp-paramS] = meanEOP.UT1*1000  # ms
        out.mjd[temp-paramS] = eopmMJD
        
        temp = result.paramName.index('pmx')
        out.aprioriValue[temp-paramS] = meanEOP.XP*180*3600*1000/np.pi   # mas
        out.mjd[temp-paramS] = eopmMJD
        
        temp = result.paramName.index('pmy')
        out.aprioriValue[temp-paramS] = meanEOP.YP*180*3600*1000/np.pi   # mas
        out.mjd[temp-paramS] = eopmMJD
        
        temp = result.paramName.index('nutx')
        out.aprioriValue[temp-paramS] = meanEOP.DX*180*3600*1000/np.pi   # mas
        out.mjd[temp-paramS] = eopmMJD
        
        temp = result.paramName.index('nuty')
        out.aprioriValue[temp-paramS] = meanEOP.DY*180*3600*1000/np.pi   # mas
        out.mjd[temp-paramS] = eopmMJD  
            
    if param.Flags.pmr[0] == 'YES':
        xpr = getRate(eopApri.MJD, eopApri.XP, eopmMJD[0])
        xpr = xpr * 180/np.pi*3600*1E3  # rad/day to mas/day
        temp = result.paramName.index('pmxr')
        out.aprioriValue[temp-paramS] = np.array([xpr])
        out.mjd[temp-paramS] = eopmMJD
        
        ypr = getRate(eopApri.MJD, eopApri.YP, eopmMJD[0])
        ypr = ypr * 180/np.pi*3600*1E3  # rad/day to mas/day
        temp = result.paramName.index('pmyr')
        out.aprioriValue[temp-paramS] = np.array([ypr])
        out.mjd[temp-paramS] = eopmMJD
                
    if param.Flags.lod[0] == 'YES':
        lod = getRate(eopApri.MJD, eopApri.UT1, eopmMJD[0])
        lod = lod * 1E3                # s to ms
        temp = result.paramName.index('lod')
        out.aprioriValue[temp-paramS] = np.array([lod])
        out.mjd[temp-paramS] = eopmMJD
    
    xyzP = result.paramName.index('xyz') - paramS
    aprioriSta(param, scanInfo, stationInfo, staObs, result, param.Flags.xyz[0], xyzP, out)
    
    souP = result.paramName.index('sou') - paramS
    aprioriSou(param, scanInfo, sourceInfo, result, param.Flags.sou[0], souP, out)

    [year, mon, day, hour, minute, second] = mjd2ymdhms(scanInfo.scanMJD[0])
    
    return out

def aprioriSta(param, scanInfo, stationInfo, staObs, result, estflag, xyzP, out):
    '''
    Get the apriori station postion and obs time

    Parameters
    ----------
    scanInfo : the SCAN struct.
    stationInfo : The STATION struct.
    out : The struct of apriori and result.
    estflag: The flag of station position estimate.
    xyzP: the posit in out.

    Returns
    -------
    None.

    '''
    
    ns_code = scanInfo.stationCode
    nsCode = []
    meanTime = []
    staAprPosit = []
    for sta in range(len(scanInfo.stationAll)):
        if not scanInfo.stationAll[sta] in param.Flags.xyz:
            nsCode.append([ns_code[sta][3],ns_code[sta][2],ns_code[sta][1],ns_code[sta][5]])
            meanTime.append(staObs.meanTime[sta])
            staAprPosit.append(staObs.meanPosit[sta])
    out.nscode = nsCode
    
    out.aprioriValue[xyzP] = np.array(staAprPosit)
    out.mjd[xyzP] = meanTime
    
    if estflag == 'YES':
        resultxyzP = result.paramName.index('xyz')
        startP = sum(result.paramNum[:resultxyzP])
        xyzNum = result.paramNum[resultxyzP]
    
        # estValue = np.reshape(result.para[startP:startP+xyzNum],(3,len(nsCode)))
        # estErr = np.reshape(result.err[startP:startP+xyzNum],(3,len(nsCode)))
        
        estValue = np.reshape(result.para[startP:startP+xyzNum],(len(nsCode),3))
        estErr = np.reshape(result.err[startP:startP+xyzNum],(len(nsCode),3))
    
        out.estValue[xyzP] = estValue
        out.formalErr[xyzP] = estErr
    
        
def aprioriSou(param, scanInfo, sourceInfo, result, estFlag, souP, out):
    
    mMJD = scanInfo.scanMJD[0] + (scanInfo.scanMJD[-1]-scanInfo.scanMJD[0])/2
    my,mm,md,mhour,mminute,msecond = mjd2date(mMJD)
    mdoy = date2doy(my,mm,md)
    secm = int((mMJD-int(mMJD))*86400)
    
    sourceID = []
    for i in range(len(scanInfo.sourceAll)):
        if scanInfo.sourceAll[i] not in param.Flags.sou:
            sourceID.append(i)
    souApriPosit = []
    
    for i in range(len(sourceID)):
        name = scanInfo.sourceAll[sourceID[i]]
        if  name in sourceInfo.sourceName:
            index = sourceInfo.sourceName.index(name)
        else:
            index = sourceInfo.ivsName.index(name)
        
        souApriPosit.append([sourceInfo.rade[index][0], sourceInfo.rade[index][1]])
        out.souName.append(scanInfo.sourceAll[sourceID[i]])
        
    out.aprioriValue[souP] = np.array(souApriPosit)
    out.mjd[souP] = [my,mdoy,secm]
        
    if estFlag == 'YES':
        resultsouP = result.paramName.index('sou')
        startP = sum(result.paramNum[:resultsouP])
        souNum = result.paramNum[resultsouP]
        
        estValue = np.reshape(result.para[startP:startP+souNum],(len(sourceID),2))
        estErr = np.reshape(result.err[startP:startP+souNum],(len(sourceID),2))
    
        out.estValue[souP] = estValue
        out.formalErr[souP] = estErr
        
        
        
        
        
