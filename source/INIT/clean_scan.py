#!/usr/bin/env python3

import numpy as np
import sys


def updateScanInfo(scanInfo, Param, wrpInfo, sessionNum):
    
    excludeObs = cleanDelayFlag(scanInfo)
    # if wrpInfo.Flag < 2:
    #     excludeObs += cleanQcode(scanInfo, Param.Setup.qcodeLim)
    if wrpInfo.Flag >= 2:
        excludeObs += cleanIonFlag(scanInfo)
    
    if Param.Arcs.version[sessionNum] > 0:
        excludeObs += cleanQcode(scanInfo, Param.Setup.qcodeLim)
    # excludeObs = np.zeros(len(scanInfo.Obs2Scan))

    # exclude station 
    rmSta = analysisList(Param.Data.sta, scanInfo.stationAll, 0)
    if rmSta:
        excludeObs += cleanSta(rmSta, scanInfo)
              
    # exclude source
    #rmSou = analysisList(Param.Data.sou, scanInfo.sourceAll, 0)
    #if rmSou:
    #    excludeObs += cleanSou(rmSou, scanInfo)
        
    noEstSta = analysisList(Param.Flags.xyz, scanInfo.stationAll, 1, Param, rmSta)
    # noEstSou = analysisList(Param.Flags.sou, scanInfo.sourceAll, 2, Param, rmSou)
    refreshScan(scanInfo, excludeObs)

    # reference clock set
    if len(scanInfo.refclk) != 8:
        updete_refClk(scanInfo)
    if scanInfo.refclk in scanInfo.rmSta:
        for ista in scanInfo.stationAll:
            if ista not in scanInfo.rmSta:
                scanInfo.refclk = ista

    updateStaEstimate(scanInfo.Scan2Station, scanInfo.stationAll, Param.Flags.xyz)
    updateSouEstimate(scanInfo, Param.Flags.sou)
    
def analysisList(targetMode, targetList, flag, *args):
    if len(args) == 2:
        Param = args[0]
        rm = args[1]
    
    rmList = []
    if len(targetMode) >=3 and 'EXCEPT' in targetMode:
        if targetMode[0] == 'YES':
            rmList = targetMode[2:]
        elif targetMode[0] == 'NO':
            useSta = targetMode[2:]

            for target in targetList:
                if not target.strip() in useSta:
                    rmList.append(target)
    elif len(targetMode) == 1 and targetMode[0] == 'NO':
        return []
            
    if flag != 0:
        for ik in rm:
            #if ik not in rmList:
            #    rmList.append(ik)
            ik_8str = ik + '        '[:8-len(ik)]
            if ik in targetList:
                rmList.append(ik)
        
        if len(rmList) == len(targetList):
            if flag == 1:
                Param.Flags.xyz = ['NO']
            elif flag == 2:
                Param.Flags.sou = ['NO']
                
        elif len(rmList):
            if flag == 1:
                Param.Flags.xyz = ['YES', 'EXCEPT'] + rmList
            elif flag == 2:
                Param.Flags.sou = ['YES', 'EXCEPT'] + rmList
            
    return rmList

