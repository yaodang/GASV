#!/usr/bin/env python3

import netCDF4 as nc
import numpy as np
import os
from COMMON.other import makeFile

def createERPApriori(path, session, numScan, eopObs):
    """
    Create the ERPApriori.nc file.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    numScan : the scan number of session.
    eopObs : the apriori value of xp,yp,ut1,DX,DY derivatives for each observe

    Returns
    -------
    The ERPApriori.nc is created.
    """
    
    ncFile = path+'/ERPApriori.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    data.createDimension('Char_x_6',6)
    data.createDimension('NumScans',numScan)
    data.createDimension('DimX000002',2)
    
    data.createVariable("Session",'S1',("Char_x_6"))
    data.variables['Session'][:]=np.char.encode(list(session))
    
    
    data.createVariable("UT1",np.float64,("NumScans"))
    data.createVariable("PolarMotion",np.float64,("NumScans","DimX000002"))
    
    data.variables['UT1'][:]=eopObs.UT1
    polar = np.vstack((eopObs.XP,eopObs.YP))
    data.variables['PolarMotion'][:]=polar.T
    
    data.close()
    
def createEphemeris(path, session, numScan, sun, moon, earth):
    """
    Create the Ephemeris.nc file.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    numScan : the scan number of session.
    sun : the geocentric position, velocity of sun
    moon : the geocentric position, velocity of moon
    earth : the barycentric position, velocity and acceleration of earth

    Returns
    -------
    The Ephemeris.nc is created.
    """
    
    ncFile = path+'/Ephemeris_kDE421JPL.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')    
    
    data.createDimension('Char_x_6',6)
    data.createDimension('NumScans',numScan)
    data.createDimension('DimX000002',2)
    data.createDimension('DimX000003',3)
    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("SunXYZ", np.float64, ("NumScans","DimX000002","DimX000003"))
    data.createVariable("MoonXYZ", np.float64, ("NumScans","DimX000002","DimX000003"))
    data.createVariable("EarthXYZ", np.float64, ("NumScans","DimX000003","DimX000003"))

    data.variables['Session'][:]=np.char.encode(list(session))
    temp = np.hstack((sun.xgeo.T, sun.vgeo.T))
    data.variables['SunXYZ'][:] = np.reshape(temp, (numScan,2,3))
    
    temp = np.hstack((moon.xgeo.T, moon.vgeo.T))
    data.variables['MoonXYZ'][:] = np.reshape(temp, (numScan,2,3))

    temp = np.hstack((earth.xbar.T, earth.vbar.T, earth.acc.T))
    data.variables['EarthXYZ'][:] = np.reshape(temp, (numScan,3,3))
    
    data.close()
    
def createTimeUTC(path, scanTime, numScan):
    '''
    Create the TimeUTC file of Scan

    Parameters
    ----------
    path : The path of TimeUTC file.
    scanTime : the scan time.
    numScan : the number of scan

    Returns
    -------
    The TimeUTC is created.

    '''
    ncFile = path+'/TimeUTC.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')    
    
    data.createDimension('NumScans',numScan)
    data.createDimension('DimX000005',5)
    
    data.createVariable("Second", np.float64, ("NumScans"))
    data.createVariable("YMDHM", np.int16, ("NumScans","DimX000005"))

    data.variables['Second'][:] = np.array(scanTime)[:,4]

    data.variables['YMDHM'][:] = np.array(scanTime,dtype=int)[:,[0,5,6,2,3]]
    
    data.close()

    
#def createNutation():
    