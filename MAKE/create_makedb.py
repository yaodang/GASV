#!/usr/bin/env python3

import os,re
from multiprocessing import Pool
import numpy as np

from MAKE.createRoot import *
from MAKE.createScan import *
from MAKE.createCrossReference import *
from MAKE.createObservables import *
from MAKE.createSolve import *
from MAKE.MK4Type import *
from COMMON import *

def makedb(dbInfo):
    '''
    Create the vgosDB format from fringe data

    Parameters
    ----------
    dbInfo: dict{
        'ac'--analysis name
        'dbName'--output file name
        'outPath'--output path
        'inPath'--the hops result file path
        }
    

    Returns
    -------
    The vgosDB data is created.

    '''
    
    print('\n------------------ vgosDB data create ------------------\n')
    vgosDBPath = makePath(dbInfo['dbName'], dbInfo['outPath'])
    session = dbInfo['inPath'][dbInfo['inPath'].rfind('/')+1:]
    
    print('    The path of vgosDb is %s\n'%vgosDBPath)
    print('    Reading the fringe files...')
    tempResult = read_fringe(dbInfo['inPath'])
    result = MK4STRUCT()
    result.band = tempResult[0].band
    result.reBuild()
    result.integrateResult(tempResult)
    
    numScan = len(result.scanTime)
    
    # create Scan path file
    print('    Creating the file of Scan dir...')
    createTimeUTC(vgosDBPath+'/Scan', result.scanTime, numScan)
    
    # create CrossReference path file
    print('    Creating the file of CrossReference dir...')
    crossPath = vgosDBPath+'/CrossReference'
    souAll = createSourceCrossRef(crossPath, np.array(result.scanSou))
    staAll = createStationCrossRef(crossPath, result.scanSta, numScan)
    Obs2Scan, blSort = createObsCrossRef(crossPath, result.scanBL, staAll)
    
    # create Observables path file
    print('    Creating the file of Observables dir...')
    obsPath = vgosDBPath+'/Observables'
    # createSource(obsPath, result.scanSou, Obs2Scan)
    # createBaseline(obsPath, result.scanBL, len(Obs2Scan), blSort)
    
    for ib in range(len(result.band)):
        createQualityCode(obsPath, result.quality[ib], blSort, result.band[ib])
        # createSNR(obsPath, result.snr[ib], blSort, result.band[ib])
        # createDelay(obsPath, result.delay[ib], result.delaySig[ib], blSort, result.band[ib], 0)
        createDelay(obsPath, result.delay[ib], result.delaySig[ib], blSort, result.band[ib], 1)
        createAmbigSize(obsPath, result.ambig[ib], result.band[ib], blSort, len(Obs2Scan))
        createRefFreq(obsPath,result.band[ib])
        createChannelInfo(obsPath, result.ampp[ib], result.apNum[ib], result.sampleRate[ib], \
                          result.channelFreq[ib], result.band[ib], blSort, len(Obs2Scan))
        
    # create Solve path file
    print('    Creating the file of Solve dir...')
    obsPath = vgosDBPath+'/Solve'
    createScanTimeMJD(obsPath, result.scanTime)
    
    # create Head.nc file
    print('    Creating Head.nc...')
    createHead(vgosDBPath, session, staAll, souAll, numScan, len(Obs2Scan))
    
    # create *.wrp file
    print('    Creating wrp file...')
    createWrpFile(vgosDBPath, staAll, 0, result.band, dbInfo['dbName'], dbInfo['ac'])
    
    print('\n    vgosDB is created!')
    

def read_fringe(path):
    
    dirs, fringefiles, rootFiles = getandcheckDir(path)
    
    coreNum = 4
    args_list = []
    
    step = int(len(dirs)/coreNum) + 1
    for i in range(coreNum):
        if i == (coreNum-1):
            index = np.linspace(step*i, len(dirs)-1, len(dirs)-step*i, dtype=int)
        else:
            index = np.linspace(step*i, step*(i+1)-1, step, dtype=int)
            
        files = [fringefiles[k] for k in index]
        rfiles = [rootFiles[k] for k in index]
        args = (dirs[index], files, rfiles)
            
        args_list.append(args)
        
    poolmk4 = Pool(processes=coreNum)
    results = poolmk4.map(parallelMK4,args_list)
    
    # args = (dirs, fringefiles, rootFiles)
    # results = parallelMK4(args)
    
    return results

