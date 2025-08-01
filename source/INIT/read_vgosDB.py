#!/usr/bin/env python3

import os,sys
import re

sys.path.append("..//")
import netCDF4 as nc
import numpy as np

np.set_printoptions(precision=15)

from COMMON import *
from INIT.read_wrpFile import *

def read_vgosDB(Param, num):
    """
    Read the vgosDB file
    ---------------------
    input: 
        Param          : PARAMETER struct
        num            : which session to process
    output: 
        scanInfo       : scan struct
    ---------------------
    """
    vgosDBPath = Param.Setup.vgosdbPath
    session = Param.Arcs.session[num]
    AC = Param.Arcs.AC[num]
    version = Param.Arcs.version[num]

    year = sessionNameCheck(session)
    
    sessionPath = vgosDBPath + str(year) + '/' + session
    if not os.path.exists(sessionPath):
        sys.stderr.write('The path %s not exists!'%(sessionPath))
        sys.exit()
    
    if AC == 'NONE':
        wrpFilename = sessionPath+'/'+session+'_V%03d'%(version)+'_kall.wrp'
    else:
        wrpFilename = sessionPath+'/'+session+'_V%03d'%(version)+'_i'+AC+'_kall.wrp'

    if not os.path.exists(wrpFilename):
        sys.stderr.write('The file %s not exists!'%(wrpFilename))
        sys.exit()
    
    wrpInfo = readWrp(wrpFilename)
    
    scanInfo = SCAN()
    scanInfo.sessionName = session
    
    if wrpInfo.Flag >= 1:
        read_HOPSDone(Param, sessionPath, scanInfo, wrpInfo)
        
    clkBrk = CLKBRK()
    clkBrk.initBrk(scanInfo.stationAll)
    scanInfo.clkBrk = clkBrk
    
    if wrpInfo.Flag >= 2:
        read_AmbIonBkDone(Param, sessionPath, scanInfo, wrpInfo)
    
    return scanInfo, wrpInfo

def read_HOPSDone(Param, sessionPath, scanInfo, wrpInfo):
    '''
    Reading the vgosDB file that after the HOPS processed.

    '''
    
    read_Head(scanInfo, sessionPath, wrpInfo)        # get session station and source
    read_Source(scanInfo, sessionPath,wrpInfo)               # get apriori source position
    read_Station(scanInfo, sessionPath,wrpInfo)              # get apriori station position
    read_nscode(scanInfo, Param)                     # get the station codes
    read_TimeUTC(scanInfo, sessionPath)              # get the scan time
    read_ScanTimeMJD(scanInfo, sessionPath)          # get the scan MJD
    
    read_ObsCross(scanInfo, sessionPath)             # get observe and scan relation
    read_StationCorss(scanInfo, sessionPath, wrpInfo)# get station and scan relation
    read_SourceCorss(scanInfo, sessionPath, wrpInfo) # get source and scan relation
    
    read_baseInfo(scanInfo, sessionPath, wrpInfo)    # get band number and ambiguity size
    read_groupDelay(scanInfo, sessionPath, wrpInfo)  # get the group delay
    read_QualityCode(scanInfo, sessionPath, wrpInfo) # get the quality of obs
    # if wrpInfo.Flag != 3:
    if wrpInfo.Flag < 2:
        read_channelInfo(scanInfo, sessionPath, wrpInfo) # get the channel information
    
    # ------------------------ the reference time set ------------------------#
    if Param.Flags.eopTime == 'NOON':
        scanInfo.refMJD = np.floor(scanInfo.scanMJD[-1]) + 1.5
    elif Param.Flags.eopTime == 'MIDNIGHT':
        scanInfo.refMJD = np.floor(scanInfo.scanMJD[-1])
    else:
        scanInfo.refMJD = np.mean(scanInfo.scanMJD)
    
    # ---------------------- the reference station clock ---------------------#    
    # refSta = 'KOKEE   '
    # if refSta in scanInfo.stationAll:
    #     scanInfo.refclk = refSta
    # else:
    #     scanInfo.refclk = scanInfo.stationAll[0]
    
    # chocie_refClk(scanInfo)
    read_cable(scanInfo, sessionPath, wrpInfo)
    read_Met(scanInfo, sessionPath, wrpInfo)
    read_FmoutGNSS(scanInfo, sessionPath, wrpInfo)
    scanInfo.delayFlag = np.zeros(len(scanInfo.Obs2Scan), dtype=int)

def read_AmbIonBkDone(Param, sessionPath, scanInfo, wrpInfo):
    '''
    Reading the vgosDB file that has remove ambiguity and ionosphere.

    '''
        
    if Param.Flags.blClk == 'IN':
        read_blClock(scanInfo, sessionPath, wrpInfo)
    
    read_Edit(scanInfo, sessionPath, wrpInfo)
    read_ionFile(scanInfo, sessionPath, wrpInfo)
    
    
    read_GroupBLWeights(Param, scanInfo, sessionPath, wrpInfo)
    read_groupDelayFull(scanInfo, sessionPath, wrpInfo)
    read_clockBreak(scanInfo, sessionPath, wrpInfo)
    read_calibrationSetup(scanInfo, sessionPath, wrpInfo)
    read_clocksetup(scanInfo, sessionPath, wrpInfo)
          
