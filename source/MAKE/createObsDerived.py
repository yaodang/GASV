#!/usr/bin/env python3

import os
import netCDF4 as nc
import numpy as np
from COMMON.other import *

def createSlantPathIonoGroup(path, ionDelay, ionDelaySig, fileList):
    '''
        Create the Cal-SlantPathIonoGroup.nc file in ObsDerived dir.

    '''

    ncFile = ncCreateSamePart(path, 'Cal-SlantPathIonoGroup', fileList, 'X')
    data = nc.Dataset(ncFile, 'w', format='NETCDF4')

    if type(ionDelay) == int:
        obsNum = ionDelaySig
    else:
        obsNum = len(ionDelay)

    data.createDimension('NumObs', obsNum)
    data.createDimension('DimX000002',2)

    data.createVariable('Cal-SlantPathIonoGroup', np.float64, ('NumObs','DimX000002'))
    data.createVariable('Cal-SlantPathIonoGroupSigma', np.float64, ('NumObs','DimX000002'))

    data.variables['Cal-SlantPathIonoGroup'][:] = np.zeros((obsNum,2))
    data.variables['Cal-SlantPathIonoGroupSigma'][:] = np.zeros((obsNum, 2))

    if type(ionDelay) != int and type(ionDelaySig) != int:
        data.variables['Cal-SlantPathIonoGroup'][:,0] = ionDelay
        data.variables['Cal-SlantPathIonoGroupSigma'][:,0] = ionDelaySig

    data.close()
