#!/usr/bin/env python3

import os,re,struct,sys,time
from multiprocessing import Pool
import numpy as np

sys.path.append('../COMMON')

from time_transfer import *
from createScan import *
from createCrossReference import *
from createObservables import *


class STRUCT():
    def __init__(self):
        self.scanTime = []
        self.scanSou = []
        self.scanSta = []
        self.band = []
        self.scanBL = []
        
        self.quality = []
        self.delay = []
        self.sbdelay = []
        self.delaySig = []
        self.sbdelaySig = []
        self.snr = []
        
    def integrateResult(self, result):
        keys = list(self.__dict__.keys())
        
        for i in range(len(result)):
            for key in keys:
                self.__dict__[key].extend(getattr(result[i], key))
            
    def addDelay(self, delayStruct,param):
        keys = list(self.__dict__.keys())
        index = keys.index(param)
        keys = keys[index:]
        
        if type(delayStruct) == list:
            for ik in range(len(keys)):
                self.__dict__[keys[ik]].append(delayStruct[ik])
        elif type(delayStruct) == STRUCT:
            for key in keys:
                self.__dict__[key].append(getattr(delayStruct, key))

def createV1(inputPath):
    
    inputPath, dirs = getandcheckDir(inputPath)
    
    coreNum = 4
    args_list = []
    
    # step = int(len(dirs)/coreNum) + 1
    # for i in range(coreNum):
    #     if i == (coreNum-1):
    #         args = (inputPath, dirs[np.linspace(step*i, len(dirs)-1, len(dirs)-step*i, dtype=int)])
    #     else:
    #         args = (inputPath, dirs[np.linspace(step*i, step*(i+1)-1, step, dtype=int)])
            
    #     args_list.append(args)
        
    # poolmk4 = Pool(processes=coreNum)
    # results = poolmk4.map(parallelMK4,args_list)
    
    args = (inputPath, dirs)
    results = parallelMK4(args)
    
    return results

def getandcheckDir(inputPath):
    
    dirs = os.listdir(inputPath)
    dirs = np.sort(dirs)
    
    if inputPath[-1] != '/':
        inputPath += '/'
    
    nDirs = []
    for i in range(len(dirs)):
        if os.path.isdir(inputPath+dirs[i]):
            nDirs.append(dirs[i])
            
    return inputPath, np.array(nDirs)

def parallelMK4(args):
    
    inputPath, dirs = args[0],args[1]
    
    mk4 = STRUCT()
    
    for dir in dirs:
        temp = STRUCT()
        
        files = os.listdir(inputPath+dir)
        
        flag = 0
        for file in files:
            res = re.match(r'[A-Z][A-Z]\.[A-Z]\.\d\.*', file)
            if res:
                if file[0] != file[1]:
                    temp.band.append(file[3])
                    
                    fid = open(inputPath+dir+'/'+file,'rb')
                    Bytes = fid.read()
                    fid.close()
                    
                    if flag == 0:
                        
                        mk4.scanTime.append(type200(Bytes))
                        mk4.scanSou.append(type201(Bytes))
                        flag = 1
                        
                    
                    baseline = type202(Bytes)
                    
                    temp.addDelay(type208(Bytes),'quality')
                    for sta in baseline:
                        if sta not in temp.scanSta:
                            temp.scanSta.append(sta)
                            
                    temp.scanBL.append(baseline)
                    
        mk4.addDelay(temp, 'scanSta')
        
    return mk4

def type200(Bytes):
    '''
    Read th type 200 (general information).

    Parameters
    ----------
    Bytes : the type 2 file bytes.

    Returns
    -------
    scanTime : the observer source

    '''
    posit = Bytes.find(b'201')
    byte = [[2,2,2,2,4],['>h','>h','>h','>h','>f']]
    

    scanTime = []
    for i in range(len(byte[0])):
        temp = posit-12+sum(byte[0][:i])
        scanTime.append(struct.unpack(byte[1][i],Bytes[temp:temp+byte[0][i]])[0])
    
    md = doy2day(scanTime[1],scanTime[0])
    scanTime.extend(md)
    
    return scanTime

def type201(Bytes):
    '''
    Read th type 201 (source information).

    Parameters
    ----------
    Bytes : the type 2 file bytes.

    Returns
    -------
    sou : the observer source

    '''
    blank = '        '
    posit = Bytes.find(b'201')
    sou = Bytes[posit+8:posit+8+32].decode()
    
    temp = sou.index('\x00')
    return sou[:temp]+blank[:8-len(sou[:temp])]
    
    
def type202(Bytes):
    '''
    Read th type 202 (baseline information).

    Parameters
    ----------
    Bytes : the type 2 file bytes.

    Returns
    -------
    sta1,sta2 : the station name

    '''
    startP = 288
    posit = Bytes[startP:].find(b'202')
    sta1 = Bytes[startP+posit+14:startP+posit+14+8].decode().replace('\x00',' ')
    sta2 = Bytes[startP+posit+14+8:startP+posit+14+8*2].decode().replace('\x00',' ')
   
    return [sta1,sta2]

def type208(Bytes):
    '''
    Read th type 208 (solution parameter).

    Parameters
    ----------
    Bytes : the type 2 file bytes.

    Returns
    -------
    sou : the observer source

    '''
    
    posit = Bytes.find(b'208')
    quality = Bytes[posit+8:posit+8+1].decode()
    
    delay = struct.unpack('>d', Bytes[posit+64:posit+72])[0] * 1E-6
    sbdelay = struct.unpack('>d', Bytes[posit+72:posit+80])[0] * 1E-6

    delaySig = struct.unpack('>f', Bytes[posit+100:posit+104])[0] * 1E-6
    sbdelaySig = struct.unpack('>f', Bytes[posit+104:posit+108])[0] * 1E-6
    
    snr = struct.unpack('>f',Bytes[posit+128:posit+132])

    return [quality,delay,sbdelay,delaySig,sbdelaySig,snr]

def main():
    
    outPath = '/Users/dangyao/Desktop/23MAR09NU'
    makePath(outPath)
    
    tempResult = createV1('/Users/dangyao/Downloads/1234')
    result = STRUCT()
    result.integrateResult(tempResult)
    
    numScan = len(result.scanTime)
    createTimeUTC(outPath+'/Scan', result.scanTime, numScan)
    
    # create CrossReference path file
    crossPath = outPath+'/CrossReference'
    createSourceCrossRef(crossPath, np.array(result.scanSou))
    staAll = createStationCrossRef(crossPath, result.scanSta, numScan)
    Obs2Scan, blSort = createObsCrossRef(crossPath, result.scanBL, staAll)
    
    # create Observables path file
    obsPath = outPath+'/Observables'
    createSource(obsPath, result.scanSou, Obs2Scan)
    createQualityCode(obsPath, result.quality, blSort)
    createSNR(obsPath, result.snr, blSort)
    createGroupDelay(obsPath, result.delay, result.delaySig, blSort)
    createBaseline(obsPath, result.scanBL, len(Obs2Scan), blSort)
    
def makePath(path):
    
    if not os.path.exists(path):
        os.system('mkdir '+path)
        
    if not os.path.exists(path+'/Scan'):
        os.system('mkdir '+path+'/Scan')
        
    if not os.path.exists(path+'/CrossReference'):
        os.system('mkdir '+path+'/CrossReference')
        
    if not os.path.exists(path+'/Observables'):
        os.system('mkdir '+path+'/Observables')
        

if __name__ == "__main__":
    main()
