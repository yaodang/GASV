#!/usr/bin/env python3

import numpy as np
import sys
from COMMON.mathComm import *
from COMMON.time_transfer import *
from INIT import *

def check(Param):
    estFlag = 0
    if Param.Flags.clk != 'NO':
        estFlag += 1
    if Param.Flags.blClk != 'NO':
        estFlag += 1
    if Param.Flags.zwd != 'NO':
        estFlag += 1
    if Param.Flags.gradient[0] != 'NO':
        estFlag += 1
    if Param.Flags.ut1[0] != 'NO':
        estFlag += 1
    if Param.Flags.pm[0] != 'NO':
        estFlag += 1
    if Param.Flags.nut[0] != 'NO':
        estFlag += 1
    if Param.Flags.xyz[0] != 'NO':
        estFlag += 1
    if Param.Flags.sou[0] != 'NO':
        estFlag += 1
    if Param.Flags.vel[0] != 'NO':
        estFlag += 1

    return estFlag   

def getOutFlag(staObs, scanInfo, stationInfo, Param, result, handOut, handFlag, bandIndex):
    
    rmPosit = []
    outlierP = (np.array([]),)
    if handFlag == 0:
        if Param.Data.outlier[0] == 'YES':# and len(result.VReal[bandIndex])>10:
            # rms = result.wrms
            # outlierP = np.where(abs(result.VReal[bandIndex])>int(Param.Data.outlier[1])*rms*1E-12*299792458*100)
            tempOut = []
            for ib in range(len(scanInfo.blResPosit)):
                blPosit = scanInfo.blResPosit[ib]
                if len(blPosit) > 8:
                    pbl = result.Pc.toarray()[blPosit,blPosit]
                    value = result.VReal[bandIndex][blPosit]
                    weightsum = np.sum(pbl)
                    vTPv = value**2@pbl
                    rms = np.sqrt(vTPv/weightsum)

                    # rms = np.sqrt(sum(value**2)/len(value))
                    temp = np.where(abs(value)>int(Param.Data.outlier[1])*rms)[0]
                    posit4rm = blPosit[temp].tolist()
                    
                    if len(posit4rm):
                        tempOut.extend(posit4rm)
                        
            outlierP = (np.array(tempOut),)
            # print(outlierP)
        else:
            outlierFlag = 0
            
    if len(handOut):
        if not np.any(outlierP[0]):
            outlierP = (np.array(handOut),)
        else:
            temp = outlierP[0].tolist()
            for num in handOut:
                if not num in temp:
                    temp.append(num)
            outlierP = (np.array(temp),)
            
    if len(outlierP[0]):
        print('\n    Main solve: remove the outlier......')
        outlierFlag = 1
                
        # get the outlier position in Obs2Scan
        rmPosit = refreshOutlier(staObs, scanInfo, stationInfo, outlierP)
    else:
        outlierFlag = 0
                    
    return outlierFlag, rmPosit

#def sou_ResInfo(scanInfo):


def sta_bl_sou_ResInfo(scanInfo):
    '''
    Get the residual of station, baseline and source information.

    Parameters
    ----------
    scanInfo : class
        the scan information.

    Returns
    -------
    baseline posit, baseline MJD, all baseline in session.

    '''
    
    useObsP = np.where(scanInfo.Obs2Scan != 0)
    Obs2Bl = scanInfo.Obs2Baseline[useObsP[0]]
    Obs2Sou = scanInfo.Obs2Source[useObsP[0]]
    MJD = scanInfo.Obs2MJD[useObsP[0]]
    
    scanInfo.staUsed = np.unique(Obs2Bl)
    scanInfo.souUsed = np.unique(Obs2Sou) - 1
    blUsed = np.unique(Obs2Bl, axis=0)
        
    #-------------------------- baseline information -------------------------#
    blResPosit = []
    blMJD = []
    
    for bl in blUsed:
        subBl = np.abs(Obs2Bl - bl)
        sumBl = np.sum(subBl,axis=1)
        
        blObs = np.where(sumBl==0)[0]
        blResPosit.append(blObs)
        blMJD.append(MJD[blObs])

    #--------------------------- station information -------------------------#
    staBlList = []
    for ista in scanInfo.staUsed:
        subSta = blUsed - ista
        staPosit = np.where(subSta[:,0]*subSta[:,1]==0)[0]
        if len(staPosit) == 0:
            print('    sta_bl_sou_ResInfo error: the station not match!')
            sys.exit()
        staBlList.append(staPosit)

    # --------------------------- source information -------------------------#
    souResPosit = []
    souMJD = []
    for isou in scanInfo.souUsed:
        souPosit = np.where(Obs2Sou == isou+1)
        if len(souPosit) == 0:
            print('    sta_bl_sou_ResInfo error: the source not match!')
            sys.exit()
        souResPosit.append(souPosit)
        souMJD.append(MJD[souPosit])

    
    scanInfo.blResPosit = blResPosit
    scanInfo.blUsed = blUsed.tolist()
    scanInfo.blMJD = blMJD
    scanInfo.staBlList = staBlList
    scanInfo.souResPosit = souResPosit
    scanInfo.souMJD = souMJD

