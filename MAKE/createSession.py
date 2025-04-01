#!/usr/bin/env python3

import netCDF4 as nc
import numpy as np
from COMMON.other import *

def createClockBreak(path, bkFlag, epoch, sta, fileList):
    '''
    Create the ClockBreak.nc file in Session path.

    Parameters
    ----------
    path : str
        the CrossReference path.
    bkFlag : list
        the flag of clock flag.
    epoch : list
        the clock break epoch
    sta : list
        the station neme list
    fileList : list
        the file list in Session path.

    Returns
    -------
    ClockBreak.nc is created.

    '''
    num = sum(bkFlag)
    posit = np.where(bkFlag != 0)

    if len(posit[0]):
        ncFile = ncCreateSamePart(path, 'ClockBreak', fileList)
        
        data = nc.Dataset(ncFile,'w', format='NETCDF4')
        
        data.createDimension('DimUnity', 1)
        data.createDimension('DimX000008', 8)

        if 'DimX%06d' % num not in data.dimensions:
            data.createDimension('DimX%06d' %num, num)
        #data.createDimension('DimX00000'+str(num), num)
        
        data.createVariable('BRK_NUMB', np.int16, ('DimUnity'))
        if num > 1:
            data.createVariable("ClockBreakStationList", 'S1', (('DimX00000'+str(num),'DimX000008')))
        elif num == 1:
            data.createVariable("ClockBreakStationList", 'S1', ('DimX000008'))
        data.createVariable("ClockBreakEpoch", np.float64, ('DimX00000'+str(num)))
        
        if num > 1:
            breakEpoch = []
            k = 0
            for i in posit[0]:
                for j in range(bkFlag[i]):
                    breakEpoch.append(epoch[i][j])
                    data.variables['ClockBreakStationList'][k] = np.char.encode(list(sta[i]))
                    k += 1
        elif num == 1:
            breakEpoch = epoch[posit[0][0]][0]
            data.variables['ClockBreakStationList'][:] = np.char.encode(list(sta[posit[0][0]]))
        
        data.variables['BRK_NUMB'][:] = num
        data.variables['ClockBreakEpoch'][:] = np.array(breakEpoch)
        
        data.close()
        
def createGroupBLWeights(path, staList, reweightInfo, fileList):
    '''
    Create the GroupBLWeights.nc file in Session path.

    Parameters
    ----------
    path : str
        the Session path.
    staList : list
        the all station name list.
    reweightInfo : dict
        the reweight value of earch baseline.
    fileList : list
        the file list of the Session path

    Returns
    -------
    GroupBLWeights.nc is created.

    '''
    
    blNum = len(reweightInfo['Baseline'])
    ncFile = ncCreateSamePart(path, 'GroupBLWeights', fileList)
    data = nc.Dataset(ncFile,'w', format='NETCDF4')
    
    data.createDimension('DimX000002', 2)
    data.createDimension('DimX000008', 8)
    
    if blNum == 1:
        data.createDimension('DimUnity', 1)
        data.createVariable("GroupBLWeightStationList", 'S1', (('DimUnity','DimX000002','DimX000008')))
        data.createVariable("GroupBLWeights", np.float64, (('DimX000002','DimUnity')))
    else:
        data.createDimension('DimX%06d'%blNum, blNum)
        data.createVariable("GroupBLWeightStationList", 'S1', (('DimX%06d'%blNum,'DimX000002','DimX000008')))
        data.createVariable("GroupBLWeights", np.float64, (('DimX000002','DimX%06d'%blNum)))

    data['GroupBLWeights'][:] = np.zeros((2,blNum))
    data['GroupBLWeights'][0] = reweightInfo['Value']

    for i in range(blNum):
        staName_1 = staList[reweightInfo['Baseline'][i][0]-1]
        staName_2 = staList[reweightInfo['Baseline'][i][1] - 1]
        data['GroupBLWeightStationList'][i,0] = np.char.encode(list(staName_1))
        data['GroupBLWeightStationList'][i,1] = np.char.encode(list(staName_2))
        
    data.close()