import numpy as np
from COMMON import *

def add_GroupDelay(scanInfo, obsDelay):
    '''
    Add the group delay and its sigma to scanInfo class.

    input:
        scanInfo: class
        obsDelay: array, [nobs,2], first column is delay, second column is sigma.
    '''

    scanInfo.gd = [obsDelay[:, 0]*1E-9]
    # gdsig = np.zeros(len(obsDelay[:,1]))+0.005/const.c
    scanInfo.gdSig = [(np.sqrt((obsDelay[:, 1]*1E-9) ** 2 + (0.005 / const.c) ** 2))]
    # scanInfo.gdSig = [obsDelay[:,1]]
    # scanInfo.gdSig = [gdsig]

def add_Source(scanInfo, obsSou, souAll, scanPosit):
    '''
    Add source information to scanInfo.

    input:
        scanInfo: class
        obsSou: list, observe source for each obs
                like: ['0202+319','0202+319','NRAO150 ','NRAO150 ','3C418   ',...]
        souAll: list, the unique source in all session
                like: ['0202+319','NRAO150 ','3C418   ',...]
        scanPosit: list, the scan posit in obs
                like: single baseline ([0,1,2,3,4,...])
                      muti-baseline ([0,2,4,7,...])
    '''

    blank = '        '
    scan2Source = np.zeros(scanInfo.scanNum, dtype=int)
    scanSource = []
    Obs2Source = np.zeros(len(obsSou), dtype=int)

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

def add_StationNew(scanInfo, scanPosit, baseline):
    '''
    Add the station information to scanInfo.

    input:
        scanInfo: class
        scanPosit: list, [nscan,1], the scan posit in obs
        baseline: list, [nobs,2], the baseline string of earch obs
            like: [['KOKEE   ','WETTZELL'], ['KOKEE    ','NYALE13S'], ...]
    '''

    staNum = len(scanInfo.stationAll)
    obsNum = len(scanInfo.Obs2Source)

    scanInfo.qCode = 9 * np.ones(len(scanInfo.Obs2Source), dtype=int)

    # obs cross
    Obs2Baseline = np.zeros((obsNum, 2), dtype=int)
    for i in range(obsNum):
        index1 = scanInfo.stationAll.index(baseline[i][0])+1
        index2 = scanInfo.stationAll.index(baseline[i][1])+1
        Obs2Baseline[i, 0] = index1
        Obs2Baseline[i, 1] = index2

    Scan2Station = np.zeros((scanInfo.scanNum, staNum), dtype=int)
    Obs2Scan = np.zeros(obsNum, dtype=int)
    for i in range(scanInfo.scanNum):
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

def add_Station(scanInfo, scanPosit, baseline):
    '''
    Add the station information to scanInfo.

    input:
        scanInfo: class
        scanPosit: list, [nscan,1], the scan posit in obs
        baseline: list, [nobs,2], the baseline string of earch obs
            like: [['KOKEE   ','WETTZELL'], ['KOKEE    ','NYALE13S'], ...]
    '''

    staNum = len(scanInfo.stationAll)
    obsNum = len(scanInfo.Obs2Source)

    scanInfo.qCode = 9 * np.ones(len(scanInfo.Obs2Source), dtype=int)

    # obs cross
    Obs2Baseline = np.zeros((obsNum, 2), dtype=int)
    if staNum > 2:
        Scan2Station = np.zeros((scanInfo.scanNum, staNum), dtype=int)
        Obs2Scan = np.zeros(obsNum, dtype=int)
        for i in range(obsNum):
            index1 = scanInfo.stationAll.index(baseline[i][0])+1
            index2 = scanInfo.stationAll.index(baseline[i][1])+1
            Obs2Baseline[i, 0] = index1
            Obs2Baseline[i, 1] = index2
    else:
        Scan2Station = np.ones((scanInfo.scanNum, 2), dtype=int)
        Station2Scan = np.ones((scanInfo.scanNum, staNum), dtype=int)
        Obs2Scan = np.linspace(1,scanInfo.scanNum,scanInfo.scanNum,dtype=int)

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

def add_TPH(scanInfo,baseline,Temperature,Press,Humidity):
    '''
    Add weather information to scanInfo.

    input:
        scanInfo: class
        baseline: list, [nobs, 2], the baseline string of earch obs
        Temperature: list, [nobs,2], the temperature of earch obs
        Press: list, [nobs,2], the temperature of earch obs
        Humidity: list, [nobs,2], the temperature of earch obs
    '''

    staNum = len(scanInfo.stationAll)
    obsNum = len(scanInfo.Obs2Source)

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

    scanInfo.cableCal = cableCal
    scanInfo.T = T
    scanInfo.P = P
    scanInfo.H = H

    scanInfo.baseInfo = [['X']]

def add_TimeUTC(date, scanInfo, scanPosit):
    '''
    Add time information to scanInfo.

    input:
        date: list, the string of date of each obs
        scanInfo: class
        scanPosit: list, the scan posit in obs
    '''

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