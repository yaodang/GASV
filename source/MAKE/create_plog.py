#!/usr/bin/env python3

import netCDF4 as nc
import numpy as np
import os

from MAKE.createStation import *
from MAKE.createRoot import *
from COMMON import *
from scipy import interpolate

def pLog(logPath, fileType, vgosDBPath):
    '''
    Read the station log file, write the Met.nc and Cal-Cable.nc file. 
    the path should be like:
        logPath/vgosDBPath/sessionXX.log

    Parameters
    ----------
    logPath : str
        the station log path.
    fileType : str
        the read file type.
    vgosDBPath : str
        the vgosDB path.

    Returns
    -------
    Met.nc and Cab-Cal.nc is created.

    '''
    
    print('\n--------------- Met and Cable data create ---------------\n')
    
    data = nc.Dataset(os.path.join(dbInfo['outPath'],'Head.nc'))
    session = ''.join(np.char.decode(data['Session'][:].data))
    staNum = data['NumStation'][:].data[0]
    stationList = data['StationList'][:].data
    
    data = nc.Dataset(os.path.join(dbInfo['outPath'],'Solve/ScanTimeMJD.nc'))
    scanMJD = data['MJD'][:].data + data['DayFrac'][:].data
    
    data = nc.Dataset(os.path.join(dbInfo['outPath'],'CrossReference/StationCrossRef.nc'))
    Scan2Station = data['Scan2Station'][:].data
    
    staAll = []
    for i in range(staNum):
        staAll.append(''.join(np.char.decode(stationList[i,:])))
    
    fileFlag = np.zeros(staNum)
    
    for root,dirs,files in os.walk(os.path.join(dbInfo['inPath'],session)):
        for file in files:
            if dbInfo['type'] == file[-3:]:
                sta,metMJD,metVal,cabMJD,cabVal,clkMJD,clkVal,flag = readStaLog(os.path.join(root, file))
                if sta in staAll:
                    ista = staAll.index(sta)
                    fileFlag[ista] = 1
                    index = np.where(Scan2Station[:,ista] > 0)
                    staMJD = scanMJD[index[0]]
                    
                    if sum(flag) == 0:
                        print('    Writing the Met and Cable of %s...'%(sta))
                    if flag[0] == 1 and flag[1] == 0:
                        print('    Writing the Met(zero) and Cable of %s...'%(sta))
                    if flag[0] == 0 and flag[1] == 1:
                        print('    Writing the Met and Cable(zero) of %s...'%(sta))
                    if sum(flag) == 2:
                        print('    Writing the Met(zero) and Cable(zero) of %s...'%(sta))
                    
                    T,P,H,CC = interpValue(staMJD, metMJD, metVal, cabMJD, cabVal)
                    if len(clkVal):
                        Clk = [np.array(clkMJD), np.array(clkVal)]
                    else:
                        Clk = [scanMJD,np.zeros(len(scanMJD))]
                    staPath = os.path.join(dbInfo['outPath'], sta.strip())
                    if not os.path.exists(staPath):
                        os.system('mkdir '+staPath)
                    createMet(staPath, T, P, H, sta)
                    createCalCab(staPath, CC, sta)
                    createClk(staPath, Clk, sta)
                    
    noFile = np.where(fileFlag==0)
    if len(noFile[0]):
        T = -999*np.ones(len(index[0]))
        P = -999*np.ones(len(index[0]))
        H = -999*np.ones(len(index[0]))
        CC = np.zeros(len(index[0]))
        Clk = [scanMJD,np.zeros(len(scanMJD))]
        
        for ista in noFile[0]:
            print('    Writing the Met(zero), Cable(zero) and Clock(zero) of %s...'%(staAll[ista]))
            index = np.where(Scan2Station[:,ista] > 0)
            
            staPath = os.path.join(dbInfo['outPath'], staAll[ista].strip())
            if not os.path.exists(staPath):
                os.system('mkdir '+staPath)
            createMet(staPath, T, P, H, staAll[ista])
            createCalCab(staPath, CC, staAll[ista])
            createClk(staPath, Clk, staAll[ista])
    
    createWrpFile(dbInfo['outPath'], staAll, 1)
                                        
def readStaLog(staLogFile):
    '''
    Read the station log file.

    Parameters
    ----------
    staLogFile : str
        the station log file path.

    Returns
    -------
    station : str
        station name.
    metMJD : list
        the met MJD in log file.
    metVal : list
        the T,P,H value.
    calMJD : list
        the cable MJD in log file.
    calVal : list
        the cable value.
    zeroFlag : list
        the zero flag for met or cable

    '''
    
    fid = open(staLogFile,'rb')
    lines = fid.readlines()
    fid.close()
    
    metLine = []
    cabcalLine = []
    clockLine = []
    station = ''
    zeroFlag = [0, 0, 0]
    
    staFlag = 0
    for line in lines:
        try:
            nline = line.decode('UTF-8')
        except UnicodeDecodeError:
            continue
        
        if '/wx/' in nline:
            metLine.append(nline)
            
        if '/cable/' in nline:
            cabcalLine.append(nline)
        
        if 'fmout-gps/' in nline or 'gps-fmout/' in nline or 'fmout-BD/' in nline:
            clockLine.append(nline)
            
        if ('AZEL' in nline or 'HADC' in nline) and 'antenna' not in nline and staFlag == 0:
            temp = list(filter(None,nline[24:].split(" ")))
            blank = '        '
            station = temp[0] + blank[:8-len(temp[0])]
            staFlag = 1
    
    
    if len(metLine) > 0:
        metMJD,metVal = getLogValue(metLine, 'met')
    else:
        metMJD = []
        metVal = []
        zeroFlag[0] = 1

    if len(cabcalLine) > 0:
        calMJD,calVal = getLogValue(cabcalLine, 'cabcal')
    else:
        calMJD = []
        calVal = []
        zeroFlag[1] = 1
        
    if len(clockLine) > 0:
        clkMJD,clkVal = getLogValue(clockLine, 'clock')
    else:
        clkMJD = []
        clkVal = []
        zeroFlag[2] = 1
    
    return station, metMJD, metVal, calMJD, calVal, clkMJD, clkVal, zeroFlag