def getandcheckDir(path):
    '''
    Check the fringe data, search to Level 3 directory. If exists, return the Dirs,
    else print the error information and exits.

    Parameters
    ----------
    path : str
        the fringe path.

    Returns
    -------
    inputPath : str
        the modify finge path
    dirs : list
        the fringe data path.

    '''
    sdirs = []
    fringeFile = []
    rootFile = []
    
    for root, dirs, files in os.walk(path):
        temp = []
        tempRootFile = ''
        for i in range(len(files)):
            res_type2 = re.match(r'\w\w\.[A-Z]\.\d\.*', files[i])
            if res_type2:
                if files[i][0] != files[i][1]:
                    temp.append(files[i])
                    
            if not '.' in files[i][:-7]:
                tempRootFile = files[i]
                
        if len(temp) and len(tempRootFile):
            fringeFile.append(temp)
            sdirs.append(root)
            rootFile.append(tempRootFile)
            
                
    if len(sdirs) == 0:
        print('    No fringe data in path. Nothing to do!\n')
        sys.exit()
    if len(rootFile) != len(fringeFile):
        print('    The number of root file not equal to type file!')
        sys.exit()
        
    index = np.argsort(sdirs)
    newfringeFiles = [fringeFile[k] for k in index]
    newRootFiles = [rootFile[k] for k in index]
            
    return np.array(sdirs)[index], newfringeFiles, newRootFiles

def parallelMK4(args):
    
    dirs, fringefiles, rootFiles = args[0],args[1],args[2]
    
    mk4 = MK4STRUCT()
    band = getBand(dirs[0], fringefiles[0])
    mk4.band = band
    mk4.reBuild()
    
    for idir in range(len(dirs)):
        temp = MK4STRUCT()
        temp.band = band
        temp.reBuild()
        
        # read root file
        rootPath = os.path.join(dirs[idir],rootFiles[idir])
        staName, staSampleRate, staChannelFreq, rootBand = typeRootFile(rootPath)
        
        
        # read type file
        '''
        sort the filelist base on baseline and band
        before: ['ci.X.*', 'Ni.S.*', 'cN.X.*', 'cN.S.*', 'Ni.X.*', 'ci.S.*']
        after:  ['Ni.S.*', 'Ni.X.*', 'cN.S.*', 'cN.X.*', 'ci.S.*', 'ci.X.*']
        '''
        fringeFileList = fringefiles[idir]
        fringeFileList.sort()
        
        flag = 0
        for file in fringeFileList:
            fid = open(dirs[idir]+'/'+file,'rb')
            Bytes = fid.read()
            fid.close()
            
            typePosit = findTypePosit(Bytes)
            
            baseline = type202(Bytes,typePosit[2])
            sampleRate, refFreq = type203(Bytes,typePosit[3])
            ffit_chan = type205(Bytes, typePosit[5])
            apNum = type206(Bytes, typePosit[6])
            type208Data = type208(Bytes,typePosit[8])
            ampp = type210(Bytes,typePosit[9])
            
            useFreq = staChannelFreq[0][rootBand.index(file[3])]
            channelFreq = getChannelFreq(refFreq, ffit_chan, len(useFreq))
            
            staSampleRatePosit1 = staName.index(baseline[0])
            if sampleRate[0]*1E-3 < staSampleRate[staSampleRatePosit1]:
                sampleRate = staSampleRate[staSampleRatePosit1]
            
            
            if flag == 0 and (file[3] in band):
                mk4.scanTime.append(type200(Bytes,typePosit[1]))
                mk4.scanSou.append(type201(Bytes,typePosit[1]))
                flag = 1
            
            
            if file[3] == band[0]:
                for sta in baseline:
                    if sta not in temp.scanSta:
                        temp.scanSta.append(sta)
                temp.scanBL.append(baseline)
            
            type208Data.append(sampleRate)
            type208Data.append(ampp[:len(useFreq)])
            type208Data.append(apNum[:len(useFreq)])
            type208Data.append(channelFreq)
            
            
            iband = band.index(file[3])
            temp.addBandInfo(type208Data,'quality', iband, 0)
        
        mk4.addScan(temp, 0)
        for ib in range(len(band)):           
            mk4.addBandInfo(temp, 'quality', ib, 0)
                    
    return mk4

