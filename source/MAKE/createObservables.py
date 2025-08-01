#!/usr/bin/env python3

import netCDF4 as nc
import numpy as np
import os
from COMMON.other import makeFile

def createAmbigSize(path, ambig, band, blSort, numObs):
    '''
    Create the AmbigSize_b?.nc file in Observables path

    Parameters
    ----------
    path : str
        the Observables path.
    ambig : float
        the group delay ambiguity.
    band : str
        the observe band.

    Returns
    -------
    AmbigSize_b? is created.

    '''
    ncFile = path+'/AmbigSize_b'+band+'.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    data.createDimension('Char_x_1', 1)
    data.createDimension('NumObs', numObs)
    
    data.createVariable("Band", 'S1', ("Char_x_1"))
    data.createVariable("AmbigSize", np.float64, ("NumObs"))
        
    if len(blSort) == 0:
        ambigSize = np.array(ambig).reshape((len(ambig),))
    else:
        ambigSize = []
        for iscan in range(len(blSort)):
            temp = np.array(ambig[iscan])
            
            ambigSize.extend(temp[blSort[iscan]].tolist())
        ambigSize = np.array(ambigSize)
    
    data.variables['Band'][:] = np.char.encode(band)
    data.variables['AmbigSize'][:] = ambigSize

    data.close()

def createBaseline(path, scanBL, obsNum, blSort):
    '''
    Create the Baseline.nc file in Observables path

    Parameters
    ----------
    path : str
        the Observables path.
    scanBL : list
        the  observe baseline of earch scan.
    obsNum : int
        the number of oberve.
    blSort : list
        the sorted baseline index of earch scan.

    Returns
    -------
    Baseline.nc is created.

    ''' 
    
    ncFile = path+'/Baseline.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    
    data.createDimension('DimX000002',2)
    data.createDimension('DimX000008',8)
    
    if len(blSort) == 0:
        data.createVariable("Baseline", 'S1', ("DimX000002", "DimX000008"))
        
        data.variables['Baseline'][0,:] = np.char.encode(list(scanBL[0][0][0]))
        data.variables['Baseline'][1,:] = np.char.encode(list(scanBL[0][0][1]))
    else:
        data.createDimension('NumObs',obsNum)
        data.createVariable("Baseline", 'S1', ("NumObs","DimX000002", "DimX000008"))
        
        num = 0
        for iscan in range(len(blSort)):
            for ibl in blSort[iscan]:        
                data.variables['Baseline'][num,0,:] = np.char.encode(list(scanBL[iscan][ibl][0]))
                data.variables['Baseline'][num,1,:] = np.char.encode(list(scanBL[iscan][ibl][1]))
                num += 1
    
    data.close()
    
def createChannelInfo(path, ampp, apNum, sampleRate, freq, band, blSort, numObs):
    
    
    ncFile = path+'/ChannelInfo_b'+band+'.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    
    data.createDimension('NumObs', numObs)
    data.createDimension('DimUnity', 1)
    data.createDimension('DimX0000002', 2)
    data.createDimension('NumChannels', len(freq[0][0]))
    
    data.createVariable("SampleRate", np.float64, ("DimUnity"))
    data.createVariable("ChannelFreq", np.float64, ("NumObs","NumChannels"))
    data.createVariable("ChanAmpPhase", np.float64, ("NumObs","NumChannels","DimX0000002"))
    data.createVariable("NumAp", np.float64, ("NumObs","NumChannels","DimX0000002"))
    
    data.variables['SampleRate'][:] = sampleRate[0][0]*1E6
    
    ChannelFreq = []
    ChanAmpPhase = []
    NumAp = []
    
    for iscan in range(len(ampp)):
        for iob in range(len(ampp[iscan])):
            if len(blSort) == 0:
                index = 0
            else:
                index = blSort[iscan][iob]
            ChannelFreq.append(freq[iscan][index])
            ChanAmpPhase.append(ampp[iscan][index])
            NumAp.append(apNum[iscan][index])
    
    
    data.variables['ChannelFreq'][:] = np.array(ChannelFreq)
    data.variables['ChanAmpPhase'][:] = np.array(ChanAmpPhase)
    data.variables['NumAp'][:] = np.array(NumAp)
    data.close()
    
    
    
