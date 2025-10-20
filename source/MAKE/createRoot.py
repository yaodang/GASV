#!/usr/bin/env python3

import netCDF4 as nc
import numpy as np
import os,datetime
from COMMON.other import makeFile

def createHead(path, session, staAll, souAll, scanNum, obsNum):
    '''
    Create the Head.nc file in vgosDB path

    Parameters
    ----------
    path : str
        vgosDB path.
    session : str
        the corr file name.
    staAll : list
        the all observe station.
    souAll : list
        the all source source.
    scanNum : int
        the all scan number.
    obsNum : int
        the all observe number.

    Returns
    -------
    Head.nc is created.

    '''
    
    ncFile = path+'/Head.nc'
    makeFile(ncFile)
    
    data = nc.Dataset(ncFile,'w',format='NETCDF4')
    
    data.createDimension('DimUnity', 1)
    data.createDimension('DimX000008',8)
    data.createDimension('DimX000006',6)
    data.createDimension('DimX000010',10)
    
    zeros = '000000'
    DimX = 'DimX'+zeros[:6-len(session)]+str(len(session))
    data.createDimension(DimX, len(session))
    
    staNum = len(staAll)
    souNum = len(souAll)

    data.createDimension('NumSource', souNum)
    data.createDimension('NumStation', staNum)
    
    #data.createVariable('Session', 'S1', (DimX))
    data.createVariable('ExpName', 'S1', ('DimX000006'))
    data.createVariable('ExpDescription', 'S1', ('DimX000010'))
    data.createVariable("NumStation", np.int32, ("DimUnity"))
    data.createVariable("NumSource", np.int32, ("DimUnity"))
    data.createVariable("NumScan", np.int32, ("DimUnity"))
    data.createVariable("NumObs", np.int32, ("DimUnity"))
    data.createVariable("StationList", 'S1', ("NumStation","DimX000008"))
    data.createVariable("SourceList", 'S1', ("NumSource","DimX000008"))
    
    
    data.variables['ExpName'][:] = np.char.encode(list('Test  '))
    data.variables['ExpDescription'][:] = np.char.encode(list('Test YD DB'))
    data.variables['NumStation'][:] = staNum
    data.variables['NumSource'][:] = souNum
    data.variables['NumScan'][:] = scanNum
    data.variables['NumObs'][:] = obsNum
    #data.variables['Session'][:] = np.char.encode(list(session))

    for i in range(staNum):
        data.variables['StationList'][i,:] = np.char.encode(list(staAll[i]))
        
    for i in range(souNum):
        data.variables['SourceList'][i,:] = np.char.encode(list(souAll[i]))
        
    data.close()
    
def createWrpFile(path, staAll, flag, *args):
    
    currentTime = datetime.datetime.now()
    
    if flag == 0:
        band = args[0]
        session = args[1]
        acName = args[2]
        
        wrpFile = os.path.join(path,session+'_V001_i%s_kall.wrp'%acName)
        makeFile(wrpFile) 
        
        fid = open(wrpFile,'w')
        fid.writelines('Begin History\n!\n'+\
                       'Begin Process makedb\n'+\
                       'CreatedBy YD\n'+\
                       'RunTimeTag %s UTC\n'%(str(currentTime))+\
                       'End Process makedb\n!\n'+\
                       'End History\n!\n')
            
        fid.writelines('Begin Session\n'+\
                       'Head.nc\n'+\
                       'Source.nc\n'+\
                       'Station.nc\n'+\
                       'StationCrossRef.nc\n'+\
                       'SourceCrossRef.nc\n'+\
                       'End Session\n!\n')
        
        staAll.sort()
        for ista in staAll:
            fid.writelines('Begin Station %s\n'%(ista.strip())+\
                           'End Station %s\n!\n'%(ista.strip()))
                
        fid.writelines('Begin Scan\n'+\
                       'TimeUTC.nc\n'+\
                       'End Scan\n!\n')
            
        for ib in band:
            fid.writelines('Begin Observation\n'+\
                           'AmbigSize_b%s.nc\n'%(ib)+\
                           'ChannelInfo_b%s.nc\n'%(ib)+\
                           'QualityCode_b%s.nc\n'%(ib)+\
                           'GroupDelay_b%s.nc\n'%(ib))
                
        fid.writelines('ObsCrossRef.nc\n'+\
                       'End Observation\n!\n')
            
        fid.writelines('Begin Program Solve\n'+\
                       'ScanTimeMJD.nc\n'+\
                       'End Program Solve\n!')
        fid.close()
    else:
        dirs = os.listdir(path)
        
        version = 0
        for difFile in dirs:
            if '.wrp' in difFile:
                index1 = difFile.index('_V')
                index2 = difFile.index('_i')
                ver = int(difFile[index1+2:index2])
                if ver >version:
                    version = ver
                    wrpFile = difFile
                    
        session = wrpFile[:index1]
        
        fid = open(path+'/'+wrpFile, 'r')
        lines = fid.readlines()
        fid.close()
        
        index_his = lines.index('End History\n')
        nlines = lines[:index_his]
        
        if flag == 1:
            nlines.extend(['Begin Process vgosDbPlog\n',\
                           'CreatedBy YD\n',\
                           'RunTimeTag %s UTC\n'%(str(currentTime)),\
                           'End Process vgosDbPlog\n',\
                           '!\n'])
        index = []
        staAll.sort()
        for sta in staAll:
            index.append(lines.index('Begin Station %s\n'%(sta.strip())))

        nlines.extend(lines[index_his:index[0]+1])
        for i in range(1,len(staAll)):
            nlines.extend(['Met.nc\n',\
                           'Cal-Cable.nc\n',\
                           'Fmout-GNSS.nc\n'])
            nlines.extend(lines[index[i-1]+1:index[i]+1])
        
        nlines.extend(['Met.nc\n',\
                       'Cal-Cable.nc\n',\
                       'Fmout-GNSS.nc\n'])    
        nlines.extend(lines[index[-1]+1:])
        
        newFile = path+'/'+session + '_V' + '%03d'%(version+1) + '_iYAO_kall.wrp'
        fid = open(newFile,'w')
        fid.writelines(nlines)
        fid.close()
