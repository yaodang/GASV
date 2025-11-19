#!/usr/bin/env python3

import numpy as np
import netCDF4 as nc
import os
from INIT import *

def createAntenna(path, session, staList):
    """
    Create the Antenna.nc file.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
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
    data.createDimension('NumStation',len(staList))
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
    
def createSource(path, session, souList, souFile):
    """
    Create the Source.nc file. Current no AprioriSourceReference variable

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    souList : the source name list

    Returns
    -------
    The Source.nc is created.
    """
    
    ncFile = path+'/Source.nc'
    makeFile(ncFile)
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    data.createDimension('Char_x_6',6)
    data.createDimension('NumSource',len(souList))
    data.createDimension('DimX000002',2)
    data.createDimension('DimX000008',8)
    data.createDimension('DimX000018',18)

    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("AprioriSourceList",'S1',("NumSource",'DimX000008'))
    data.createVariable("AprioriSource2000RaDec",np.float64,("NumSource",'DimX000002'))
    data.createVariable("AprioriSourceReference",'S1',("NumSource",'DimX000018'))

    sou_iers, sou_icrf, sou_iau, sou_ivs, flag, Ra, De = readSourceFile(souFile)
    blank = '        '
    RaDec = []
    for i in range(len(souList)):
        name = souList[i]
        if name.strip() in sou_iers:
            index = sou_iers.index(name.strip())
            souRa = Ra[index]
            souDe = De[index]
        elif name.strip() in sou_ivs:
            index = sou_ivs.index(name.strip())
            souRa = Ra[index]
            souDe = De[index]
        else:
            print('        The %s not in source file, using apriori posit in data!' % name)
            sys.exit()
        RaDec.append([souRa, souDe])

    souL = []
    for sou in souList:
        souL.append(list(sou))
    
    data.variables['Session'][:]=np.char.encode(session)
    data.variables['AprioriSourceList'][:] = np.char.encode(souL)
    data.variables['AprioriSource2000RaDec'][:] = np.array(RaDec)
    
    data.close()

    return np.array(RaDec)
    
def createStation(path, session, staList, staFile):
    """
    Create the Station.nc file. Current no AprioriStationTectonicPlate vaariable.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    staList : the station list

    Returns
    -------
    The Station.nc is created.
    """
    
    ncFile = path+'/Station.nc'
    makeFile(ncFile)    
        
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    data.createDimension('Char_x_6',6)
    data.createDimension('NumStation',len(staList))
    data.createDimension('DimX000003',3)
    data.createDimension('DimX000004',4)
    data.createDimension('DimX000008',8)

    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("AprioriStationTectonicPlate",'S1',("NumStation",'DimX000004'))
    data.createVariable("AprioriStationList",'S1',("NumStation",'DimX000008'))
    data.createVariable("AprioriStationXYZ",np.float64,("NumStation",'DimX000003'))
    data.createVariable("AprioriStationVel",np.float64,("NumStation",'DimX000003'))

    station = np.loadtxt(staFile, dtype='str', comments='$$', usecols=[0], unpack=True)
    staPosit = np.loadtxt(staFile, dtype='float', comments='$$', usecols=[1, 2, 3, 4, 5, 6, 7], unpack=False)
    station = add_blank(station)

    XYZ = []
    Vel = []
    for i in range(len(staList)):
        name = staList[i]
        if name in station:
            index = station.index(name)
            XYZ.append(staPosit[index, 0:3])
            Vel.append(staPosit[index,3:6])
        else:
            print('        The %s not in station file, using apriori posit in data and set velocity zeros!'%name)
            sys.exit()

    staL = []
    for sta in staList:
        staL.append(list(sta))
    
    data.variables['Session'][:]=np.char.encode(session)
    data.variables['AprioriStationList'][:] = np.char.encode(staL)
    data.variables['AprioriStationXYZ'][:] = np.array(XYZ)
    data.variables['AprioriStationVel'][:] = np.array(Vel)
    
    data.close()

    return np.array(XYZ)
    
def makeFile(ncFile):
    
    if os.path.exists(ncFile):
        os.system('rm '+ncFile)
        
    fid = open(ncFile,'w')
    fid.close()
    
    os.system('chmod 777 '+ncFile)