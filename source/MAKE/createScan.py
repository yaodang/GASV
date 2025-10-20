#!/usr/bin/env python3

import netCDF4 as nc
import numpy as np
import os,sys
from COMMON.other import makeFile
from COMMON.time_transfer import *
from MOD.mod_iau2006a import mod_iau2006a_iers
from MOD.mod_eop import *

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

def createHFERP(path, scanMJD, numScan):
    '''
    Create the HFERP_kdesai.nc file in Scan dir.

    Parameters
    ----------
    path : The path of Scan file.
    scanMJD : the MJD of scan.
    scanNum : the number of scan

    Returns
    -------
    The Cal-HiFreqERP_kdesai.nc is created.

    '''
    TAB = getTab('Desai')
    hfpmx, hfpmy, hfut1 = eop_hf_eanes(scanMJD, TAB)
    hferp = np.array([hfpmx, hfpmy, hfut1])

    ncFile = path + '/Cal-HiFreqERP_kdesai.nc'
    makeFile(ncFile)

    data = nc.Dataset(ncFile, 'w', format='NETCDF4')

    data.createDimension('NumScans', numScan)
    data.createDimension('DimX000003', 3)

    data.createVariable("PMUT1", np.float64, ("NumScans", "DimX000003"))
    data.variables['PMUT1'][:] = hferp.T
    data.close()

def createNutation(path, scanMJD, numScan):
    '''
    Create the NutationNRO_kIAU2006.nc file of Scan

    Parameters
    ----------
    path : The path of NutationNRO file.
    scanMJD : the MJD of scan.
    numScan : the number of scan

    Returns
    -------
    The NutationNRO_kIAU2006.nc is created.

    '''
    X,Y,S = mod_iau2006a_iers(scanMJD)

    ncFile = path + '/NutationNRO_kIAU2006.nc'
    makeFile(ncFile)

    data = nc.Dataset(ncFile, 'w', format='NETCDF4')

    data.createDimension('NumScans', numScan)
    data.createDimension('DimX000002', 2)
    data.createDimension('DimX000003', 3)

    data.createVariable("NutationNRO", np.float64, ("NumScans", "DimX000002", "DimX000003"))
    tempData = np.zeros((numScan,2,3))
    for i in range(numScan):
        tempData[i][0, 0] = X[i]
        tempData[i][0, 1] = Y[i]
        tempData[i][0, 2] = S[i]
    data.variables['NutationNRO'][:] = tempData
    data.close()

def createTimeUTC(path, scanTime, numScan):
    '''
    Create the TimeUTC.nc file of Scan

    Parameters
    ----------
    path : The path of TimeUTC file.
    scanTime : the scan time.
    numScan : the number of scan

    Returns
    -------
    The TimeUTC.nc is created.

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
    