def getBlUsedPosit(blList, reverseBl, blUsed):
    
    posit = []
    for i in reverseBl:
        temp = [blList[i][1], blList[i][0]]
        if temp in blUsed:
            posit.append(blUsed.index(temp))
        else:
            print('    sta_bl_ResInfo: the baseline sort is wrong!\n')
            sys.exit()
            
    return posit

def pick_staObs(scanInfo,stationInfo):
    """
    Prepare the observation parameter for each station
    ---------------------
    input: 
        scanInfo        : the scan struct, see read_vgosDB define
        stationInfo     : the station struct, see read_station define
    output: 
        staObs          : the sorted station observe
    ---------------------
    """
    
    staObs = STAOBS()
    for istat in range(len(stationInfo.stationName)):
        mjd = []
        ymdhms = []
        oc_nob = []
        first = []
        other = []
        mf = []
        mge = []
        mgn = []
        pcoor = []
        scan_bl = []
        
        num_obs = 0
        
        for iscan in range(len(scanInfo.scanMJD)):
            for iobs in range(scanInfo.scanObsNum[iscan]):
                sta1 = scanInfo.stationAll[scanInfo.scanBl[iscan][iobs][0]]
                sta2 = scanInfo.stationAll[scanInfo.scanBl[iscan][iobs][1]]
                
                if stationInfo.stationName[istat] == sta1 or stationInfo.stationName[istat] == sta2:
                    #num_sta_obs += 1
                    mjd.append(scanInfo.scanMJD[iscan])
                    ymdhms.append(scanInfo.scanTime[iscan])
                    oc_nob.append(num_obs)
                    scan_bl.append([iscan, scanInfo.scanBl[iscan][iobs][0],scanInfo.scanBl[iscan][iobs][1]])
                    
                if stationInfo.stationName[istat] == sta1:
                    first.append(-1)
                    other.append(sta2)
                    mf.append(scanInfo.scanMFW[iscan][scanInfo.scanStation[iscan].index(sta1)])
                    mge.append(scanInfo.scanMFGE[iscan][scanInfo.scanStation[iscan].index(sta1)])
                    mgn.append(scanInfo.scanMFGN[iscan][scanInfo.scanStation[iscan].index(sta1)])
                    #pcoor.append(-scanInfo.pxyz[iscan][iobs])
                    pcoor.append(-scanInfo.pxyz[num_obs])  #modify 2022.11.24
                    
                if stationInfo.stationName[istat] == sta2:
                    first.append(1)
                    other.append(sta1)
                    mf.append(scanInfo.scanMFW[iscan][scanInfo.scanStation[iscan].index(sta2)])
                    mge.append(scanInfo.scanMFGE[iscan][scanInfo.scanStation[iscan].index(sta2)])
                    mgn.append(scanInfo.scanMFGN[iscan][scanInfo.scanStation[iscan].index(sta2)])

                    #pcoor.append(scanInfo.pxyz[iscan][iobs])
                    pcoor.append(scanInfo.pxyz[num_obs])
                    
                num_obs = num_obs + 1
        
        if len(mjd):
            meanMJD = (mjd[0]+mjd[-1])/2.0
            mYear,mMon,mDay,mHour,mMinute,mSecond = mjd2date(meanMJD)
            mDoy = date2doy(mYear,mMon,mDay)
            mSec = mHour*3600+mMinute*60+np.floor(mSecond)
            mMJD = modjuldat(np.array([mYear]),np.array([mMon]),np.array([mDay]),mHour,mMinute,np.floor(mSecond))
            
            dDoy = date2doy(int(ymdhms[0][0]),int(ymdhms[0][1]),int(ymdhms[0][2]))
            sSec = ymdhms[0][3]*3600+ymdhms[0][4]*60+ymdhms[0][5]
            eDoy = date2doy(int(ymdhms[-1][0]),int(ymdhms[-1][1]),int(ymdhms[-1][2]))
            eSec = ymdhms[-1][3]*3600+ymdhms[-1][4]*60+ymdhms[-1][5]
            
            meanTime = [ymdhms[0][0], dDoy, sSec, ymdhms[-1][0], eDoy, eSec, mYear, mDoy, mSec, mMon,mDay,mHour,mMinute,mSecond,mMJD[0]]
    
            meanPosit = [stationInfo.posit[istat][0] + stationInfo.vel[istat][0]*(meanMJD-stationInfo.epoch[istat])/365.25,\
                          stationInfo.posit[istat][1] + stationInfo.vel[istat][1]*(meanMJD-stationInfo.epoch[istat])/365.25,\
                          stationInfo.posit[istat][2] + stationInfo.vel[istat][2]*(meanMJD-stationInfo.epoch[istat])/365.25]
        else:
            meanTime = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            meanPosit = [0,0,0]
            
        staObs.addParam(mjd,oc_nob,first,mf,mge,mgn,other,pcoor,scan_bl,meanTime,meanPosit)
    return staObs