def read_baseInfo(scanInfo, sessionPath, wrpInfo):
    """
    Get the session base information(band,reFreq,ambigSize)

    """
    band = []
    reFreq = []
    ambigSize = []
    
    for file in wrpInfo.Observe:
        if 'GroupDelay_' in file:
            index = file.index('_')
            if not file[index+2] in band:
                band.append(file[index+2])
                
    # sort the band list
    if len(band) == 2:
        band.sort()
                
    for i in range(len(band)):
        # reFreq.append([])
        try:
            data = nc.Dataset(sessionPath+'/Observables/RefFreq_b'+band[i]+'.nc')
            reFreq.append(data['RefFreq'][:].data)
        except:
            print('         Not exist RefFreq_b'+band[i]+'.nc')
            reFreq.append(0)
        try:
            data = nc.Dataset(sessionPath+'/Observables/AmbigSize_b'+band[i]+'.nc')
            if len(data['AmbigSize'][:].data) == 1:
                ambigSize.append(data['AmbigSize'][:].data[0]*np.ones(len(scanInfo.Obs2Scan)))
            else:
                ambigSize.append(data['AmbigSize'][:].data)
        except:
            print('         Not exist AmbigSize_b'+band[i]+'.nc')
            ambigSize.append([])
               
    scanInfo.baseInfo = [band,reFreq,ambigSize]
    scanInfo.ambigNum = np.zeros((len(band),len(scanInfo.Obs2Scan)))


def read_blClock(scanInfo, sessionPath, wrpInfo):
    """
    Read the BaselineClockSetup.nc file, get baseline clock list.

    """ 
    blClock = []
    
    blClockFile = ''
    for file in wrpInfo.Solve:
        if 'BaselineClockSetup' in file:
            blClockFile = file
    
    if len(blClockFile):
        path = sessionPath + '/Solve/'+blClockFile
        data = nc.Dataset(path)
        
        temp=np.char.decode(data['BaselineClock'][:].data)

        if len(temp.shape) == 2:
            sta1 = changeBlank(temp[0])
            sta2 = changeBlank(temp[1])

            sta1P = scanInfo.stationAll.index(sta1) + 1
            sta2P = scanInfo.stationAll.index(sta2) + 1

            blClock.append([sta1P,sta2P])
        elif len(temp.shape) == 3:
            for i in range(data['BaselineClock'].shape[0]):
                #sta1 = ''.join(temp[i][0])
                #sta2 = ''.join(temp[i][1])
                sta1 = changeBlank(temp[i][0])
                sta2 = changeBlank(temp[i][1])

                sta1P = scanInfo.stationAll.index(sta1) + 1
                sta2P = scanInfo.stationAll.index(sta2) + 1

                blClock.append([sta1P, sta2P])

        scanInfo.blClkList = blClock
    
def read_cable(scanInfo, sessionPath, wrpInfo):
    """
    Read the Cal-Cable.nc file, get cable correct for earch station.
   
    """
    cableCal = []
    for i in range(len(scanInfo.stationAll)):
        temp = np.where(scanInfo.Scan2Station[:,i] != 0)
        NumStatScan = scanInfo.Scan2Station[temp[0][-1],i]
        
        # signFlag = 1
        # if scanInfo.stationAll[i] == 'NYALES20':
        #     signFlag = -1
        
        cableFile = ''
        index = wrpInfo.Station[0].index(scanInfo.stationAll[i].strip())
        for file in wrpInfo.Station[1][index]:
            if 'Cal-Cable' in file:
                cableFile = file.strip()
        
        if len(cableFile):
            path = sessionPath+'/'+wrpInfo.Station[0][index]+'/'+cableFile
            data = nc.Dataset(path)
            
            try:
                data.variables['Cal-Cable']
            except KeyError:
                cableFlag = False
            else:
                cableFlag = True
            
            if cableFlag:
                if data['Cal-Cable'][:].data.shape[0] == NumStatScan:
                    # cableCal.append(data['Cal-Cable'][:].data)
                    if std(data['Cal-Cable'][:].data*1E12) > 1000:
                        cableCal.append(np.zeros(NumStatScan))
                    else:
                        cableCal.append(data['Cal-Cable'][:].data)
                    
                else:
                    print('        The cable cal of %s not equal! Set default'%scanInfo.stationAll[i].strip())
                    cableCal.append(np.zeros(NumStatScan))
            else:
                if data['Cal-CableCorrections'][:].data.shape[0] == NumStatScan:
                    try:
                        data['Cal-CableCorrections'][:].data.shape[1]
                    except IndexError:
                        cableCal.append(data['Cal-CableCorrections'][:].data)
                    else:
                        cableCal.append(data['Cal-CableCorrections'][:,0].data)
                else:
                    print('        The cable cal of %s not equal! Set default'%scanInfo.stationAll[i].strip())
                    cableCal.append(np.zeros(NumStatScan))
        else:
            cableCal.append(np.zeros(NumStatScan))
            
    scanInfo.cableCal = cableCal
    
