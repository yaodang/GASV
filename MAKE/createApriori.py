#!/usr/bin/env python3

import numpy as np
import netCDF4 as nc
import os

def createAntenna(path, session, numSta, staList, stationInfo):
    """
    Create the Antenna.nc file.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    numSta : the station number of session.
    staList : the station list
    stationInfo : the struct of station information

    Returns
    -------
    The Antenna.nc is created.
    """
    
    ncFile = path+'/Antenna.nc'
    makeFile(ncFile)    
        
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    data.createDimension('Char_x_6',6)
    data.createDimension('NumStation',numSta)
    data.createDimension('DimX000001',1)
    data.createDimension('DimX000008',8)

    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("AntennaStationList",'S1',("NumStation",'DimX000008'))
    data.createVariable("AntennaAxisOffset",np.float64,("NumStation"))

    axisOffset = []
    staL = []
    for sta in staList:
        positS = stationInfo.stationName.index(sta)
        axisOffset.append(stationInfo.axoffset[positS])
        staL.append(list(sta))
    
    data.variables['Session'][:]=np.char.encode(session)
    data.variables['AntennaStationList'][:] = np.char.encode(staL)
    data.variables['AntennaAxisOffset'][:] = np.array(axisOffset)
    
    data.close()
    
def createSource(path, session, numSou, souList, sourceInfo):
    """
    Create the Source.nc file. Current no AprioriSourceReference variable

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    numSou : the source number of session.
    souList : the source name list
    sourceInfo : the struct of source information

    Returns
    -------
    The Source.nc is created.
    """
    
    ncFile = path+'/Source.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    data.createDimension('Char_x_6',6)
    data.createDimension('NumSource',numSou)
    data.createDimension('DimX000002',2)
    data.createDimension('DimX000008',8)
    data.createDimension('DimX000018',18)

    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("AprioriSourceList",'S1',("NumSource",'DimX000008'))
    data.createVariable("AprioriSource2000RaDec",np.float64,("NumSource",'DimX000002'))
    data.createVariable("AprioriSourceReference",'S1',("NumSource",'DimX000018'))

    RaDec = []
    souL = []
    for sou in souList:
        positS = sourceInfo.sourceName.index(sou)
        RaDec.append(sourceInfo.rade[positS])
        souL.append(list(sou))
    
    data.variables['Session'][:]=np.char.encode(session)
    data.variables['AprioriSourceList'][:] = np.char.encode(souL)
    data.variables['AprioriSource2000RaDec'][:] = np.array(RaDec)
    
    data.close()
    
def createStation(path, session, numSta, staList, stationInfo):
    """
    Create the Station.nc file. Current no AprioriStationTectonicPlate vaariable.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    numSta : the station number of session.
    staList : the station list
    stationInfo : the struct of station information

    Returns
    -------
    The Station.nc is created.
    """
    
    ncFile = path+'/Station.nc'
    makeFile(ncFile)    
        
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    data.createDimension('Char_x_6',6)
    data.createDimension('NumStation',numSta)
    data.createDimension('DimX000003',3)
    data.createDimension('DimX000004',4)
    data.createDimension('DimX000008',8)

    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("AprioriStationTectonicPlate",'S1',("NumStation",'DimX000004'))
    data.createVariable("AprioriStationList",'S1',("NumStation",'DimX000008'))
    data.createVariable("AprioriStationXYZ",np.float64,("NumStation",'DimX000003'))
    data.createVariable("AprioriStationVel",np.float64,("NumStation",'DimX000003'))


    XYZ = []
    Vel = []
    staL = []
    for sta in staList:
        positS = stationInfo.stationName.index(sta)
        XYZ.append(stationInfo.posit[positS])
        Vel.append(stationInfo.vel[positS])
        staL.append(list(sta))
    
    data.variables['Session'][:]=np.char.encode(session)
    data.variables['AprioriStationList'][:] = np.char.encode(staL)
    data.variables['AprioriStationXYZ'][:] = np.array(XYZ)
    data.variables['AprioriStationVel'][:] = np.array(Vel)
    
    data.close()
    
def makeFile(ncFile):
    
    if os.path.exists(ncFile):
        os.system('rm '+ncFile)
        
    fid = open(ncFile,'w')
    fid.close()
    
    os.system('chmod 777 '+ncFile)