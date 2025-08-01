#!/usr/bin/env python3

import sys

class WRP():
    def __init__(self):
        self.Flag = 0
        self.Session = []
        self.Station = []
        self.Observe = []
        self.Solve = []

def readWrp(wrpFile):
    '''
    Reading the information from wrp file.

    Parameters
    ----------
    wrpFile : str
        the input .wrp file.

    Returns
    -------
    wrpInfo : class
        the class of file information.

    '''
    
    fid = open(wrpFile,'r')
    lines = fid.readlines()
    fid.close()
    
    wrpInfo = WRP()
    wrpInfo.Session = findSession(lines)
    wrpInfo.Station = findStation(lines)
    wrpInfo.Observe = findObserve(lines)
    wrpInfo.Scan = findScan(lines)
    wrpInfo.Solve = findSolve(lines)
    wrpInfo.Flag = processFlag(lines)
    wrpInfo.file = wrpFile
    
    return wrpInfo

def processFlag(lines):
    
    flag = 0
    step = []
    for line in lines:
        if 'Begin Process' in line:
            step.append(line)

    for line in step:
        if 'nuSolve' in line or 'VIPSSolve' in line:
            flag = 2
        if 'db2vgosDB' in line:
            flag = 3

    if flag < 2:
        if 'vgosDbMake' in step[-1] or 'vgosDbCalc' in step[-1] or \
                'vgosDbProcLogs' in step[-1] or 'vgosDbPlog' in step[-1] or \
                'makedb' in step[-1]:
            flag = 1
    '''
    if 'vgosDbMake' in step[-1] or 'vgosDbCalc' in step[-1] or \
       'vgosDbProcLogs' in step[-1] or 'vgosDbPlog' in step[-1] or \
       'makedb' in step[-1]:
        flag = 1
    if 'nuSolve' in step[-1] or 'VIPSSolve' in step[-1]:
        flag = 2
    if  'db2vgosDB' in step[-1]:
        flag = 3
    '''
    return flag
    
def findSession(lines):
    
    session = []
    beginPosit = lines.index('Begin Session\n')
    endPosit = lines.index('End Session\n')
    
    for line in lines[beginPosit+1:endPosit]:
        if line[0] != '!':
        # if '.nc' in line:
            session.append(line[:-1])
    return session

def findStation(lines):
    
    station = [[],[]]
    beginPosit = []
    endPosit = []
    
    for il in range(len(lines)):
        if 'Begin Station' in lines[il]:
            beginPosit.append(il)
        if 'End Station' in lines[il]:
            endPosit.append(il)
            
    if len(beginPosit) != len(endPosit):
        print('    The station readed in wrap is wrong!')
        sys.exit()
        
    for ista in range(len(beginPosit)):
        station[0].append(lines[beginPosit[ista]][14:-1])
        temp = []
        for line in lines[beginPosit[ista]+1:endPosit[ista]]:
            if '.nc' in line:
                temp.append(line[:-1])
            # if 'Cal-Cable' in line:
                # temp.append(line[:-1])
        station[1].append(temp)
    return station

def findObserve(lines):
    
    observe = []
    beginPosit = lines.index('Begin Observation\n')
    endPosit = lines.index('End Observation\n')
    
    for line in lines[beginPosit+1:endPosit]:
        if '.nc' in line:
            observe.append(line[:-1])
    return observe

def findScan(lines):
    try:
        scan = []
        beginPosit = lines.index('Begin Scan\n')
        endPosit = lines.index('End Scan\n')
        
        for line in lines[beginPosit+1:endPosit]:
            if '.nc' in line:
                scan.append(line[:-1])
        return scan
    except ValueError:
        print('    Error: there no Scan part in wrp file!')
        sys.exit()
        
def findSolve(lines):
    
    solve = []
    beginPosit = lines.index('Begin Program Solve\n')
    endPosit = lines.index('End Program Solve\n')
    
    for line in lines[beginPosit+1:endPosit]:
        if '.nc' in line:
            solve.append(line[:-1])
    return solve