def refreshOutlier(staObs, scanInfo, stationInfo, outlier):
    
    excludeObs = np.zeros(len(scanInfo.Obs2Scan), dtype=int)
    firstP = np.where(scanInfo.Obs2Scan != 0)
    oldList = sorted(list(set(scanInfo.Obs2Scan[firstP[0]])))
    rmP = firstP[0][outlier[0]]
    rmBl = scanInfo.Obs2Baseline[rmP]
            
    # refresh staObs
    for ista in range(len(staObs.mjd)):
        staRmP = []
        for i in range(len(rmBl)):
            if ista+1 in rmBl[i]:
                sta1 = rmBl[i][0] - 1
                sta2 = rmBl[i][1] - 1
                scanNum = len(list(set(scanInfo.Obs2Scan[firstP[0]][:outlier[0][i]+1])))
                
                staRmP.append(staObs.scanbl[ista].index([scanNum-1, sta1, sta2])) 
        staObs.mjd[ista] = np.delete(np.array(staObs.mjd[ista]),staRmP).tolist()
        staObs.first[ista] = np.delete(np.array(staObs.first[ista]),staRmP).tolist()
        staObs.mf[ista] = np.delete(np.array(staObs.mf[ista]),staRmP).tolist()
        staObs.mge[ista] = np.delete(np.array(staObs.mge[ista]),staRmP).tolist()
        staObs.mgn[ista] = np.delete(np.array(staObs.mgn[ista]),staRmP).tolist()
        staObs.other[ista] = np.delete(np.array(staObs.other[ista]),staRmP).tolist()
        staObs.pcoor[ista] = np.delete(np.array(staObs.pcoor[ista]),staRmP,axis=0).tolist()
  
    # refresh scanInfo
    excludeObs[rmP] += 1
    scanInfo.rmScanNum = []
    refreshScan(scanInfo, excludeObs)
    
    if len(scanInfo.rmScanNum):
        k = 0
        for i in range(len(scanInfo.rmScanNum)):
            scanInfo.scanMFW.pop(scanInfo.rmScanNum[i]-k)
            scanInfo.scanMFGE.pop(scanInfo.rmScanNum[i]-k)
            scanInfo.scanMFGN.pop(scanInfo.rmScanNum[i]-k)
            scanInfo.scanStation.pop(scanInfo.rmScanNum[i]-k)
            k += 1
    scanInfo.rmScanNum = []

    firstP = np.where(scanInfo.Obs2Scan != 0)
    newList = sorted(list(set(scanInfo.Obs2Scan[firstP[0]])))
    
    
    scanInfo.scanObsNum = []
    scanInfo.scanBl = []
    for iscan in range(len(scanInfo.scanMJD)):
        scan_posit = np.where(scanInfo.Obs2Scan==newList[iscan])  # +1: start from 1
        if len(scan_posit[0]):
            scanInfo.scanObsNum.append(len(scan_posit[0]))
            scanInfo.scanBl.append((scanInfo.Obs2Baseline-1)[scan_posit[0]].tolist())
    
    
    staObs.oc_nob = []
    staObs.scanbl = []
    for istat in range(len(stationInfo.stationName)):
        oc_nob = []
        scan_bl = []
        num_obs = 0
        
        for iscan in range(len(scanInfo.scanMJD)):
            for iobs in range(scanInfo.scanObsNum[iscan]):
                sta1 = scanInfo.stationAll[scanInfo.scanBl[iscan][iobs][0]]
                sta2 = scanInfo.stationAll[scanInfo.scanBl[iscan][iobs][1]]
                
                if stationInfo.stationName[istat] == sta1 or stationInfo.stationName[istat] == sta2:
                    oc_nob.append(num_obs)
                    scan_bl.append([iscan, scanInfo.scanBl[iscan][iobs][0],scanInfo.scanBl[iscan][iobs][1]])
                num_obs = num_obs + 1
        staObs.oc_nob.append(oc_nob)
        staObs.scanbl.append(scan_bl)
    
    for i in range(len(scanInfo.baseInfo[0])):
        scanInfo.oc_obs[i] = np.delete(np.array(scanInfo.oc_obs[i]), outlier[0]).tolist()
        scanInfo.pObs[i] = np.delete(np.array(scanInfo.pObs[i]), outlier[0]).tolist()
    scanInfo.pEOP = np.delete(scanInfo.pEOP, outlier[0], axis=0)
    scanInfo.pxyz = np.delete(scanInfo.pxyz, outlier[0], axis=0)
    scanInfo.psou = np.delete(scanInfo.psou, outlier[0], axis=0)
    
    return rmP