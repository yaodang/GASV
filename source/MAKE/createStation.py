#!/usr/bin/env python3

import netCDF4 as nc
import numpy as np
import os
from INIT.read_sourceFile import *
from MOD.mod_staCorr import *
from COMMON.coordinate_transfer import *

def createAzEl(path, RaDec, souPosit, staXYZ, trs2crs):
    """
    Create the <STATION>/AzEl.nc file.

    Parameters
    ----------
    path : the path of vgosDb.
    RaDec : the rigth ascension and declination of observed source [rad].
    souPosit : the observed source position in RaDec.
    staXYZ : the station ITRF coordinates [m].
    trs2crs : TRS transfer to CRS matrix.

    Returns
    -------
    The <STATION>/AzEl.nc is created.
    """
    
    ncFile = path + '/AzEl.nc'
    makeFile(ncFile)
        
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    numStatScan = len(souPosit)
    data.createDimension('Char_x_6',6)
    data.createDimension('Char_x_8',8)
    data.createDimension('NumStatScan',numStatScan)
    data.createDimension('DimX000002',2)

    data.createVariable("ElTheo",np.float64,("NumStatScan",'DimX000002'))
    data.createVariable("AzTheo",np.float64,("NumStatScan",'DimX000002'))

    lam, phi, height = xyz2ell(staXYZ)
    Az = []
    El = []
    for i in range(numStatScan):
        rq, pRaDec = partialSource(RaDec[souPosit[i]-1][0],RaDec[souPosit[i]-1][1])
        az, zd, corz, de, LHAe = locsource(lam, phi, rq, trs2crs[i])
        Az.append([az*180/np.pi,0])
        El.append([(np.pi/2-zd)*180/np.pi,0])
    
    data.variables['ElTheo'][:] = np.array(El)
    data.variables['AzTheo'][:] = np.array(Az)
    
    data.close()
    
def createCalAxisOffset(path, session, station, StatScan, scanState):  
    """
    Create the <STATION>/Cal-AxisOffset.nc file.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    station : the station name
    StatScan : scan posit and station posit in scan.
    scanState : the ellipsoidal coordinates lam,phi,elh for each station of each scan.

    Returns
    -------
    The <STATION>/Cal-AxisOffset.nc is created.
    """
    
    ncFile = path+'/'+station.strip()+'/Cal-AxisOffset.nc'
    makeFile(ncFile)    
        
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    numStatScan = len(StatScan[0])
    data.createDimension('Char_x_6',6)
    data.createDimension('Char_x_8',8)
    data.createDimension('NumStatScan',numStatScan)
    data.createDimension('DimX000002',2)

    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("Station",'S1',("Char_x_8"))
    data.createVariable("Cal-AxisOffset",np.float64,("NumStatScan",'DimX000002'))


    axisOffset = []
    for i in range(numStatScan):
        axisOffset.append([scanState[StatScan[0][i]][StatScan[1][i]][5],0])
 
    data.variables['Session'][:]=np.char.encode(list(session))
    data.variables['Station'][:]=np.char.encode(list(station))
    
    data.variables['Cal-AxisOffset'][:] = np.array(axisOffset)
    
    data.close()

def createPartAxisOffset(path, session, station, StatScan, scanState):    
    """
    Create the <STATION>/Part-AxisOffset.nc file.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    station : the station name
    StatScan : scan posit and station posit in scan.
    scanState : the ellipsoidal coordinates lam,phi,elh for each station of each scan.

    Returns
    -------
    The <STATION>/Part-AxisOffset.nc is created.
    """
    
    ncFile = path+'/'+station.strip()+'/Part-AxisOffset.nc'
    makeFile(ncFile)    
        
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    numStatScan = len(StatScan[0])
    data.createDimension('Char_x_6',6)
    data.createDimension('Char_x_8',8)
    data.createDimension('NumStatScan',numStatScan)
    data.createDimension('DimX000002',2)

    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("Station",'S1',("Char_x_8"))
    data.createVariable("Part-AxisOffset",np.float64,("NumStatScan",'DimX000002'))


    pAxisO = []
    for i in range(numStatScan):
        pAxisO.append([scanState[StatScan[0][i]][StatScan[1][i]][6],0])
 
    data.variables['Session'][:]=np.char.encode(list(session))
    data.variables['Station'][:]=np.char.encode(list(station))
    
    data.variables['Part-AxisOffset'][:] = np.array(pAxisO)
    
    data.close()

def createCalSlantDry(path, session, station, StatScan, scanState):
    """
    Create the <STATION>/Cal-SlantPathTropDry_kXXX.nc file.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    station : the station name
    StatScan : scan posit and station posit in scan.
    scanState : the ellipsoidal coordinates lam,phi,elh for each station of each scan.

    Returns
    -------
    The <STATION>/Cal-SlantPathTropDry_kXXX.nc is created.
    """
    
    ncFile = path+'/'+station.strip()+'/Cal-SlantPathTropDry_kGPT3.nc'
    makeFile(ncFile)    
        
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    numStatScan = len(StatScan[0])
    data.createDimension('Char_x_6',6)
    data.createDimension('Char_x_8',8)
    data.createDimension('NumStatScan',numStatScan)
    data.createDimension('DimX000002',2)

    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("Station",'S1',("Char_x_8"))
    data.createVariable("Cal-SlantPathTropDry",np.float64,("NumStatScan",'DimX000002'))

    zdryDelay = []
    for i in range(numStatScan):
        zdryDelay.append([scanState[StatScan[0][i]][StatScan[1][i]][7],0])
 
    data.variables['Session'][:]=np.char.encode(list(session))
    data.variables['Station'][:]=np.char.encode(list(station))
    
    data.variables['Cal-SlantPathTropDry'][:] = np.array(zdryDelay)
    
    data.close()
    
