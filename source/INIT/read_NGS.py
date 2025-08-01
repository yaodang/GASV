#!/usr/bin/env python3
import sys
from INIT.read_vgosDB import *
from INIT.read_AddInfo import *
import numpy as np

def ngsScanInfo(Param, sessionNum):
    scanInfo = SCAN()
    wrpInfo = WRP()
    wrpInfo.Flag = 4
    scanInfo.sessionName = Param.Arcs.session[sessionNum]
    vgosDBPath = Param.Setup.vgosdbPath

    readNGSResult(scanInfo, os.path.join(vgosDBPath, scanInfo.sessionName))
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

    return scanInfo, wrpInfo

#def readNGSResult(scanInfo, fileName):
def readNGSResult(scanInfo, fileName):

    fid = open(fileName,'r')
    lines = fid.readlines()
    fid.close()

    souAll,startPosit = getSource(lines)
    getStaScanDelay(scanInfo, lines, startPosit, souAll)

def getSource(lines):
    posit = []
    for i in range(len(lines)):
        if '$END' in lines[i]:
            posit.append(i)
        if len(posit) == 3:
            break

    if len(posit) == 3:
        source = []
        for i in range(posit[0]+1,posit[1]):
            source.append(lines[i][:8])

        return source,posit[2]+1
    else:
        print('The NGS format is wrong!')
        sys.exit()

def  getStaScanDelay(scanInfo, lines, num, souAll):
    station = []
    obsTime = []
    baseline = []
    obsDelay = []
    obsSou = []
    Temperature = []
    Press = []
    Humidity = []

    blockNum = 9
    obsNum = int((len(lines)-num)/blockNum)
    for i in range(obsNum):
        firstLine = lines[num + blockNum * i]
        secondLine = lines[num + blockNum * i + 1]
        sixLine = lines[num + blockNum * i + 5]

        sta1 = firstLine[:8]
        sta2 = firstLine[10:18]
        if sta1 not in station:
            station.append(sta1)
        if sta2 not in station:
            station.append(sta2)

        baseline.append([sta1,sta2])
        temp = list(filter(None,sixLine.split(" ")))
        Temperature.append([float(temp[0]),float(temp[1])])
        Press.append([float(temp[2]),float(temp[3])])
        Humidity.append([float(temp[4])/100,float(temp[5])/100])
        obsSou.append(firstLine[20:28])
        obsTime.append(firstLine[29:60])
        obsDelay.append([float(secondLine[:20]),float(secondLine[20:30])])

    scanInfo.stationAll = sorted(station)
    scanInfo.delayFlag = np.zeros(len(obsTime), dtype=int)

    scanPosit = get_scanTime(scanInfo, obsTime)

    create_Head(scanInfo, obsSou, souAll, scanPosit)
    create_Init(scanInfo, scanPosit, baseline, Temperature, Press, Humidity)
    create_TimeUTC(obsTime, scanInfo, scanPosit)
    create_GroupDelay(scanInfo, np.array(obsDelay))

    #add_Source(scanInfo, obsSou, souAll, scanPosit)
    #add_Station(scanInfo, scanPosit, baseline)
    #add_TPH(scanInfo, baseline, Temperature, Press, Humidity)
    #add_TimeUTC(obsTime, scanInfo, scanPosit)
    #add_GroupDelay(scanInfo, np.array(obsDelay))

def create_Head(scanInfo, obsSou, souAll, scanPosit):
    blank = '        '
    scan2Source = np.zeros(scanInfo.scanNum, dtype=int)
    scanSource = []
    Obs2Source = np.zeros(len(obsSou), dtype=int)

    #tempSource = np.unique(source).tolist()

    for i in range(len(obsSou)):
        index = souAll.index(obsSou[i])
        Obs2Source[i] = index + 1

    k = 0
    for posit in scanPosit:
        sou = obsSou[posit]
        index = souAll.index(sou)
        scan2Source[k] = index
        scanSource.append(sou)
        k = k + 1

    scanInfo.sourceAll = souAll
    scanInfo.scan2Source = scan2Source
    scanInfo.scanSource = scanSource
    scanInfo.Obs2Source = Obs2Source

def create_GroupDelay(scanInfo, obsDelay):
    scanInfo.gd = [obsDelay[:, 0]*1E-9]
    # gdsig = np.zeros(len(obsDelay[:,1]))+0.005/const.c
    scanInfo.gdSig = [np.sqrt(obsDelay[:, 1]*1E-9 ** 2 + (0.005 / const.c) ** 2)]
    # scanInfo.gdSig = [obsDelay[:,1]]
    # scanInfo.gdSig = [gdsig]