def createDelay(path, delay, sigma, blSort, band, choice):
    '''
    Create the GroupDelay_b?.nc file in Observables path

    Parameters
    ----------
    path : str
        the Observables path..
    delay : list
        the group delay of earch scan.
    sigma : list
        the group delay sigma of earch scan.
    blSort : list
        the sorted baseline index of earch scan.
    band : char
        the observe frequency.
    choice : int
        the sgdelay(0) or groupdelay (1)

    Returns
    -------
    GroupDelay_b?.nc is created.

    ''' 
    
    if choice == 0:
        ncFile = path+'/SBDelay_b'+band+'.nc'
    elif choice == 1:
        ncFile = path+'/GroupDelay_b'+band+'.nc'

    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    
    if len(blSort) == 0:
        GD = np.array(delay).reshape((len(delay),))
        GDSig = np.array(sigma).reshape((len(delay),))
    else:
        GD = []
        GDSig = []
        for iscan in range(len(blSort)):
            tempGD = np.array(delay[iscan])
            tempGDSig = np.array(sigma[iscan])
            
            GD.extend(tempGD[blSort[iscan]].tolist())
            GDSig.extend(tempGDSig[blSort[iscan]].tolist())
        GD = np.array(GD)
        GDSig = np.array(GDSig)
            
    numObs = len(GD)
    
    data.createDimension('NumObs', numObs)
    data.createDimension('Char_x_1', 1)
    
    data.createVariable("Band", 'S1', ("Char_x_1"))
    data.createVariable("GroupDelay", np.float64, ("NumObs"))
    data.createVariable("GroupDelaySig", np.float64, ("NumObs"))
    
    data.variables['Band'][:] = np.char.encode(band)
    data.variables['GroupDelay'][:] = GD
    data.variables['GroupDelaySig'][:] = GDSig
    
    data.close()

def createQualityCode(path, QCode, blSort, band):
    '''
    Create the QualityCode_b?.nc file in Observables path

    Parameters
    ----------
    path : str
        the Observables path..
    QCode : list
        the observe quality of earch scan.
    blSort : list
        the sorted baseline index of earch scan.

    Returns
    -------
    QualityCode_b?.nc is created.

    '''
    
    ncFile = path+'/QualityCode_b'+band+'.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    
    if len(blSort) == 0:
        QualityCode = np.char.encode(np.array(QCode).reshape((len(QCode),)))
    else:
        QualityCode = []
        for iscan in range(len(blSort)):
            temp = np.array(QCode[iscan])
            QualityCode.extend(temp[blSort[iscan]].tolist())
        QualityCode = np.char.encode(QualityCode)
            
    numObs = len(QualityCode)
    
    data.createDimension('Char_x_1', 1)
    data.createDimension('NumObs', numObs)
    
    data.createVariable("Band", 'S1', ("Char_x_1"))
    data.createVariable("QualityCode", 'S1', ("NumObs"))
    
    data.variables['Band'][:] = np.char.encode(band)
    data.variables['QualityCode'][:] = QualityCode
    
    data.close()
    
def createRefFreq(path,band):
    ncFile = os.path.join(path,'RefFreq_b'+band+'.nc')
    makeFile(ncFile) 
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    data.createDimension('Char_x_1', 1)
    data.createDimension('DimUnity', 1)
    
    data.createVariable("Band", 'S1', ("Char_x_1"))
    data.createVariable("RefFreq", np.float64, ("DimUnity"))
    
    data.variables['Band'][:] = np.char.encode(band)
    data.variables['RefFreq'][:] = np.array([8000])
    
    data.close()
    
def createSNR(path, snr, blSort, band):
    '''
    Create the SNR_b?.nc file in Observables path

    Parameters
    ----------
    path : str
        the Observables path..
    snr : list
        the observe snr of earch scan.
    blSort : list
        the sorted baseline index of earch scan.

    Returns
    -------
    SNR_b?.nc is created.

    '''
    
    ncFile = os.path.join(path,'SNR_b'+band+'.nc')
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    
    if len(blSort) == 0:
        obsSNR = np.array(snr).reshape((len(snr),))
    else:
        obsSNR = []
        for iscan in range(len(blSort)):
            temp = np.array(snr[iscan])
            
            obsSNR.extend([temp[blSort[iscan]].tolist()])
        obsSNR = np.array(obsSNR)
            
    numObs = len(obsSNR)
    
    data.createDimension('Char_x_1', 1)
    data.createDimension('NumObs', numObs)
    
    data.createVariable("Band", 'S1', ("Char_x_1"))
    data.createVariable("SNR", np.float64, ("NumObs"))
    
    data.variables['Band'][:] = np.char.encode(band)
    data.variables['SNR'][:] = obsSNR
    
    data.close()

def createSource(path, sou, Obs2Scan):
    '''
    Create the Source.nc file in Observables path.

    Parameters
    ----------
    path : str
        the Observables path.
    sou : list
        the source name of earch scan.
    Obs2Scan : array
        the observe number of earch scan.

    Returns
    -------
    Source.nc is created.

    '''
    
    ncFile = path+'/Source.nc'
    makeFile(ncFile)    
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    
    data.createDimension('NumObs', len(Obs2Scan))
    data.createDimension('DimX000008',8)
    
    data.createVariable("Source", 'S1', ("NumObs",'DimX000008'))

    
    for iscan in range(len(sou)):
        posit = np.where(Obs2Scan==(iscan+1))
        data.variables['Source'][posit[0]] = np.char.encode(list(sou[iscan]))
        
        
    data.close()