def createCalSlantWet(path, session, station, StatScan):
    """
    Create the <STATION>/Cal-SlantPathTropWet_kXXX.nc file, now is set to zeros.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    station : the station name
    StatScan : scan posit and station posit in scan.
    scanState : the ellipsoidal coordinates lam,phi,elh for each station of each scan.

    Returns
    -------
    The <STATION>/Cal-SlantPathTropWet_kXXX.nc is created.
    """
    
    ncFile = path+'/'+station.strip()+'/Cal-SlantPathTropWet_kGPT3.nc'
    makeFile(ncFile)    
        
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    numStatScan = len(StatScan[0])
    data.createDimension('Char_x_6',6)
    data.createDimension('Char_x_8',8)
    data.createDimension('NumStatScan',numStatScan)
    data.createDimension('DimX000002',2)

    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("Station",'S1',("Char_x_8"))
    data.createVariable("Cal-SlantPathTropWet",np.float64,("NumStatScan",'DimX000002'))
 
    data.variables['Session'][:] = np.char.encode(list(session))
    data.variables['Station'][:] = np.char.encode(list(station))
    
    data.variables['Cal-SlantPathTropWet'][:] = np.zeros((numStatScan,0))
    
    data.close()
    
def createMet(path, T, P, H, station):
    
    ncFile = path+'/Met.nc'
    makeFile(ncFile)
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
        
    data.createDimension('NumStatScan',len(T))
    data.createDimension('Char_x_8', 8)
    
    data.createVariable("Station",'S1',("Char_x_8"))
    data.createVariable("TempC",np.float64,("NumStatScan"))
    data.createVariable("AtmPres",np.float64,("NumStatScan"))
    data.createVariable("RelHum",np.float64,("NumStatScan"))
    
    data.variables['Station'] = np.char.encode(list(station))
    data.variables['TempC'][:] = T
    data.variables['AtmPres'][:] = P
    data.variables['RelHum'][:] = H*1E-2
    
    data.close()

def createCalCab(path, CC, station):
    
    staCab,cabSign = initCabSign()
    if station in staCab:
        index= staCab.index(station)
        sign = cabSign[index]
    else:
        sign = 1
    
    ncFile = path+'/Cal-Cable.nc'
    makeFile(ncFile)
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    
    data.createDimension('Char_x_8',8)
    data.createDimension('NumStatScan',len(CC))
    
    data.createVariable("Station",'S1',("Char_x_8"))
    data.createVariable("Cal-Cable",np.float64,("NumStatScan"))
    
    data.variables['Station'][:] = np.char.encode(list(station))
    data.variables['Cal-Cable'][:] = CC*sign
    
    data.close()
    
def createClk(path, Clk, station):
    ncFile = path+'/Fmout-GNSS.nc'
    makeFile(ncFile)
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    
    data.createDimension('Char_x_8',8)
    data.createDimension('NumLogClock',len(Clk[0]))
    
    data.createVariable("Station",'S1',("Char_x_8"))
    data.createVariable("ClkMJD",np.float64,("NumLogClock"))
    data.createVariable("Fmout-GNSS",np.float64,("NumLogClock"))
    
    data.variables['Station'][:] = np.char.encode(list(station))
    data.variables['ClkMJD'][:] = Clk[0]
    data.variables['Fmout-GNSS'][:] = Clk[1]
    
    data.close()
    
def createPartZenithWet(path, session, station, StatScan, mfWet):
    """
    Create the <STATION>/Part-ZenithPathTropWet_kXXX.nc file.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    station : the station name
    StatScan : scan posit and station posit in scan.
    mfWet : the mapping function of zenith wet delay.

    Returns
    -------
    The <STATION>/Part-HorizonGrd_kXXX.nc is created.
    """
    
    ncFile = path+'/'+station.strip()+'/Part-ZenithPathTropWet_kGPT3.nc'
    makeFile(ncFile)    
        
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    numStatScan = len(StatScan[0])
    data.createDimension('Char_x_6',6)
    data.createDimension('Char_x_8',8)
    data.createDimension('NumStatScan',numStatScan)
    data.createDimension('DimX000002',2)

    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("Station",'S1',("Char_x_8"))
    data.createVariable("Part-ZenithPathTropWet",np.float64,("NumStatScan",'DimX000002'))


    pmfWet = []
    for i in range(numStatScan):
        
        pmfWet.append([mfWet[StatScan[0][i]][StatScan[1][i]],0])

    data.variables['Session'][:]=np.char.encode(list(session))
    data.variables['Station'][:]=np.char.encode(list(station))
    
    data.variables['Part-ZenithPathTropWet'][:] = np.array(pmfWet)
    
    data.close()
    
