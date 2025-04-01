#!/usr/bin/env python3

import netCDF4 as nc
import numpy as np
import os
from COMMON import *

def CreatePartDelayAtmRefract(path, session, numObs, pRefract):
    """
    Create the Part-DelayAtmRefract.nc file.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    numObs : the observe number of session.
    pRefract : the partial derivatives of atmosphere refraction

    Returns
    -------
    The Part-DelayAtmRefract.nc is created.
    """
    ncFile = path+'/ObsPart/Part-DelayAtmRefract.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    data.createDimension('Char_x_6',6)
    data.createDimension('NumObs',numObs)
    data.createDimension('DimX000002',2)
    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("Part-DelayAtmRefract",np.float64,("NumObs",'DimX000002'))
    
    data.variables['Session'][:]=np.char.encode(list(session))
    temp = np.vstack((pRefract, np.zeros(numObs)))
    data.variables['Part-DelayAtmRefract'][:] = temp.T

    data.close()

def createPartERP(path, session, numObs, pdx, pdy, pdut1):
    """
    Create the Part-ERP.nc file, current only the wobble is put.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    numObs : the observe number of session.
    pdx : the partial derivatives of polar x axis for each observe
    pdy : the partial derivatives of polar y axis for each observe
    pdut1 : the partial derivatives of ut1 for each observe

    Returns
    -------
    The Part-ERP.nc is created.
    """
    
    ncFile = path+'/ObsPart/Part-ERP.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    data.createDimension('Char_x_6',6)
    data.createDimension('NumObs',numObs)
    data.createDimension('DimX000002',2)
    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("Part-Wobble",np.float64,("NumObs",'DimX000002','DimX000002'))
    data.createVariable("Part-UT1",np.float64,("NumObs",'DimX000002','DimX000002'))
    
    data.variables['Session'][:]=np.char.encode(list(session))
    tempxy = np.vstack((np.array(pdx),np.array(pdy)))
    temp = np.hstack((tempxy.T, np.zeros((numObs,2))))
    data.variables['Part-Wobble'][:] = np.reshape(temp, (numObs,2,2))

    data.close()
    
def CreatePartRaDec(path, session, numObs, psou):
    """
    Create the Part-RaDec.nc file, current only the wobble is put.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    numObs : the observe number of session.
    psou : the partial derivatives of right ascension and declination for each observe

    Returns
    -------
    The Part-RaDec.nc is created.
    """
    ncFile = path+'/ObsPart/Part-RaDec.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    data.createDimension('Char_x_6',6)
    data.createDimension('NumObs',numObs)
    data.createDimension('DimX000002',2)
    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("Part-RaDec",np.float64,("NumObs",'DimX000002','DimX000002'))
    
    data.variables['Session'][:]=np.char.encode(list(session))
    temp = np.hstack((np.array(psou)*3600000*180/(100*np.pi), np.zeros((numObs,2))))
    data.variables['Part-RaDec'][:] = np.reshape(temp, (numObs,2,2))

    data.close()
    
def createPartXYZ(path, session, numObs, pxyz):
    """
    Create the Part-XYZ.nc file, current only the partial of delay is put, 
    the partial of delay rate is zeros.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    numObs : the observe number of session.
    pxyz : the partial derivatives of station XYZ for each observe

    Returns
    -------
    The Part-XYZ.nc is created.
    """
    ncFile = path+'/ObsPart/Part-XYZ.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    data.createDimension('Char_x_6',6)
    data.createDimension('NumObs',numObs)
    data.createDimension('DimX000002',2)
    data.createDimension('DimX000003',3)
    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("Part-XYZ",np.float64,("NumObs",'DimX000002','DimX000003'))

    
    data.variables['Session'][:]=np.char.encode(list(session))
    temp = np.hstack((np.array(pxyz)/const.c, np.zeros((numObs,3))))
    data.variables['Part-XYZ'][:]=np.reshape(temp, (numObs,2,3))
    
    data.close()
    
    
def makeFile(ncFile):
    
    if os.path.exists(ncFile):
        os.system('rm '+ncFile)
        
    fid = open(ncFile,'w')
    fid.close()
    
    os.system('chmod 777 '+ncFile)