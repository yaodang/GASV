#!/usr/bin/env python3

from COMMON import *
from INIT.read_vgosDB import *
import numpy as np
import os
from INIT.read_AddInfo import *

def createScanInfo(Param, sessionNum):
    scanInfo = SCAN()
    wrpInfo = WRP()
    wrpInfo.Flag = 4
    scanInfo.sessionName = Param.Arcs.session[sessionNum]
    vgosDBPath = Param.Setup.vgosdbPath
    
    
    readAipsResult(scanInfo, os.path.join(vgosDBPath, scanInfo.sessionName))
    read_nscode(scanInfo, Param)
    
    clkBrk = CLKBRK()
    clkBrk.initBrk(scanInfo.stationAll)
    scanInfo.clkBrk = clkBrk
    scanInfo.souPosit = []
    
    # ------------------------ the reference time set ------------------------#
    if Param.Flags.eopTime == 'NOON':
        scanInfo.refMJD = np.floor(scanInfo.scanMJD[-1]) + 1.5
    elif Param.Flags.eopTime == 'MIDNIGHT':
        scanInfo.refMJD = np.floor(scanInfo.scanMJD[-1])
    else:
        scanInfo.refMJD = np.mean(scanInfo.scanMJD)
        
    refSta = 'KOKEE   '
    if refSta in scanInfo.stationAll:
        scanInfo.refclk = refSta
    else:
        scanInfo.refclk = scanInfo.stationAll[0]
    
    return scanInfo,wrpInfo
        
    
def readAipsResult(scanInfo, fileName):
    # fileName = 'U230619-delay-JL-KS-v1.txt'
    
    obsDate = np.loadtxt(fileName,comments='!',usecols=[0],unpack=True,dtype=str)
    obsSource = np.loadtxt(fileName,comments='!',usecols=[1],unpack=True,dtype=str)
    obsDelay = np.loadtxt(fileName,comments='!',usecols=[6,8],unpack=False,dtype=float)

    scanInfo.stationAll = ['JILIN12 ', 'KASHI12 ']
    scanInfo.scanNum = len(obsDate)
    scanInfo.delayFlag = np.zeros(scanInfo.scanNum, dtype=int)
    '''
    create_Head(scanInfo,obsSource)
    create_Init(scanInfo)
    create_TimeUTC(obsDate, scanInfo)
    create_GroupDelay(scanInfo, obsDelay)
    '''

    #'''
    souAll = sorted(np.unique(obsSource).tolist())
    scanPosit = []
    baseline = []
    Temperature = []
    Press = []
    Humidity = []
    for i in range(scanInfo.scanNum):
        scanPosit.append(i)
        baseline.append(['JILIN12 ', 'KASHI12 '])
        Temperature.append([-999,-999])
        Press.append([-999, -999])
        Humidity.append([-999, -999])

    add_Source(scanInfo, obsSource, souAll, scanPosit)
    add_StationNew(scanInfo, scanPosit, baseline)
    add_TPH(scanInfo, baseline, Temperature, Press, Humidity)
    obsTime = []
    obsDateNew = obsDate.tolist()
    for i in range(len(obsDateNew)):
        temp = obsDateNew[i].replace('-',' ')
        obsTime.append(temp.replace(':',' '))

    add_TimeUTC(obsTime, scanInfo, scanPosit)
    add_GroupDelay(scanInfo, obsDelay*1E9)
    #'''

def create_GroupDelay(scanInfo, obsDelay):
    scanInfo.gd = [obsDelay[:,0]]
    # gdsig = np.zeros(len(obsDelay[:,1]))+0.005/const.c
    scanInfo.gdSig = [np.sqrt(obsDelay[:,1]**2 + (0.005/const.c)**2)]
    # scanInfo.gdSig = [obsDelay[:,1]]
    # scanInfo.gdSig = [gdsig]

def create_Head(scanInfo, source):
    blank = '        '
    scan2Source = np.zeros(scanInfo.scanNum,dtype=int)
    scanSource = []
    Obs2Source = np.zeros(scanInfo.scanNum,dtype=int)
    
    tempSource = np.unique(source).tolist()
    
    for i in range(len(source)):
        tempSou = source[i]+blank[:8-len(source[i])]
        if tempSou not in tempSource:
            index = tempSource.index(source[i])
            tempSource[index] = tempSou
        else:
            index = tempSource.index(tempSou)
            
        scan2Source[i] = index
        Obs2Source[i] = index + 1
        scanSource.append(tempSou)

    scanInfo.sourceAll = tempSource
    scanInfo.scan2Source = scan2Source
    scanInfo.scanSource = scanSource
    scanInfo.Obs2Source = Obs2Source

def create_Init(scanInfo):
    scanInfo.qCode = 9*np.ones(scanInfo.scanNum, dtype=int)
    
    # obs cross
    Scan2Station = np.ones((scanInfo.scanNum,2),dtype=int)
    Station2Scan = np.ones((scanInfo.scanNum,2),dtype=int)
    Obs2Baseline = np.zeros((scanInfo.scanNum,2),dtype=int)
    for i in range(scanInfo.scanNum):
        Scan2Station[i] = Scan2Station[i]*(i + 1)
        Station2Scan[i] = Station2Scan[i]*i
        Obs2Baseline[i,0] = 1
        Obs2Baseline[i,1] = 2
        
        
    scanInfo.Scan2Station = Scan2Station
    scanInfo.Station2Scan = Station2Scan
    scanInfo.Obs2Baseline = Obs2Baseline
    scanInfo.Obs2Scan = np.linspace(1, scanInfo.scanNum, scanInfo.scanNum, dtype=int)
    
    # cable and met
    cableCal = []
    T = []
    P = []
    H = []
    
    for i in range(len(scanInfo.stationAll)):
        temp = np.where(scanInfo.Scan2Station[:,i] != 0)
        NumStatScan = scanInfo.Scan2Station[temp[0][-1],i]
        cableCal.append(np.zeros(NumStatScan))
        T.append(-999*np.ones(NumStatScan))
        P.append(-999*np.ones(NumStatScan))
        H.append(-999*np.ones(NumStatScan))
        
    scanInfo.cableCal = cableCal
    scanInfo.T = T
    scanInfo.P = P
    scanInfo.H = H
    
    scanInfo.baseInfo = [['X']]
    
def create_TimeUTC(date, scanInfo):
    YMDHMS = np.zeros((len(date),6))
    MJD = np.zeros(len(date))
    
    for i in range(len(date)):
        year = int(date[i][0:4])
        mon = int(date[i][5:7])
        day = int(date[i][8:10])
        hour = int(date[i][11:13])
        minute = int(date[i][14:16])
        seconds = float(date[i][17:27])
        
        MJD[i] = modjuldat(np.array([year]),np.array([mon]),np.array([day]),\
                           hour,minute,seconds)
        
        YMDHMS[i,0] = year
        YMDHMS[i,1] = mon
        YMDHMS[i,2] = day
        YMDHMS[i,3] = hour
        YMDHMS[i,4] = minute
        YMDHMS[i,5] = seconds
        
    scanInfo.scanTime = YMDHMS
    scanInfo.scanMJD = MJD
    scanInfo.Obs2MJD = MJD
    
# fileName = '../U230619-delay-JL-KS-v1.txt'
# readAipsResult(fileName)
    