def read_calibrationSetup(scanInfo, sessionPath, wrpInfo):
    '''
    Reading the CalibrationSetup.nc, get the cable cal used.

    '''
    
    for file in wrpInfo.Solve:
        if 'CalibrationSetup' in file:
            path = sessionPath + '/Solve/'+file
            data = nc.Dataset(path)
            staCableFlag = data['StatCalFlag'][:].data
            cableUsedPosit = np.where(staCableFlag==1)
            temp_sta = np.char.decode(data['StatCalStationList'][:].data)
            
            cableUsedStaList = []
            for i in cableUsedPosit[0]:
                cableUsedStaList.append(''.join(temp_sta[i]))
                
            for i in range(len(scanInfo.stationAll)):
                if scanInfo.stationAll[i] not in cableUsedStaList:
                    scanInfo.cableCal[i] = 0*scanInfo.cableCal[i]
    
def read_channelInfo(scanInfo, sessionPath, wrpInfo):
    '''
    Reading the ChannelInfo_b?.nc, get the effect frequency.

    '''
    
    effFreq = []
    
    for ib in range(len(scanInfo.baseInfo[0])):
        band = scanInfo.baseInfo[0][ib]
        for file in wrpInfo.Observe:
            if ('ChannelInfo_b'+band) in file:
                path = sessionPath + '/Observables/'+file
                data = nc.Dataset(path)
                sampRate = data['SampleRate'][:].data
                chanAmpPhase = data['ChanAmpPhase'][:].data
                numAp = data['NumAp'][:].data
                chanFreq = data['ChannelFreq'][:].data
                
                effFreq.append(calcEffFreq(sampRate, chanFreq, chanAmpPhase, numAp))
                
    scanInfo.effFreq = effFreq
    
def read_clockBreak(scanInfo, sessionPath, wrpInfo):
    """
    Reading the ClockBreak.nc file, get the clock break.

    """
    
    clkBkName = ''
    for file in wrpInfo.Session:
        if 'ClockBreak' in file:
            clkBkName = file
            
    if clkBkName:
        brkNum = 0
        path = sessionPath + '/Session/'+clkBkName
        if os.path.exists(path):
            data = nc.Dataset(path)
            brkNum = data['BRK_NUMB'][:].data
            
        if brkNum != 0:
            brkSta = []
            brkEpoch = []
            if data['ClockBreakStationList'][:].data.size <= 8:
                temp_sta = np.char.decode(data['ClockBreakStationList'][:].data)
                for i in range(brkNum[0]):
                    temp = ''.join(temp_sta)
                    temp = temp.strip().replace(' ', '_')

                    if len(temp) == 8:
                        brkSta.append(temp)
                    else:
                        blanks = '        '
                        brkSta.append(temp + blanks[:8-len(temp)])
            else:
                temp_sta = np.char.decode(data['ClockBreakStationList'][:].data)
                for i in range(data['ClockBreakStationList'][:].shape[0]):
                    #2025.02.12
                    brkSta.append(changeBlank(temp_sta[i]))
                    
            brkEpoch = data['ClockBreakEpoch'][:].data
            for i in range(len(brkEpoch)):
                if brkEpoch[i] > 2400000.5:
                    brkEpoch[i] -= 2400000.5
            
            
            for i in range(len(brkSta)):
                posit = scanInfo.clkBrk.staName.index(brkSta[i])
                scanInfo.clkBrk.brkFlag[posit] += 1
                scanInfo.clkBrk.brkMJD[posit].append(brkEpoch[i])
                
def read_clocksetup(scanInfo, sessionPath, wrpInfo):
    """
    Reading the ClockSetup.nc file, get the reference clock station.
    """
    
    for file in wrpInfo.Solve:
        if 'ClockSetup' in file[:11]:
            path = sessionPath + '/Solve/'+file
            data = nc.Dataset(path)    
            
            temp = np.char.decode(data['ReferenceClock'][:].data)
            if temp.ndim >= 2:
                #temprefclk = ''.join(temp[0])
                temprefclk = changeBlank(temp[0])
            else:
                #temprefclk = ''.join(temp)
                temprefclk = changeBlank(temp)
            blank = '        '
            scanInfo.refclk = temprefclk + blank[:8-len(temprefclk)]
            
def read_Edit(scanInfo, sessionPath, wrpInfo):
    """
    Reading the Edit.nc file, get the delay unweight flag

    """
    
    for file in wrpInfo.Observe:
        if 'Edit_' in file or 'Edit.' in file:
            path = sessionPath + '/ObsEdit/'+file
            data = nc.Dataset(path)
            scanInfo.delayFlag = data['DelayFlag'][:].data
        
            
    if len(scanInfo.delayFlag) == 0 or len(scanInfo.delayFlag) != len(scanInfo.Obs2Scan):
        scanInfo.delayFlag = np.zeros(len(scanInfo.Obs2Scan), dtype=int)
    # else:
    #     path = sessionPath + '/ObsEdit/Edit.nc'
    #     if os.path.exists(path):
    #         data = nc.Dataset(path)
    #         scanInfo.delayFlag = data['DelayFlag'][:].data
    
