#!/usr/bin/env python3

import os
import netCDF4 as nc
import numpy as np

def createDelayTheoretical(path, session, numObs, delayTheory):
    """
    Create the DelayTheoretical.nc file.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    numObs : the observe number of session.
    delayTheory : the consensus theory delay

    Returns
    -------
    The DelayTheoretical.nc is created.
    """
    ncFile = path+'/ObsTheoretical/DelayTheoretical.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    data.createDimension('Char_x_6',6)
    data.createDimension('NumObs',numObs)
    data.createDimension('DimX000002',2)
    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("DelayTheoretical",np.float64,("NumObs"))
    
    data.variables['Session'][:]=np.char.encode(list(session))
    data.variables['DelayTheoretical'][:] = delayTheory

    data.close()    
    

#def createRateTheoretical():
    
def makeFile(ncFile):
    
    if os.path.exists(ncFile):
        os.system('rm '+ncFile)
        
    fid = open(ncFile,'w')
    fid.close()
    
    os.system('chmod 777 '+ncFile)