def createPartHorizonGrd(path, session, station, StatScan, mfGE, mfGN):
    """
    Create the <STATION>/Part-HorizonGrd_kGPT3.nc file.

    Parameters
    ----------
    path : the path of vgosDb.
    session : experiment name.
    station : the station name
    StatScan : scan posit and station posit in scan.
    mfGE : the mapping function of east gradient.
    mfGN : the mapping function of north gradient.

    Returns
    -------
    The <STATION>/Part-HorizonGrd_kGPT3.nc is created.
    """
    
    ncFile = path+'/'+station.strip()+'/Part-HorizonGrd_kGPT3.nc'
    makeFile(ncFile)    
        
    data = nc.Dataset(ncFile,'w',format='NETCDF4')

    numStatScan = len(StatScan[0])
    data.createDimension('Char_x_6',6)
    data.createDimension('Char_x_8',8)
    data.createDimension('NumStatScan',numStatScan)
    data.createDimension('DimX000002',2)

    data.createVariable("Session",'S1',("Char_x_6"))
    data.createVariable("Station",'S1',("Char_x_8"))
    data.createVariable("Part-HorizonGrad",np.float64,("NumStatScan",'DimX000002','DimX000002'))


    mfgrad = []
    for i in range(numStatScan):
        
        mfgrad.append([mfGN[StatScan[0][i]][StatScan[1][i]],
                       mfGE[StatScan[0][i]][StatScan[1][i]]])

    data.variables['Session'][:]=np.char.encode(list(session))
    data.variables['Station'][:]=np.char.encode(list(station))
    
    temp = np.hstack((np.array(mfgrad),np.zeros((numStatScan, 2))))
    data.variables['Part-HorizonGrad'][:] = np.reshape(temp, (numStatScan,2,2))
    
    data.close()

def createOceanTidal(path, scanTime, Scan2Station, cto):
    '''
    Create the Dis-OceanLoad.nc file in Station dir.

    Parameters
    ----------
    path : The path of Scan file.
    scanTime : the Y/DOY/H/M/S of scan.
    Scan2Station : the station scan.
    cto : the ocean tidal parameter.

    Returns
    -------
    The Dis-OceanLoad.nc is created.

    '''
    posit = np.where(Scan2Station!=0)
    scanStaNum = len(posit[0])

    DZWS = np.zeros((scanStaNum,2,3))
    for i in range(scanStaNum):
        DZ,DW,DS = ocean_tidal_corr_iers(scanTime[posit[0][i]], cto)
        DZWS[i, 0, 0] = DZ
        DZWS[i, 0, 1] = DW
        DZWS[i, 0, 2] = DS

    if not os.path.exists(path):
        os.mkdir(path)

    ncFile = path + '/Dis-OceanLoad.nc'
    makeFile(ncFile)

    data = nc.Dataset(ncFile, 'w', format='NETCDF4')

    data.createDimension('NumStatScan', scanStaNum)
    data.createDimension('DimX000002', 2)
    data.createDimension('DimX000003', 3)

    data.createVariable("Dis-OceanLoad", np.float64, ("NumStatScan", "DimX000002", "DimX000003"))
    data.variables['Dis-OceanLoad'][:] = DZWS
    data.close()

def createStaTimeUTC(path, scanTime, Scan2Station):
    '''
    Create the TimeUTC.nc file in Station dir.

    Parameters
    ----------
    path : The path of Scan file.
    scanTime : the Y/DOY/H/M/S of scan.
    Scan2Station : the station scan.

    Returns
    -------
    The TimeUTC.nc is created.

    '''
    posit = np.where(Scan2Station != 0)
    scanStaNum = len(posit[0])
    YMDHM = np.zeros((scanStaNum, 5), dtype=np.int16)
    Second = np.zeros(scanStaNum, dtype=np.float64)
    for i in range(scanStaNum):
        YMDHM[i] = [scanTime[posit[0][i]][0],
                    scanTime[posit[0][i]][5],
                    scanTime[posit[0][i]][6],
                    scanTime[posit[0][i]][2],
                    scanTime[posit[0][i]][3]]
        Second[i] = scanTime[posit[0][i]][4]

    ncFile = path + '/TimeUTC.nc'
    makeFile(ncFile)

    data = nc.Dataset(ncFile, 'w', format='NETCDF4')

    data.createDimension('NumStatScan', scanStaNum)
    data.createDimension('DimX000005', 5)

    data.createVariable("Second", np.float64, ("NumStatScan"))
    data.createVariable("YMDHM", np.int16, ("NumStatScan", "DimX000005"))

    data.variables['Second'][:] = Second
    data.variables['YMDHM'][:] = YMDHM
    data.close()
    
def initCabSign():

    staCab = ['HARTRAO ', 'MATERA  ', 'AAGO    ','KOKEE   ','ONSALA60']
    cabSign = -np.ones(len(staCab))
    
    return staCab, cabSign