def refreshScan(scanInfo, excludeObs):
    # refresh the scan struct
    noneZeroP = np.where(scanInfo.Obs2Scan != 0)
    zeroPosit = np.where(scanInfo.Obs2Scan == 0)
    newScanNum = sorted(list(set(scanInfo.Obs2Scan[noneZeroP[0]])))
    
    # ----- the station observe number in each scan --------
    staCount = []
    for i in range(len(newScanNum)):
        posit = np.where(scanInfo.Obs2Scan==newScanNum[i])
        
        count = np.zeros(len(scanInfo.stationAll), dtype=int)
        for j in posit[0]:
            if not j in zeroPosit[0]:
                staPosit = scanInfo.Obs2Baseline[j]-1
                count[staPosit] += 1
        staCount.append(count)
    # ------------------------------------------------------
    
    
    rmPosit = np.where(excludeObs > 0)
    apriRmScanNum = scanInfo.Obs2Scan[rmPosit[0]]
    
    if len(rmPosit[0]):
        # scanInfo.gd[rmPosit[0]] = 0
        # scanInfo.gdSig[rmPosit[0]] = 0
        
        for i in range(len(rmPosit[0])):
            if apriRmScanNum[i] in newScanNum:
                scanNum = newScanNum.index(apriRmScanNum[i])
                sta = scanInfo.Obs2Baseline[rmPosit[0][i]] - 1
                staCount[scanNum][sta] -= 1
                
                if staCount[scanNum][sta[0]] == 0:
                    scanInfo.Scan2Station[apriRmScanNum[i]-1,sta[0]] = 0
                if staCount[scanNum][sta[1]] == 0:
                    scanInfo.Scan2Station[apriRmScanNum[i]-1,sta[1]] = 0
            
        for i in range(scanInfo.Scan2Station.shape[1]):
            if not np.any(scanInfo.Scan2Station[:,i]):
                if not scanInfo.stationAll[i] in scanInfo.rmSta:
                    scanInfo.rmSta.append(scanInfo.stationAll[i])

        scanInfo.Obs2Scan[rmPosit[0]] = 0
        scanInfo.Obs2Source[rmPosit[0]] = 0
        
        # if there exist the scan number, if zero, then remove scan, else pass
        rmScanNum = []
        temp = list(set(apriRmScanNum))
        for scan in temp:
            allScanNum = np.where(scanInfo.Obs2Scan == scan)
            if len(allScanNum[0]) == 0:
                rmScanNum.append(newScanNum.index(scan))
        
        if len(rmScanNum)>0:
            scanInfo.rmScanNum = sorted(rmScanNum)
            scanInfo.scanMJD = np.delete(scanInfo.scanMJD, rmScanNum)
            scanInfo.scanSource = np.delete(scanInfo.scanSource, rmScanNum)
            scanInfo.scan2Source = np.delete(scanInfo.scan2Source, rmScanNum)
            scanInfo.scanTime = np.delete(scanInfo.scanTime, rmScanNum, axis=0)            
        
def cleanBl(blRm, scanInfo):
    """
    Remove the observe of baseline.
    ---------------------
    input: 
        scanInfo : class
            the scan struct
        blRm : list
            the baseline to remove, eg:['WETTZ13S','WETTZ13N']
    output: 
        excludeObs : array
            which observe to be exclude (>0-exclude,=0-include)
    ---------------------
    """
    excludeObs = np.zeros(len(scanInfo.Obs2Scan), dtype=int)
    index = []
    for sta in blRm:
        blank = '        '
        sta = sta + blank[0:8-len(sta)]
        if sta.upper() in scanInfo.stationAll:
            index.append(scanInfo.stationAll(sta.upper()) + 1)

    if len(index) == 2:
        index.sort()
        posit = np.where((scanInfo.Obs2Baseline[:,0]==index[0]) & \
                         (scanInfo.Obs2Baseline[:,1]==index[1]))
        excludeObs[posit[0]] = excludeObs[posit[0]] + 1
        
    return excludeObs

def cleanDelayFlag(scanInfo):
    """
    Remove the unweight flag
    ---------------------
    input: 
        scanInfo                : the scan struct
    output: 
        excludeScan              : which observe to be exclude (>0-exclude,=0-include)
    ---------------------
    """
    excludeObs = np.zeros(len(scanInfo.Obs2Scan), dtype=int)
    # if len(scanInfo.Obs2Scan) == len(scanInfo.delayFlag):
    if np.any(scanInfo.delayFlag):
        posit = np.where(scanInfo.delayFlag > 0)
        excludeObs[posit[0]] = excludeObs[posit[0]] + 1
    
    return excludeObs

def cleanIonFlag(scanInfo):
    excludeObs = np.zeros(len(scanInfo.Obs2Scan), dtype=int)

    posit = np.where(scanInfo.ionFlag != 0)
    excludeObs[posit[0]] = excludeObs[posit[0]] + 1

    return excludeObs