def create_Init(scanInfo, scanPosit, baseline, Temperature, Press, Humidity):
    staNum = len(scanInfo.stationAll)
    obsNum = len(scanInfo.Obs2Source)

    scanInfo.qCode = 9 * np.ones(len(scanInfo.Obs2Source), dtype=int)

    # obs cross
    Scan2Station = np.zeros((scanInfo.scanNum, staNum), dtype=int)
    Obs2Baseline = np.zeros((obsNum, 2), dtype=int)
    Obs2Scan = np.zeros(obsNum,dtype=int)
    if staNum > 2:
        for i in range(obsNum):
            index1 = scanInfo.stationAll.index(baseline[i][0])+1
            index2 = scanInfo.stationAll.index(baseline[i][1])+1
            Obs2Baseline[i, 0] = index1
            Obs2Baseline[i, 1] = index2
    else:
        Station2Scan = np.zeros((scanInfo.scanNum, staNum), dtype=int)

    for i in range(scanInfo.scanNum):
        if staNum == 2:
            Scan2Station[i] = Scan2Station[i] * (i + 1)
            Station2Scan[i] = Station2Scan[i] * i
            Obs2Baseline[i, 0] = 1
            Obs2Baseline[i, 1] = 2
        else:
            staList = []
            if i != scanInfo.scanNum - 1:
                for j in range(scanPosit[i],scanPosit[i+1]):
                    staList.extend(baseline[j])
                    Obs2Scan[j] = i + 1
            else:
                for j in range(scanPosit[i],obsNum):
                    staList.extend(baseline[j])
                    Obs2Scan[j] = i + 1

            staListNew = list(set(staList))
            for s in range(len(staListNew)):
                index = scanInfo.stationAll.index(staListNew[s])
                maxObs2Sta = max(Scan2Station[:,index])
                Scan2Station[i,index] = maxObs2Sta + 1

    rows = max(Scan2Station[-1,:])
    if staNum > 2:
        Station2Scan = np.zeros((rows, staNum), dtype=int)
        for i in range(staNum):
            posit = np.where(Scan2Station[:,i]!=0)[0]
            #Station2Scan[:len(posit),i] =Station2Scan[:len(posit),i]+ posit + 1
            for j in range(len(posit)):
                Station2Scan[j, i] = posit[j] + 1

    scanInfo.Scan2Station = Scan2Station
    scanInfo.Station2Scan = Station2Scan
    scanInfo.Obs2Baseline = Obs2Baseline
    scanInfo.Obs2Scan = Obs2Scan

    # cable and met
    cableCal = []
    T = []
    P = []
    H = []

    for i in range(staNum):
        T.append([])
        P.append([])
        H.append([])
        temp = np.where(scanInfo.Scan2Station[:, i] != 0)
        cableCal.append(np.zeros(len(temp[0])))

    for i in range(obsNum):
        index1 = scanInfo.stationAll.index(baseline[i][0])
        index2 = scanInfo.stationAll.index(baseline[i][1])
        T[index1].append(Temperature[i][0])
        T[index2].append(Temperature[i][1])
        P[index1].append(Press[i][0])
        P[index2].append(Press[i][1])
        H[index1].append(Humidity[i][0])
        H[index2].append(Humidity[i][1])

    for i in range(staNum):
        T[i] = np.array(T[i])
        P[i] = np.array(P[i])
        H[i] = np.array(H[i])

    #for i in range(staNum):
    #    temp = np.where(scanInfo.Scan2Station[:, i] != 0)
    #    NumStatScan = scanInfo.Scan2Station[temp[0][-1], i]
    #    cableCal.append(np.zeros(NumStatScan))
    #    T.append(-999 * np.ones(NumStatScan))
    #    P.append(-999 * np.ones(NumStatScan))
    #    H.append(-999 * np.ones(NumStatScan))

    scanInfo.cableCal = cableCal
    scanInfo.T = T
    scanInfo.P = P
    scanInfo.H = H

    scanInfo.baseInfo = [['X']]

def create_TimeUTC(date, scanInfo, scanPosit):
    YMDHMS = np.zeros((len(date), 6))
    MJD = np.zeros(len(date))

    for i in range(len(date)):
        temp = list(filter(None,date[i].split(" ")))
        year = int(temp[0])
        mon = int(temp[1])
        day = int(temp[2])
        hour = int(temp[3])
        minute = int(temp[4])
        seconds = float(temp[5])

        MJD[i] = modjuldat(np.array([year]), np.array([mon]), np.array([day]), \
                           hour, minute, seconds)

        YMDHMS[i, 0] = year
        YMDHMS[i, 1] = mon
        YMDHMS[i, 2] = day
        YMDHMS[i, 3] = hour
        YMDHMS[i, 4] = minute
        YMDHMS[i, 5] = seconds

    scanInfo.scanTime = YMDHMS[np.array(scanPosit),:]
    scanInfo.scanMJD = MJD[np.array(scanPosit)]
    scanInfo.Obs2MJD = MJD

def get_scanTime(scanInfo, obsTime):
    obsDate = sorted(list(set(obsTime)))
    scanInfo.scanNum = len(obsDate)

    scanPosit = []
    for date in obsDate:
        index = obsTime.index(date)
        scanPosit.append(index)

    return scanPosit
#def getScanNum(scanTime):

#fileName = '24SEP17RN_V004'
#readNGSResult(fileName)