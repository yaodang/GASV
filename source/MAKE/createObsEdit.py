#!/usr/bin/env python3

import os
import netCDF4 as nc
import numpy as np
from COMMON.other import *


def createEdit(path, delayFlag, fileList):
    '''
    Create the Edit.nc file in ObsEdit dir.

    '''
    if len(delayFlag):
        ncFile = ncCreateSamePart(path, 'Edit', fileList)
        
        data = nc.Dataset(ncFile,'w', format='NETCDF4')
        data.createDimension('NumObs', len(delayFlag))
        data.createVariable('DelayFlag', np.int16, ('NumObs'))
        
        data.variables['DelayFlag'][:] = delayFlag
        
        data.close()
        
def createGroupDelayFull(path, scanInfo, fileList):
    '''
    Create the GroupDelayFull.nc file in ObsEdit dir.

    '''
    for i in range(len(scanInfo.baseInfo[0])):
        if len(scanInfo.ambigNum[i]):
            #string = 'GroupDelayFull_b'+scanInfo.baseInfo[0][i]
            ncFile = ncCreateSamePart(path, 'GroupDelayFull', fileList,scanInfo.baseInfo[0][i])
            
            data = nc.Dataset(ncFile,'w', format='NETCDF4')
            
            data.createDimension('Char_x_1', 1)
            data.createDimension('NumObs', len(scanInfo.gd[i]))
            
            data.createVariable('Band', 'S1', ('Char_x_1'))
            data.createVariable('GroupDelayFull', np.float64, ('NumObs'))
            
            data.variables['Band'][:] = scanInfo.baseInfo[0][i]
            data.variables['GroupDelayFull'][:] = scanInfo.gdApri[i] + scanInfo.ambigNum[i] * scanInfo.baseInfo[2][i]
            
            data.close()

def createNumGroupAmbig(path, scanInfo, fileList):
    '''
    Create the NumGroupAmbig.nc file in ObsEdit dir.

    '''
    for i in range(len(scanInfo.baseInfo[0])):
        if len(scanInfo.ambigNum[i]):
            string = 'NumGroupAmbig_b'+scanInfo.baseInfo[0][i]
            ncFile = ncCreateSamePart(path, string, fileList)
            
            data = nc.Dataset(ncFile,'w', format='NETCDF4')
            
            data.createDimension('Char_x_1', 1)
            data.createDimension('NumObs', len(scanInfo.ambigNum[i]))
            
            data.createVariable('Band', 'S1', ('Char_x_1'))
            data.createVariable('NumGroupAmbig', np.int16, ('NumObs'))
            
            data.variables['Band'][:] = scanInfo.baseInfo[0][i]
            data.variables['NumGroupAmbig'][:] = scanInfo.ambigNum[i]
            
            data.close()
        