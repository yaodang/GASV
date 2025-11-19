#!/usr/bin/env python3


import netCDF4 as nc
import numpy as np
import os
from COMMON.other import makeFile

def createObsCrossRef(path, scanBL, staAll):
    '''
    Create the ObsCrossRef.nc file in CrossReference path.

    Parameters
    ----------
    path : str
        the CrossReference path.
    scanBL : list
        the baseline of earch scan.
    staAll : list
        the all observed station.

    Returns
    -------
    Obs2Scan: array
        the observe num of earch scan
    blSort: list
        the new index baseline of earch scan
    ObsCrossRef.nc is created.

    '''
    
    ncFile = path+'/ObsCrossRef.nc'
    makeFile(ncFile)
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    
    Obs2Scan = []
    Obs2Baseline = []
    blSort = []
    
    flag = 1
    if len(staAll) == 2:
        flag = 0
    
    for iscan in range(len(scanBL)):
        blNum = len(scanBL[iscan])
        temp = np.ones(blNum,dtype=int)*(iscan+1)
        Obs2Scan.extend(temp.tolist())
        
        if flag == 1:
            blIndex = np.argsort(np.array(scanBL[iscan])[:,0])
            
            bl = []
            for ibl in range(blNum):
                nibl = blIndex[ibl]
                
                temp = []
                for ista in scanBL[iscan][nibl]:
                    index = staAll.index(ista) + 1
                    temp.append(index)
                bl.append(temp)
                
            newBlIndex, newBlList = reSortScanBl(blIndex, bl)
            Obs2Baseline.extend(newBlList)
            blSort.append(newBlIndex)
        elif flag == 0:
            Obs2Baseline = [1,2]
            flag = 3
            
            
        # if flag == 1:
        #     blIndex = np.argsort(np.array(scanBL[iscan])[:,0])
        #     for ibl in range(blNum):
        #         nibl = blIndex[ibl]
                
        #         bl = []
        #         for ista in scanBL[iscan][nibl]:
        #             index = staAll.index(ista) + 1
        #             bl.append(index)
        #         Obs2Baseline.append(bl)
        #     blSort.append(blIndex)
        # elif flag == 0:
        #     Obs2Baseline = [1,2]
        #     flag = 3
                        
    data.createDimension('NumObs', len(Obs2Scan))
    data.createDimension('DimX000002',2)
            
    data.createVariable("Obs2Scan", np.int32, ("NumObs"))
    if flag == 1:
        data.createVariable("Obs2Baseline", np.int16, ("NumObs",'DimX000002'))
    elif flag == 3:
        data.createVariable("Obs2Baseline", np.int16, ('DimX000002'))
    
    data.variables['Obs2Scan'][:] = np.array(Obs2Scan)
    data.variables['Obs2Baseline'][:] = np.array(Obs2Baseline)
    
    data.close()
    
    return np.array(Obs2Scan), blSort
    
def createSourceCrossRef(path, sou):
    '''
    Create the SourceCrossRef.nc in CrossReference path

    Parameters
    ----------
    path : str
        the CrossReference path.
    sou : list
        the source name of earch scan.

    Returns
    -------
    The SourceCrossRef.nc is created.
    sortSou : array
        the all observe source.
    
    '''
    
    ncFile = path+'/SourceCrossRef.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    
    sortSou = np.sort(np.unique(sou))
    
    numSou = len(sortSou)
    numScan = len(sou)
    
    data.createDimension('NumSource', numSou)
    data.createDimension('NumScans', numScan)
    data.createDimension('DimX000008',8)
    
    data.createVariable("CrossRefSourceList", 'S1', ("NumSource",'DimX000008'))
    data.createVariable("Scan2Source", np.int32, ("NumScans"))
    
    Scan2Sou = np.zeros(numScan, dtype=int)
    for i in range(numSou):
        posit = np.where(sou == sortSou[i])
        Scan2Sou[posit[0]] = i + 1
        data.variables['CrossRefSourceList'][i] = np.char.encode(list(sortSou[i]))
    
    data.variables['Scan2Source'][:] = Scan2Sou
    
    data.close()
    
    return sortSou, Scan2Sou
    
def createStationCrossRef(path, scanSta, numScan):
    '''
    Create the StationCrossRef file in CrossReference path.

    Parameters
    ----------
    path : str
        the CrossReference path.
    scanSta : list
        the station of earch scan.
    numScan : int
        Tthe number of scan.

    Returns
    -------
    StationCrossRef.nc is created.

    '''
    
    ncFile = path+'/StationCrossRef.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    
    staAll = scanSta[0]
    staObs = np.ones(len(scanSta[0]),dtype=int).tolist()
    scanNum = []
    for i in range(len(scanSta[0])):
        scanNum.append([0])
    
    for iscan in range(1,numScan):
        for sta in scanSta[iscan]:
            if sta not in staAll:
                staAll.append(sta)
                staObs.append(1)
                scanNum.append([iscan])
            else:
                temp = staAll.index(sta)
                staObs[temp] += 1
                scanNum[temp].append(iscan)
    
    sortIndex = np.argsort(staAll)
    numSta = len(sortIndex)
    
    maxObs = max(staObs)
    zeros = '000000'
    DimX = 'DimX'+zeros[6-len(str(maxObs))]+str(maxObs)
    data.createDimension('NumStation', numSta)
    data.createDimension('NumScans', numScan)
    data.createDimension(DimX,maxObs)
    data.createDimension('DimX000008',8)
    
    data.createVariable("CrossRefStationList", 'S1', ('NumStation','DimX000008'))
    data.createVariable("Station2Scan", np.int32, (DimX,'NumStation'))
    data.createVariable("Scan2Station", np.int32, ("NumScans",'NumStation'))
    
    Station2Scan = np.zeros((max(staObs), numSta),dtype=int)
    Scan2Station = np.zeros((numScan, numSta), dtype=int)
    
    for ista in range(numSta):
        nista = sortIndex[ista]
        obsNum = np.linspace(1, staObs[nista], staObs[nista], dtype=int)
        Scan2Station[scanNum[nista],ista] = obsNum
        Station2Scan[:staObs[nista],ista] = np.array(scanNum[nista], dtype=int) + 1
        data.variables['CrossRefStationList'][ista] = np.char.encode(list(staAll[nista]))
        
    data.variables['Station2Scan'][:] = Station2Scan
    data.variables['Scan2Station'][:] = Scan2Station
    
    data.close()
    
    return np.array(staAll)[sortIndex].tolist(),Scan2Station

def reSortScanBl(blIndex, blList):
    '''
    blList = [[1,4]
              [1,3]
              [3,4]]
    
    sorted to
    newBlList = [[1,3]
                 [1,4]
                 [3,4]]
    

    '''
    newBlIndex = blIndex + 0
    
    blArray = np.array(blList)
    staList = np.unique(blArray)
    
    newBlList = blArray + 0
    for i in range(len(staList)-1):
        staSub = blArray[:,0] - staList[i]
        containBl = np.where(staSub==0)[0]
        
        if len(containBl) > 1:
            secondSort = np.argsort(blArray[containBl,1])
            newBlIndex[containBl] = blIndex[secondSort+containBl[0]]
            newBlList[containBl] = blArray[secondSort+containBl[0]]
        
    return newBlIndex, newBlList.tolist()
    
    