def read_FmoutGNSS(scanInfo, sessionPath, wrpInfo):
    """
    Reading the Fmout-GNSS.nc file, get the clock change

    """
    
    Fmout_GNSS = []
    for sta in scanInfo.stationAll:
        tempFG = [[],[]]
        index = wrpInfo.Station[0].index(sta.strip())
        for file in wrpInfo.Station[1][index]:
            if 'Fmout-GNSS' in file:
                path = sessionPath + '/' + sta.strip()+'/'+file
                data = nc.Dataset(path)
                tempFG[0] = data['ClkMJD'][:].data
                tempFG[1] = data['Fmout-GNSS'][:].data
        if len(tempFG[0]):
            Fmout_GNSS.append(tempFG)
        else:
            Fmout_GNSS.append([scanInfo.scanMJD, np.zeros(len(scanInfo.scanMJD))])
            
    scanInfo.Fmout_GNSS = Fmout_GNSS
    

def read_groupDelay(scanInfo, sessionPath, wrpInfo):
    """
    Read the GroupDelay_b?.nc, get the group delay and sigma.

    """
    
    gd = []
    gdSig = []
    scanInfo.gdSigApri = []
    for ib in range(len(scanInfo.baseInfo[0])):
        band = scanInfo.baseInfo[0][ib]
        for file in wrpInfo.Observe:
            if ('GroupDelay_b'+band) in file:
                path = sessionPath + '/Observables/'+file
                data = nc.Dataset(path)
                temp = data['GroupDelay'][:].data # [s]
                # temp[scanInfo.reversePosit] = 0 - temp[scanInfo.reversePosit]
                gd.append(temp)
                tempSig = data['GroupDelaySig'][:].data
                gdSig.append(np.sqrt(tempSig**2 + (0.005/const.c)**2))  # [s]
                scanInfo.gdSigApri.append(tempSig)
        
    # data=nc.Dataset(sessionPath + '/ObsEdit/NumGroupAmbig_bX.nc')
    # amb = data['NumGroupAmbig'][:].data
    # gd[1] = gd[1] + amb*scanInfo.baseInfo[2][1]
    
    # data=nc.Dataset(sessionPath + '/ObsEdit/NumGroupAmbig_bS.nc')
    # amb = data['NumGroupAmbig'][:].data
    # gd[0] = gd[0] + amb*scanInfo.baseInfo[2][0]
    
    # iondata = np.loadtxt('/Users/dangyao/Downloads/stec_23JUN25XN.out.txt',comments='!', usecols=[5],dtype=float,unpack=True)
    
    # gd[0] -= iondata
    scanInfo.gd = gd
    scanInfo.gdApri = gd
    scanInfo.gdSig = gdSig
    
def read_groupDelayFull(scanInfo, sessionPath, wrpInfo):
    """
    Read the GroupDelayFull_bX.nc, get the group delay that remove the ambiguity, 
        and correct the ionosphere delay.

    """
    
    gdFull = []
    for ib in range(len(scanInfo.baseInfo[0])):
        band = scanInfo.baseInfo[0][ib]
        #temp = []
        temp = scanInfo.gd[ib] + 0

        #20250213
        pattern = re.compile(f'^{r"GroupDelayFull"}.*{r"_b%s"}.*'%band)
        gfile = [file for file in wrpInfo.Observe if pattern.match(file)]
        if len(gfile) == 1:
            path = sessionPath + '/ObsEdit/' + gfile[0]
            data = nc.Dataset(path)
            temp = data['GroupDelayFull'][:].data  # [s]
        elif len(gfile) > 1:
            print('wrp file read wrong!')
            sys.exit()
        gdFull.append(temp)

        '''
        for file in wrpInfo.Observe:
            if 'GroupDelayFull_' in file and ('_b'+band) in file:
                path = sessionPath + '/ObsEdit/'+file
                data = nc.Dataset(path)
                temp = data['GroupDelayFull'][:].data  # [s]
                # temp[scanInfo.reversePosit] = 0 - temp[scanInfo.reversePosit]
                gdFull.append(temp)
        '''
                
    if len(gdFull) != 0:

        scanInfo.gdApri = gdFull
        scanInfo.gd = []
        for iband in range(len(scanInfo.baseInfo[0])):
            if scanInfo.baseInfo[0][iband] == 'X':
                scanInfo.gd.append(gdFull[iband] - scanInfo.iondl)
            else:
                scanInfo.gd.append(gdFull[iband])

        index = scanInfo.baseInfo[0].index('X')
        #gdFull[index] = gdFull[index] - scanInfo.iondl
        #scanInfo.gd = gdFull
        if len(scanInfo.blWeight) != len(scanInfo.gdSig[index]):
            scanInfo.gdSig[index] = np.sqrt(scanInfo.gdSig[index] ** 2 + scanInfo.iondlSig ** 2)
        else:
            scanInfo.gdSig[index] = np.sqrt(scanInfo.gdSig[index]**2 + scanInfo.iondlSig**2 + scanInfo.blWeight**2)