def cleanQcode(scanInfo, qcodeLim):
    """
    Remove the low quality observe, the exclude standard is X band quality.
    ---------------------
    input: 
        scanInfo : class
            the scan struct
        qcodeLim : int
            the limit quality code
    output: 
        excludeScan : array
            which observe to be exclude (>0-exclude,=0-include)
    ---------------------
    """
    excludeObs = np.zeros(len(scanInfo.Obs2Scan), dtype=int)
    
    for i in range(len(scanInfo.baseInfo[0])):
        # if len(scanInfo.qCode[i]) == len(scanInfo.Obs2Scan):
        posit = np.where(scanInfo.qCode[i] <= qcodeLim)
        excludeObs[posit[0]] = excludeObs[posit[0]] + 1
    
    return excludeObs

def cleanSou(rmSou, scanInfo):
    """
    Remove the observe of source
    ---------------------
    input: 
        scanInfo : class
            the scan struct
        rmSou : list
            the source list to remove
    output: 
        excludeScan : array
            which observe to be exclude (>0-exclude,=0-include)
    ---------------------
    """
    excludeObs = np.zeros(len(scanInfo.Obs2Scan), dtype=int)

    #20250217 the bug for remove source in data
    k = 0
    for i in range(len(rmSou)):
        sou = '%-8s'%rmSou[i].upper()
        try:
            index = scanInfo.sourceAll.index(sou) + 1
            posit = np.where(scanInfo.Obs2Source==index)

            excludeObs[posit[0]] = excludeObs[posit[0]] + 1
            k += 1
        except:
            continue
            
    if (len(scanInfo.sourceAll)- k <= 1):
        print('        Error: the used source is less than 1, please modify the DATA part of cnt file!')
        sys.exit() 
    return excludeObs
    

def cleanSta(rmSta, scanInfo):
    """
    Remove the observe of station
    ---------------------
    input: 
        scanInfo : class
            the scan struct
        rmSta : list
            the station list to remove
    output: 
        excludeScan : array
            which observe to be exclude (>0-exclude,=0-include)
    ---------------------
    """
    excludeObs = np.zeros(len(scanInfo.Obs2Scan), dtype=int)
    k = 0
    for i in range(len(rmSta)):
        sta = rmSta[i].upper()
        blank = '        '
        sta = sta + blank[0:8-len(sta)]
        if not sta in scanInfo.rmSta:
            scanInfo.rmSta.append(sta)
        
        if sta in scanInfo.stationAll:
            k += 1
            index = scanInfo.stationAll.index(sta) + 1
            posit = np.where((scanInfo.Obs2Baseline[:,0]==index) | \
                             (scanInfo.Obs2Baseline[:,1]==index))
                
            excludeObs[posit[0]] = excludeObs[posit[0]] + 1
            
    if (len(scanInfo.stationAll)- k <= 1):
        print('        Error: the used station is less than 1, please modify the DATA part of cnt file!')
        sys.exit() 
    return excludeObs

def makeScan(v2Flag,scanInfo):
    """
    rebuild the scanInfo for each scan
    ---------------------
    input: 
        v2Flag : int
            create the vgosDB version 2 Flag
        scanInfo : class
            the scan struct
    output: 
        scanInfo : class 
            creat the value for each scan
    ---------------------
    """
    strStation = np.array(scanInfo.stationAll)
    
    for iscan in range(scanInfo.scanNum):
        scan_posit = np.where(scanInfo.Obs2Scan==(iscan+1))  # +1: start from 1

        if len(scan_posit[0]):
            scanInfo.scanObsNum.append(len(scan_posit[0]))
            scanInfo.scanBl.append((scanInfo.Obs2Baseline-1)[scan_posit[0]].tolist()) # -1: search from 1

            if v2Flag != 1:
                tempgd = []
                tempgdSig = []
                for iband in range(len(scanInfo.baseInfo[0])):
                    tempgd.append(scanInfo.gd[iband][scan_posit[0]])
                    tempgdSig.append(scanInfo.gdSig[iband][scan_posit[0]])
                    
                scanInfo.scanGD.append(tempgd)
                scanInfo.scanGDSig.append(tempgdSig)
        
        sta_posit = np.where(scanInfo.Scan2Station[iscan] != 0)
        
        
        temp_T = []
        temp_P = []
        temp_H = []
        temp_cc = []
        
        if len(sta_posit[0]):
            if v2Flag != 1:
                for i in range(len(sta_posit[0])):
                    temp_T.append(scanInfo.T[sta_posit[0][i]][scanInfo.Scan2Station[iscan][sta_posit[0][i]]-1])
                    temp_P.append(scanInfo.P[sta_posit[0][i]][scanInfo.Scan2Station[iscan][sta_posit[0][i]]-1])
                    temp_H.append(scanInfo.H[sta_posit[0][i]][scanInfo.Scan2Station[iscan][sta_posit[0][i]]-1])
                    temp_cc.append(scanInfo.cableCal[sta_posit[0][i]][scanInfo.Scan2Station[iscan][sta_posit[0][i]]-1])
                scanInfo.scanT.append(temp_T)
                scanInfo.scanP.append(temp_P)
                scanInfo.scanH.append(temp_H)
                scanInfo.scanCabCal.append(temp_cc)
            
            scanInfo.scanStation.append(strStation[sta_posit[0]].tolist())
            scanInfo.scanTRP.append(np.zeros(len(sta_posit[0])).tolist())
        
    #write_result(vgosDBPath, session, scanInfo)

