#!/usr/bin/env python3

import os,sys
sys.path.append("..//")

from INIT import *
from COMMON import *
from INIT.read_AIPS import *
from INIT.read_NGS import *


def init(Param, sessionNum):
    
    v2Flag = 0
    print('\n------------------------  INIT  ------------------------')
    print('    Reading wrapfile......')
    if Param.Setup.calctheroe.upper() == 'CREATE':
        v2Flag = 1
        scanInfo = read_vgosDB_V1(Param, sessionNum)
    else:
        if Param.Arcs.version[sessionNum] > 0:
            scanInfo,wrpInfo = read_vgosDB(Param, sessionNum)
        elif Param.Arcs.version[sessionNum] == 0:
            scanInfo,wrpInfo = ngsScanInfo(Param,sessionNum)
        elif Param.Arcs.version[sessionNum] == -1:
            scanInfo,wrpInfo = createScanInfo(Param,sessionNum)

    aprioriPath(v2Flag, Param)
    print('    Reading station file......')
    stationInfo = read_station(Param.Map.stationFile, scanInfo)
    
    if v2Flag != 1:
        updateScanInfo(scanInfo, Param, wrpInfo)
        
    makeScan(v2Flag, scanInfo)
    # write_result(Param, sessionNum, scanInfo)
    
    
    print('    Reading source file......')
    meanMJD = np.mean(scanInfo.scanMJD)
    sourceInfo = read_source(Param.Map.sourceFile, scanInfo.sourceAll, scanInfo.souPosit,meanMJD)
    
    # print('    Calculate the ionosphere from GIM')
    # ionDelay = readAndCreateIONFile(Param, scanInfo, stationInfo, sourceInfo)
    
    print('    Reading eop file......')
    eopApri = read_eop(Param.Map.eopFile, scanInfo.scanMJD)
    
    print('    Reading ephem file......')
    ephem = read_eph(Param.Map.ephemFile,scanInfo.scanMJD)
    
    if Param.Map.mapFun == 'GPT3':
        read_trpgrid(Param)
    

    #print('-----------------------------------------------\n')
    
    return scanInfo, sourceInfo, stationInfo, eopApri, ephem

def aprioriPath(v2Flag, Param):
    currentPath = os.path.dirname(__file__)
    posit = currentPath.rfind('/')
    
    if v2Flag == 1:
        Param.Map.stationFile = currentPath[:posit]+'/APRIORI/station.txt'
        Param.Map.sourceFile = currentPath[:posit]+'/APRIORI/glo.src'
        Param.Map.eopFile = currentPath[:posit]+'/APRIORI/usno_finals.erp'
        Param.Map.ephemFile = currentPath[:posit]+'/APRIORI/de421.bsp'

        