def read_GroupBLWeights(Param, scanInfo, sessionPath, wrpInfo):
    """
    Read the GroupBLWeights.nc file, get reweight information

    """
    weight = np.zeros(len(scanInfo.Obs2Scan))
    
    if Param.Setup.weight == 'IN':
        for file in wrpInfo.Session:
            if 'GroupBLWeights' in file:
                path = sessionPath + '/Session/'+file
                data = nc.Dataset(path)
                blWeight = data['GroupBLWeights'][:].data
                blList = data['GroupBLWeightStationList'][:].data
                blNum = len(blList)
                
                for i in range(blNum):
                    if len(blList.shape) == 3:
                        temp1 = np.char.decode(blList[i][0])
                        temp2 = np.char.decode(blList[i][1])
                    elif len(blList.shape) == 2:
                        temp1 = np.char.decode(blList[i])
                        temp2 = np.char.decode(blList[i])
                    bl1 = ''.join(temp1)
                    bl2 = ''.join(temp2)
                    #20250324
                    blank = '        '
                    if ' ' in bl1.strip():
                        temp  = bl1.strip().replace(' ','_')
                        bl1 = temp + blank[0:8-len(temp)]
                    if ' ' in bl2.strip():
                        temp  = bl2.strip().replace(' ','_')
                        bl2 = temp + blank[0:8-len(temp)]

                    index1 = scanInfo.stationAll.index(bl1)
                    index2 = scanInfo.stationAll.index(bl2)
                    
                    blSub = scanInfo.Obs2Baseline - [index1+1, index2+1]
                    blPosit = np.where(np.sum(blSub,axis=1) == 0)
                    
                    if len(blList.shape) == 3:
                        weight[blPosit] = blWeight[0][i]
                    elif len(blList.shape) == 3:
                        weight[blPosit] = blWeight[i]
                
    scanInfo.blWeight = weight
                
def read_Head(scanInfo, sessionPath, wrpInfo):
    """
    Read the head.nc file, get station and source list

    """
    staList = []
    sourList = []

    for file in wrpInfo.Session:
        if 'Head' in file:
            path = sessionPath+'/'+file
    
    if os.path.exists(path):
        data = nc.Dataset(path)
        
        # station list
        temp_sta = np.char.decode(data['StationList'][:].data)
        for i in range(data['StationList'][:].shape[0]):
            #staStr = ''.join(temp_sta[i])
            #staList.append(staStr)

            # 2025.02.12
            staName = changeBlank(temp_sta[i])

            staList.append(staName)

        # source list
        temp_sour = np.char.decode(data['SourceList'][:].data)
        for i in range(data['SourceList'][:].shape[0]):
            sourList.append(''.join(temp_sour[i]))
            
        # if len(staList) != data['NumStation'][:].data[0] or \
        #    len(sourList) != data['NumSource'][:].data[0]:
        #     print('The station or source number not equal in Head.nc!')
        #     sys.exit()
            
        scanInfo.stationAll = staList
        scanInfo.sourceAll = sourList

        try:
            temp_exp = np.char.decode(data['ExpName'][:].data)
            scanInfo.expName = ''.join(temp_exp)
        except:
            scanInfo.expName = 'None'
        try:
            temp_expd = np.char.decode(data['ExpDescription'][:].data)
            scanInfo.expDescrip = ''.join(temp_expd)
        except:
            scanInfo.expDescrip = 'None'
            
    else:
        print('The Head.nc file is not exists!')
        sys.exit()
        
def read_ionFile(scanInfo, sessionPath, wrpInfo):
    """
    Read the Cal-SlantPathIonoGroup.nc file, get ionosphere delay

    """
    
    ionFile = ''
    for file in wrpInfo.Observe:
        if 'Cal-SlantPathIonoGroup_bX' in file:
            ionFile = file
    
    if len(ionFile):
        path = sessionPath + '/ObsDerived/'+ionFile
        if os.path.exists(path):
            data = nc.Dataset(path)
            
            if data['Cal-SlantPathIonoGroup'][:].data.shape[0] == 2:
                scanInfo.iondl = np.zeros(len(scanInfo.Obs2Scan))
                scanInfo.iondlSig = np.zeros(len(scanInfo.Obs2Scan))
            else:
                scanInfo.iondl = data['Cal-SlantPathIonoGroup'][:].data[:,0]
                scanInfo.iondlSig = data['Cal-SlantPathIonoGroupSigma'][:].data[:,0]
        else:
            scanInfo.iondl = np.zeros(len(scanInfo.Obs2Scan))
            scanInfo.iondlSig = np.zeros(len(scanInfo.Obs2Scan))
    else:
        scanInfo.iondl = np.zeros(len(scanInfo.Obs2Scan))
        scanInfo.iondlSig = np.zeros(len(scanInfo.Obs2Scan))
    
    # scanInfo.iondl = np.zeros(len(scanInfo.Obs2Scan))
    # scanInfo.iondlSig = np.zeros(len(scanInfo.Obs2Scan))
     