def getBand(path, files):
    '''
    Get the band list.

    Parameters
    ----------
    path : str
        the fringe data path.
    files : list
        the fringe data file.

    Returns
    -------
    band : list
        the observe band.

    '''
    
    band = []
    
    for file in files:
        if file[3] not in band:
            band.append(file[3])
            
            fid = open(path+'/'+file,'rb')
            Bytes = fid.read()
            fid.close()
    
    band.sort()        
    return band

def getChannelFreq(refFreq, ffit_chan, freqNum):
    
    channelNum = 0
    for i in range(len(ffit_chan)):
        if ffit_chan[i][0] > -1 or ffit_chan[i][1] > -1:
            channelNum += 1
    
    channelFreq = np.zeros(freqNum)
    for i in range(channelNum):
        if ffit_chan[i][0] > -1:
            channel = ffit_chan[i][0]
        else:
            channel = ffit_chan[i][1]
        channelFreq[i] = refFreq[channel]*1E-6
        
    return channelFreq
        
def makePath(dbName, outPath):
    '''
    Check and create the vgosDB path

    Parameters
    ----------
    dbName : str
        output vgosDB name.
    outPath : str
        the path store the vgosDB data.

    Returns
    -------
    The path is created.

    '''
    if '/' == outPath[-1]:
        path = outPath + dbName
    else:
        path = outPath + '/' + dbName
    
    if not os.path.exists(path):
        os.mkdir(path)
        
    if not os.path.exists(path+'/Scan'):
        os.mkdir(path+'/Scan')
        
    if not os.path.exists(path+'/CrossReference'):
        os.mkdir(path+'/CrossReference')
        
    if not os.path.exists(path+'/Observables'):
        os.mkdir(path+'/Observables')
        
    if not os.path.exists(path+'/Solve'):
        os.mkdir(path+'/Solve')   
        
    return path

def findTypePosit(Bytes):
    
    typeName = [b'200',b'201',b'202',b'203',b'204',b'205',b'206',b'207',b'208',b'210']
    typePosit = np.zeros(len(typeName),dtype=int)
    
    for i in range(len(typeName)):
        searchFlag = 1
        if i == 0:
            searchPosit = 0
        else:
            searchPosit = typePosit[i-1]
        
        while searchFlag:
            posit = Bytes[searchPosit:].find(typeName[i]) + searchPosit
                
            if Bytes[searchPosit:].find(typeName[i]) == -1:
                searchFlag = 0
                
            if Bytes[posit+5:posit+8] == b'   ':
                typePosit[i] = posit + 0
                searchFlag = 0
            else:
                searchPosit = posit + 1
    
    notFindPosit = np.where(typePosit == 0)[0]
    if len(notFindPosit):
        for i in notFindPosit:
            if i == 0:
                posit = Bytes[:typePosit[i+1]].find(typeName[i])
                if posit != -1:
                    typePosit[i] = posit
            else:
                posit = Bytes[typePosit[i-1]:typePosit[i+1]].find(typeName[i]) + typePosit[i-1]
                if Bytes[typePosit[i-1]:typePosit[i+1]].find(typeName[i]) != -1:
                    typePosit[i] = posit
            
    return typePosit
        
    
# if __name__ == "__main__":
    # createV1()