def interpValue(staMJD, metMJD, metVal,calMJD,calVal):
    '''
    Interpolation the log value to the observe time.

    Parameters
    ----------
    staMJD : array
        the observe MJD.
    metMJD : list
        the met MJD in log file.
    metVal : list
        the T,P,H value.
    calMJD : list
        the cable MJD in log file.
    calVal : list
        the cable value.

    Returns
    -------
    obsT : array
        temperature.
    obsP : array
        pressure.
    obsH : array
        DESCRIPTION.
    obsCabC : array
        cabel correct.

    '''
    
    if len(metVal):
        Value = np.array(metVal)
        MJD = np.array(metMJD)
        
        obsT = checkAndInterp(MJD, staMJD, Value[:,0])
        obsP = checkAndInterp(MJD, staMJD, Value[:,1])
        obsH = checkAndInterp(MJD, staMJD, Value[:,2])
        
    else:
        obsT = -999*np.ones(len(staMJD))
        obsP = -999*np.ones(len(staMJD))
        obsH = -999*np.ones(len(staMJD))
        
    if len(calVal):
        calArray = np.array(calVal)
        calMJDArray = np.array(calMJD)
        rms = np.sqrt(np.sum(calArray**2)/len(calArray))
        outPosit = np.where(calArray < 3*rms)
        
        
        calValNew = calArray[outPosit] - np.mean(calArray[outPosit])
        obsCabC = checkAndInterp(calMJDArray[outPosit], staMJD, calValNew)
    else:
        obsCabC = np.zeros(len(staMJD))
        
    return obsT, obsP, obsH, obsCabC

def checkAndInterp(logMJD, staMJD, Value):
    
    obsValue = np.zeros(len(staMJD))
    
    existsValue = np.where(Value != -999)[0]
    
    if len(existsValue) < 5:
        return -999*np.ones(len(staMJD))
    
    func = interpolate.splrep(logMJD[existsValue],Value[existsValue])
    
    startMJD = logMJD[existsValue[0]]
    stopMJD = logMJD[existsValue[-1]]
    
    findStart = np.where(staMJD >= startMJD)[0]
    findStop = np.where(staMJD <= stopMJD)[0]
    
    obsValue[findStart[0]:findStop[-1]] = interpolate.splev(staMJD[findStart[0]:findStop[-1]], func, der=0)
    
    
    obsValue[:findStart[0]] = obsValue[findStart[0]]
    obsValue[findStop[-1]:] =  obsValue[findStop[-1]-1]
    
    return obsValue    

def getLogValue(line, choice):
    '''
    Pick the MJD and value from line.

    Parameters
    ----------
    line : list
        the line cotain the met or cable value.
    choice : str
        met or cabcal.

    Returns
    -------
    MJD : list
        MJD.
    Val : list
        met or cable value.

    '''
    
    scale = 4.0E5
    MJD = []
    Val = []
    
    for i in range(len(line)):
        year = int(line[i][0:4])
        doy = int(line[i][5:8])
        mon,day = doy2day(doy, year)
        
        hour = int(line[i][9:11])
        mi = int(line[i][12:14])
        sec = float(line[i][15:20])
        mjd = modjuldat(np.array([year]),np.array([mon]),np.array([day]),hour,mi,sec)
        
        
        if choice == 'met':
            index = line[i].index('wx/')
            temp = list(filter(None,line[i][index+3:].split(",")))
            
            if len(temp) == 1 and len(temp[0]) > 10:
                temp = [-999,-999,-999]
            else:
                try:
                    float(temp[0])
                except ValueError:
                    temp[0] = '-999'
                    
                try:
                    float(temp[1])
                except ValueError:
                    temp[1] = '-999'
                    
                try:
                    float(temp[2])
                except ValueError:
                    temp[2] = '-999'
                
            Val.append([float(temp[0]),float(temp[1]),float(temp[2])])
            MJD.append(mjd[0].tolist())

        elif choice == 'cabcal':
            index = line[i].index('cable/')
            temp = float(line[i][index+6:-1])
            Val.append(temp/scale)
            MJD.append(mjd[0].tolist())
            
        elif choice == 'clock':
            index = -1
            clkOffsetType = ['fmout-BD','fmout-gps']
            for offType in clkOffsetType:
                if offType in line[i]:
                    index = line[i].index(offType)
                    typeLen = len(offType)
            
            if index != -1:
                try:
                    index2 = line[i].index(',')
                    temp = float(line[i][index+typeLen+1:index2])
                except ValueError:
                    temp = float(line[i][index+typeLen+1:-1])
                if abs(temp) != 1:
                    Val.append(temp)
                    MJD.append(mjd[0].tolist())
            
    return MJD, Val    
    