def read_Met(scanInfo, sessionPath, wrpInfo):
    """
    Read the Met.nc file, get T/P/H of earch station.

    """
    T = []
    P = []
    H = []
    
    for i in range(len(scanInfo.stationAll)):
        path = sessionPath + '/' + scanInfo.stationAll[i].strip() + '/Met.nc'
        temp = np.where(scanInfo.Scan2Station[:,i] != 0)
        NumStatScan = scanInfo.Scan2Station[temp[0][-1],i]
        
        metFile = ''
        index = wrpInfo.Station[0].index(scanInfo.stationAll[i].strip())
        for file in wrpInfo.Station[1][index]:
            if 'Met' in file:
                metFile = file.strip()
        
        
        if len(metFile):
            # path = sessionPath + '/' + wrpInfo.Station[0][index] + '/Met.nc'
            path = sessionPath + '/' + wrpInfo.Station[0][index] + '/'+metFile
            data = nc.Dataset(path)
            
            if data['TempC'][:].data.shape[0] == NumStatScan:
                T.append(data['TempC'][:].data)
            else:
                print('        The TempC of %s not equal! Set default'%scanInfo.stationAll[i].strip())
                if data['TempC'][:].data.shape[0] == 1:
                    T.append(data['TempC'][:].data[0]*np.ones(NumStatScan))
                elif data['TempC'][:].data.shape[0] > 1:
                    T.append(np.mean(data['TempC'][:].data)*np.ones(NumStatScan))
                                    
            if data['AtmPres'][:].data.shape[0] == NumStatScan:
                P.append(data['AtmPres'][:].data)
            else:
                print('        The Pressure of %s not equal! Set default'%scanInfo.stationAll[i].strip())
                P.append(-999*np.ones(NumStatScan))
                
            if data['RelHum'][:].data.shape[0] == NumStatScan:
                H.append(data['RelHum'][:].data)
            else:
                print('        The RelHum of %s not equal! Set default'%scanInfo.stationAll[i].strip())
                H.append(-999*np.ones(NumStatScan))
            
        else:
            print('        The Met.nc of %s not exists! Set default'%scanInfo.stationAll[i].strip())
            T.append(-999*np.ones(NumStatScan))
            P.append(-999*np.ones(NumStatScan))
            H.append(-999*np.ones(NumStatScan))
    
    scanInfo.T = T
    scanInfo.P = P
    scanInfo.H = H
    
def read_nscode(scanInfo, param):
    '''
    Reading the ns-codes.txt file, get the station codes.

    '''
    nsCode = []
    path = param.Map.stationFile[0:param.Map.stationFile.rfind('/')]
    ns_code = np.loadtxt(os.path.join(path,'ns-codes.txt'),dtype=str,comments='*',usecols=[0,1,2,3],unpack=False)

    sitplPath = os.path.join(path, 'sitpl.dat')
    fid = open(sitplPath,'r')
    lines = fid.readlines()
    fid.close()
    
    sitpl = [[],[]]
    for line in lines:
        sit = line[:8].strip().replace(' ', '_')
        sitpl[0].append(sit)
        sitpl[1].append(line[11:15])
    
    k = 0
    for staStr in scanInfo.stationAll:
        sit = staStr.strip()
        nsCodeP = np.where(ns_code[:,1]==sit)
        
        if sit in sitpl[0]:
            index = sitpl[0].index(sit)
            obsSitpl = sitpl[1][index]
        else:
            obsSitpl = 'NONE'

        if nsCodeP[0].size == 1:
            nsCode.append(ns_code[nsCodeP[0][0]].tolist())
            nsCode[k].append(obsSitpl)
            k += 1
        else:
            print('        The %s not in ns-codes.txt, set default!'%staStr)
            nsCode.append(['Xx',staStr,'XXXXXXXXX','0000','XXXX'])
            k += 1
            #sys.exit()
        
    scanInfo.stationCode = nsCode

def read_ObsCross(scanInfo, sessionPath):
    """
    Read the ObsCrossRef.nc file, get observe and baseline in scan.
    
    """
    path = sessionPath+'/CrossReference/ObsCrossRef.nc'
    
    if os.path.exists(path):
        data = nc.Dataset(path)
        Obs2Scan = data['Obs2Scan'][:].data
        Obs2Baseline = data['Obs2Baseline'][:].data
        
        scanInfo.Obs2Scan = Obs2Scan
        
        scanInfo.Obs2MJD = np.zeros(len(Obs2Scan))
        for i in range(len(scanInfo.scanMJD)):
            posit = np.where(Obs2Scan == (i+1))
            scanInfo.Obs2MJD[posit[0]] = scanInfo.scanMJD[i]
            
        if len(Obs2Baseline) == 2:
            OB = Obs2Baseline
            for i in range(len(scanInfo.scanMJD)-1):
                OB = np.vstack((OB, Obs2Baseline))
                
            scanInfo.Obs2Baseline = OB
        else:
            scanInfo.Obs2Baseline = Obs2Baseline
                