def updateStaEstimate(Scan2Station, targetList, targetMode):
    rmFlag = np.sum(Scan2Station,axis=0)
    rmPosit = np.where(rmFlag==0)[0]
    if len(rmPosit):
        for i in rmPosit:
            rmSta = targetList[i]
            if rmSta not in targetMode:
                targetMode.append(rmSta)

    if len(targetMode) >= 3:
        for i in range(2,len(targetMode)):
            if len(targetMode[i]) != 8:
                targetMode[i] = '%-8s'%targetMode[i]
    
def updateSouEstimate(scanInfo, targetMode):
    # souNum = np.unique(scanInfo.scan2Source)   # start from 0
    # scanSouP = np.where(scanInfo.Obs2Source!=0)
    # Obs2Source = scanInfo.Obs2Source[scanSouP[0]]-1
    
    if len(targetMode) >= 3:
        for i in range(2,len(targetMode)):
            if len(targetMode[i]) != 8:
                targetMode[i] = '%-8s'%targetMode[i]
    
    # estimate the source with the observe more than 5
    noEstSou = []
    for i in range(len(scanInfo.sourceAll)):
        sp = np.where(scanInfo.Obs2Source==(i+1))
        if len(sp[0]) < 5:
            noEstSou.append(scanInfo.sourceAll[i])
    
    # for i in range(len(souNum)):
    #     sp = np.where(Obs2Source==souNum[i])
    #     if len(sp[0]) < 5:
    #         noEstSou.append(scanInfo.sourceAll[souNum[i]])
    
    # souNum = souNum.tolist()
    # for i in range(len(scanInfo.sourceAll)):
    #     if i not in souNum:
    #         noEstSou.append(scanInfo.sourceAll[i])
            
            
    if len(noEstSou):
        if len(targetMode) == 1 and targetMode[0] == 'YES':
            targetMode += ['EXCEPT'] + noEstSou
        elif targetMode[0] == 'YES' and 'EXCEPT' in targetMode:
            for isou in noEstSou:
                if isou not in targetMode:
                    targetMode.append(isou)
        elif targetMode[0] == 'NO' and 'EXCEPT' in targetMode:
            tempSou = []
            for isou in scanInfo.sourceAll:
                if isou not in targetMode:
                    tempSou.append(isou)
            
            for isou in noEstSou:
                if isou not in tempSou:
                    tempSou.append(isou)

            targetMode = ['YES','EXCEPT']+tempSou

def updete_refClk(scanInfo):
    '''
    Get the reference clock station which has max observe
    '''
    
    useBaseline = scanInfo.Obs2Baseline[np.where(scanInfo.Obs2Scan!=0)[0]]
    
    staObs = []
    for i in range(len(scanInfo.stationAll)):
        baselineSub = useBaseline - (i+1)
        baselineMul = baselineSub[:,0]*baselineSub[:,1]
        obsNum = np.where(baselineMul ==0)[0]
        
        if len(obsNum):
            staObs.append(len(obsNum))
        else:
            staObs.append(0)

    maxValue = max(staObs)
    index = staObs.index(maxValue)
    scanInfo.refclk = scanInfo.stationAll[index]
