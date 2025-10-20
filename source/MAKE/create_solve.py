#!/usr/bin/env python3

from MAKE.createSession import *
from MAKE.createSolve import *
from MAKE.createObsEdit import *
from MAKE.createObsDerived import *
import datetime,os
import numpy as np
from COMMON.other import *

def create_result(vgosDBPath, scanInfo, wrpInfo, Arcs):
    
    # Session directory
    sessionPath = os.path.join(vgosDBPath,'Session')
    createClockBreak(sessionPath, scanInfo.clkBrk.brkFlag, \
                     scanInfo.clkBrk.brkMJD, scanInfo.clkBrk.staName, \
                     wrpInfo.Session)
    try:
        createGroupBLWeights(sessionPath, scanInfo.stationAll,\
                            scanInfo.reweightInfo, wrpInfo.Session)
    except AttributeError:
        pass
    
    # Solve directory
    solvePath = os.path.join(vgosDBPath, 'Solve')
    createClockSetup(solvePath, scanInfo.refclk, wrpInfo.Solve)
    createBaselineClockSetup(solvePath, scanInfo.stationAll, \
                             scanInfo.blClkList, wrpInfo.Solve)

    
    # ObseDerived directory
    ionPath = vgosDBPath + '/ObsDerived'
    if hasattr(scanInfo, "iondl"):
        # two band observe
        createSlantPathIonoGroup(ionPath, scanInfo.iondl, scanInfo.iondlSig, wrpInfo.Observe)
    else:
        # single band observe
        createSlantPathIonoGroup(ionPath, 0, len(scanInfo.Obs2Scan), wrpInfo.Observe)
        

    # ObsEdit directory
    editPath = vgosDBPath + '/ObsEdit'
    createEdit(editPath, scanInfo.delayFlag, wrpInfo.Observe)
    createGroupDelayFull(editPath, scanInfo, wrpInfo.Observe)
    createNumGroupAmbig(editPath, scanInfo, wrpInfo.Observe)
    
    
    # update .wrp file
    fid = open(wrpInfo.file, 'r')
    lines = fid.readlines()
    fid.close()
    
    index_his = lines.index('End History\n')
    nlines = lines[:index_his]
    
    #if wrpInfo.Flag < 2:
    nowTime = datetime.datetime.now()
    nlines.extend(['Begin Process SgLib/VIPSSolve\n',\
                   'RunTimeTag %s UTC\n'%(nowTime.strftime('%Y-%m-%d %H:%M:%S')),\
                   'End Process SgLib/VIPSSolve\n',\
                   '!\n'])
            
    nlines.append('End History\n!\n')
    
    # Session part
    nlines.append('Begin Session\n')
    for file in wrpInfo.Session:
        nlines.append(file+'\n')
    nlines.append('End Session\n!\n')
    
    # Station part
    for i in range(len(wrpInfo.Station[0])):
        nlines.append('Begin Station %s\n'%wrpInfo.Station[0][i])
        for file in wrpInfo.Station[1][i]:
            nlines.append(file+'\n')
        nlines.append('End Station %s\n!\n'%wrpInfo.Station[0][i])
    
    # Scan part
    nlines.append('Begin Scan\n')
    for file in wrpInfo.Scan:
        nlines.append(file+'\n')
    nlines.append('End Scan\n!\n')
        
    # Observe part
    nlines.append('Begin Observation\n')
    for file in wrpInfo.Observe:
        nlines.append(file+'\n')
    nlines.append('End Observation\n!\n')
    
    # Solve part
    nlines.append('Begin Program Solve\n')
    for file in wrpInfo.Solve:
        nlines.append(file+'\n')
    nlines.append('End Program Solve\n!\n')

    version = searchWrp(vgosDBPath) + 1
    newFile = Arcs.session[0] + '_V' + '%03d'%version + '_iNTSC_kall.wrp'
    
    fid = open(vgosDBPath + '/'+newFile,'w')
    fid.writelines(nlines)
    fid.close()