def read_QualityCode(scanInfo, sessionPath, wrpInfo):
    """
    Read the QualityCode.nc file, get the observe quality

    """
    
    qCode = []
    for ib in range(len(scanInfo.baseInfo[0])):
        band = scanInfo.baseInfo[0][ib]
        #'''
        tempn = np.ones(len(scanInfo.gd[ib]))*9
        pattern = re.compile(f'^{r"QualityCode_b%s"}.*'%band)
        gfile = [file for file in wrpInfo.Observe if pattern.match(file)]
        if len(gfile) == 1:
            path = sessionPath + '/Observables/' + gfile[0]
            data = nc.Dataset(path)
            temp = np.char.decode(data['QualityCode'][:].data, 'utf-8')

            # vgosDB from calc/solve
            posit = np.where(((temp == '') | (temp == ' ') | (temp == 'A') | (temp == 'C') |\
                              (temp == 'D') | (temp == 'E') | (temp == 'F') | (temp == 'J')))
            temp[posit] = '0'

            if len(temp) == 1:
                tempn = np.tile(temp, len(scanInfo.gd[ib])).astype(int)
            else:
                tempn = temp.astype(int)
        elif len(gfile) > 1:
            print('wrp file read wrong!')
            sys.exit()

        qCode.append(tempn)

        '''
        for file in wrpInfo.Observe:
            if ('QualityCode_b'+band) in file:
                path = sessionPath + '/Observables/'+file
                data = nc.Dataset(path)
                temp = np.char.decode(data['QualityCode'][:].data, 'utf-8')
                
                # vgosDB from calc/solve
                posit = np.where(((temp=='') | (temp==' ') | (temp=='D') | (temp=='E') | (temp=='F')))
                temp[posit] = '0'

                if len(temp) == 1:
                    temp = np.tile(temp,len(scanInfo.gd[ib]))
                
                qCode.append(temp.astype(int))
        '''
    scanInfo.qCode = qCode
    
def read_ScanTimeMJD(scanInfo, sessionPath):
    '''
    Reading the ScanTimeMJD.nc file, get the Modified Julian Day of earch scan.
    
    '''
    
    path = sessionPath+'/Solve/ScanTimeMJD.nc'
    if os.path.exists(path):
        data = nc.Dataset(path)
        MJD = data['MJD'][:].data
        DayFrac = data['DayFrac'][:].data
        
        scanInfo.scanMJD = MJD + DayFrac
        scanInfo.scanNum = len(DayFrac)

def read_Source(scanInfo, sessionPath, wrpInfo):
    #path = sessionPath + '/Apriori/Source.nc'
    for file in wrpInfo.Session:
        if 'Source' in file and 'CrossRef' not in file:
            path = sessionPath + '/Apriori/'+file

    sourcePosit = np.zeros((len(scanInfo.sourceAll),2)) # [rad]

    if os.path.exists(path):
        data = nc.Dataset(path)
        temp_sour = np.char.decode(data['AprioriSourceList'][:].data)
        sourList = []
        for i in range(data['AprioriSourceList'][:].shape[0]):
            sourList.append(''.join(temp_sour[i]))

        for i in range(len(scanInfo.sourceAll)):
            index = sourList.index(scanInfo.sourceAll[i])
            sourcePosit[i][0] = data['AprioriSource2000RaDec'][:].data[index][0]
            sourcePosit[i][1] = data['AprioriSource2000RaDec'][:].data[index][1]

    scanInfo.souPosit = sourcePosit

def read_Station(scanInfo, sessionPath, wrpInfo):
    #path = sessionPath + '/Apriori/Station.nc'
    for file in wrpInfo.Session:
        if 'Station' in file and 'CrossRef' not in file:
            path = sessionPath + '/Apriori/'+file
    staPosit = np.zeros((len(scanInfo.stationAll), 3))  # [m]

    if os.path.exists(path):
        data = nc.Dataset(path)
        temp_sta = np.char.decode(data['AprioriStationList'][:].data)
        staList = []
        for i in range(data['AprioriStationList'][:].shape[0]):
            #temp_staName = ''.join(temp_sta[i])
            #if ' ' in temp_staName.strip():
            #    staName1 = temp_staName.strip().replace(' ','_')
            #    staName = staName1 + ' '*(8-len(staName1))
            #else:
            #    staName = temp_staName
            #2025.02.12
            staName = changeBlank(temp_sta[i])
            staList.append(staName)

        for i in range(len(scanInfo.stationAll)):
            index = staList.index(scanInfo.stationAll[i])
            staPosit[i][0] = data['AprioriStationXYZ'][:].data[index][0]
            staPosit[i][1] = data['AprioriStationXYZ'][:].data[index][1]
            staPosit[i][2] = data['AprioriStationXYZ'][:].data[index][2]

    scanInfo.staPosit = staPosit

