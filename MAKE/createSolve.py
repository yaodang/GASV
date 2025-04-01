#!/usr/bin/env python3

import netCDF4 as nc
import numpy as np
import os
from COMMON.other import *

def createBaselineClockSetup(path, staAll, baselineClock, fileList):
    '''
    Create the BaselineClockSetup.nc file in Solve dir.

    '''
    if len(baselineClock):
        ncFile = ncCreateSamePart(path, 'BaselineClockSetup', fileList)
        blNum = len(baselineClock)
        data = nc.Dataset(ncFile,'w',format='NETCDF4')
        
        data.createDimension('DimX000002', 2)
        data.createDimension('DimX000008', 8)
        if blNum != 2:
            if 'DimX%06d' % blNum not in data.dimensions:
                data.createDimension('DimX%06d'%blNum, blNum)
            
        data.createVariable("BaselineClock", 'S1', ('DimX%06d'%blNum,\
                                                    "DimX000002",\
                                                    "DimX000008"))
        for i in range(blNum):
            sta1 = staAll[baselineClock[i][0]-1]
            sta2 = staAll[baselineClock[i][1]-1]
            data.variables['BaselineClock'][i,0] = np.char.encode(list(sta1))
            data.variables['BaselineClock'][i,1] = np.char.encode(list(sta2))
            
        data.close()
    

def createClockSetup(path, refClkName, fileList):
    '''
    Create the ClockSetup.nc file in Solve dir.

    '''
    ncFile = ncCreateSamePart(path, 'ClockSetup', fileList)
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    data.createDimension('DimX000008', 8)
    data.createVariable("ReferenceClock", 'S1', ("DimX000008"))
    data.variables['ReferenceClock'][:] = np.char.encode(list(refClkName))
    
    data.close()
    
def createScanTimeMJD(path, scanTime):
    '''
    Create the ScanTimeMJD.nc file in Solve dir.

    Parameters
    ----------
    path : str
        The Solve path.
    scanTime : list
        the scan time.

    Returns
    -------
    The ScanTimeMJD.nc is created.

    '''

    ncFile = path+'/ScanTimeMJD.nc'
    makeFile(ncFile)
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')   
    
    data.createDimension('NumScans', len(scanTime))
    data.createVariable("DayFrac", np.float64, ("NumScans"))

    time = np.array(scanTime)
    DayFrac = time[:,-1]-np.floor(time[:,-1])
    data.variables['DayFrac'][:] = DayFrac
    
    MJD = []
    for i in range(len(scanTime)):
        MJD.append(int(scanTime[i][-1]))
    
    diff = np.diff(np.array(MJD))
    flag = np.where(diff==1)
    if len(flag[0]):
        data.createVariable("MJD", np.int32, ("NumScans"))
        data.variables['MJD'][:] = np.array(MJD)
    else:
        data.createDimension('DimX000001', 1)
        data.createVariable("MJD", np.int32, ("DimX000001"))
        data.variables['MJD'][:] = MJD[0]
        
    data.close()