def read_SourceCorss(scanInfo, sessionPath, wrpInfo):
    """
    Read the SourceCrossRef.nc file, get source and scan relationship, like:
    
    source      scan
    2123+010    0
    0059+581    1
    ...

    return:
    scan2Source : start from 0
    Obs2Source : start from 1
        
    """
    for file in wrpInfo.Session:
        if 'SourceCrossRef' in file:
            path = sessionPath + '/CrossReference/'+file
    
    if os.path.exists(path):
        data = nc.Dataset(path)
        Scan2Source = data['Scan2Source'][:].data

        # sorted the source list
        souListSort = sorted(scanInfo.sourceAll)
        tempscanSource = []
        tempscan2Source = []
        for i in range(Scan2Source.shape[0]):
            index = souListSort.index(scanInfo.sourceAll[Scan2Source[i]-1])
            tempscanSource.append(scanInfo.sourceAll[Scan2Source[i]-1])
            tempscan2Source.append(index)
        scanInfo.scanSource = tempscanSource
        scanInfo.scan2Source = np.array(tempscan2Source)
        scanInfo.sourceAll = souListSort

        #scanInfo.scanSource = np.array(scanInfo.sourceAll)[Scan2Source-1].tolist()
        #scanInfo.scan2Source = Scan2Source-1
    
    scanNum = len(scanInfo.scan2Source)
    scanInfo.Obs2Source = np.zeros(len(scanInfo.Obs2Scan),dtype=int)
    
    for scan in range(scanNum):
        temp = np.where(scanInfo.Obs2Scan == (scan+1))
        scanInfo.Obs2Source[temp[0]] = scanInfo.scan2Source[scan] + 1

def read_StationCorss(scanInfo, sessionPath, wrpInfo):
    """
    Read the StationCrossRef.nc file, get station and scan relationship, like:
    
             station (6)
             
    scan     1 0 0 1 1 1
             0 1 1 0 0 0
             0 1 0 1 1 1
             ...
    
    """
    for file in wrpInfo.Session:
        if 'StationCrossRef' in file:
            path = sessionPath+'/CrossReference/'+file
    
    if os.path.exists(path):
        data = nc.Dataset(path)
        Scan2Station = data['Scan2Station'][:].data
        Station2Scan = data['Station2Scan'][:].data
        
        scanInfo.Scan2Station = Scan2Station
        scanInfo.Station2Scan = Station2Scan

def read_TimeUTC(scanInfo, sessionPath):
    """
    Read the TimeUTC.nc file, get observe time (y,m,d,h,mi,s) of earch scan

    """
    path = sessionPath+'/Scan/TimeUTC.nc'
    
    if os.path.exists(path):
        data = nc.Dataset(path)
        YMDHM = data['YMDHM'][:].data
        Second = data['Second'][:].data
        if len(Second) == 1:
            Secondn = np.ones(len(YMDHM))*Second
        else:
            Secondn = Second
        YMDHMS = np.hstack((YMDHM,np.transpose([Secondn])))
    
        scanInfo.scanTime = YMDHMS

def calcEffFreq(sampRate, chanFreq, chanAmpPhase, numAp):
    '''
    Calc the effect Freq.

    '''
    
    effFreq = np.zeros(chanAmpPhase.shape[0])
    bw = sampRate/2*1E-6 #MHz
    
    for iob in range(chanAmpPhase.shape[0]):
        if chanFreq.ndim == 1:
            freq = chanFreq + 0.0
        else:
            freq = chanFreq[iob] + 0.0
        rf = np.zeros(len(freq))
        
        for i in range(len(freq)):
            if numAp[iob, i, 0] > 0:
                freq[i] -= bw/2
                rf[i] += chanAmpPhase[iob, i, 0]
            if numAp[iob, i, 1] > 0:
                freq[i] += bw/2
                rf[i] += chanAmpPhase[iob, i, 0]
                
            if freq[i] == 0:
                freq[i] = 1
                rf[i] = 0
            
        sumrf = sum(rf)
        sumrff = sum(rf*freq)
        effFreq[iob] = np.sqrt(-(sumrf*sum(rf*freq**2)-sumrff**2)/(sumrf**2-sumrff*sum(rf/freq)))
            
    return effFreq
    

def write_result(Param, num, scanInfo):    
    """
    Write the obs information to file
    ---------------------
    input: 
        obsInfo        : OBSERVATION class
        session        : session name
        scanInfo       : scan struct
    output:
        file
    ---------------------
    """
    session = Param.Arcs.session[num]
    
    scanNum = scanInfo.scanNum

    fid = open(session+'.out','w')
    fid.writelines('#The station number is: %d\n'%len(scanInfo.stationAll))
    fid.writelines('#The source number is: %d\n'%len(scanInfo.sourceAll))
    fid.writelines('#The scan number is: %d\n'%scanNum)
    #fid.writelines('#The obs number is: %d\n'%sum(scanInfo.obsNum))
    fid.writelines('# Y   M  D  H  M   S   Source         Baseline        GroupDelay\n')
    
    k = 0       
    for i in range(scanNum):
        for j in range(len(scanInfo.scanBl[i])):
            fid.writelines('%4d %2d %2d %2d %2d %4.1f  %8s  %8s  %8s  %15.12f\n'%(scanInfo.scanTime[i,0],scanInfo.scanTime[i,1],\
                                                       scanInfo.scanTime[i,2],scanInfo.scanTime[i,3],\
                                                       scanInfo.scanTime[i,4],scanInfo.scanTime[i,5],\
                                                       scanInfo.scanSource[i],scanInfo.stationAll[scanInfo.scanBl[i][j][0]],\
                                                       scanInfo.stationAll[scanInfo.scanBl[i][j][1]],\
                                                       scanInfo.scanGD[i][j]))
            k += 1
            
    fid.close()
            
    
    
